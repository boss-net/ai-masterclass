# Agent Basics Utilities

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict

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


def create_memory_key(user_id: str, context_id: str = None) -> str:
    """Create a unique memory key."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if context_id:
        return f"{user_id}_{context_id}_{timestamp}"
    return f"{user_id}_{timestamp}"


def validate_response(response: Dict[str, Any]) -> bool:
    """Validate API response format."""
    required_fields = ["id", "object", "created", "choices"]
    return all(field in response for field in required_fields)


def format_prompt(template: str, context: Dict[str, Any]) -> str:
    """Format prompt with context variables."""
    try:
        return template.format(**context)
    except KeyError as e:
        logger.warning(f"Missing context variable: {e}")
        return template


def rate_limit(func):
    """Decorator for rate limiting."""
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
