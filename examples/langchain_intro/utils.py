# LangChain Utilities

import json
import logging
import os
import time
from functools import wraps
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.py") -> Dict[str, Any]:
    """Load configuration from file."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return {}


def validate_input(input_data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Validate input data against schema."""
    for field, field_type in schema.items():
        if field not in input_data:
            logger.warning(f"Missing required field: {field}")
            return False
        if not isinstance(input_data[field], field_type):
            logger.warning(f"Invalid type for {field}")
            return False
    return True


def rate_limit(func):
    """Rate limiting decorator."""
    import time
    from functools import wraps

    last_call = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        now = time.time()
        if "user_id" in kwargs:
            user_id = kwargs["user_id"]
        else:
            user_id = args[0] if args else "default"

        if user_id in last_call:
            elapsed = now - last_call[user_id]
            if elapsed < 1:  # 1 request per second
                time.sleep(1 - elapsed)

        last_call[user_id] = time.time()
        return func(*args, **kwargs)

    return wrapper


def batch_process(data: List[Any], batch_size: int = 10) -> List[List[Any]]:
    """Batch process data."""
    return [data[i : i + batch_size] for i in range(0, len(data), batch_size)]


def create_vector_store_path(base_path: str = "./data/vector_store") -> str:
    """Create vector store path with timestamp."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(base_path, f"store_{timestamp}")


def format_chain_input(input_data: Dict[str, Any], template: str) -> str:
    """Format chain input with template."""
    try:
        return template.format(**input_data)
    except KeyError as e:
        logger.warning(f"Missing input variable: {e}")
        return template


def error_handler(func):
    """Error handling decorator."""
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return None

    return wrapper
