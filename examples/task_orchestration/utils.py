# Task Orchestration Utilities

import json
import logging
from datetime import datetime
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


def validate_task(task: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Validate task against schema."""
    required_fields = schema.get("required", [])
    for field in required_fields:
        if field not in task:
            logger.warning(f"Missing required field: {field}")
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
        if "task_id" in kwargs:
            task_id = kwargs["task_id"]
        else:
            task_id = args[0] if args else "default"

        if task_id in last_call:
            elapsed = now - last_call[task_id]
            if elapsed < 1:  # 1 request per second
                time.sleep(1 - elapsed)

        last_call[task_id] = time.time()
        return func(*args, **kwargs)

    return wrapper


def batch_process(tasks: List[Dict[str, Any]], batch_size: int = 10) -> List[List[Dict[str, Any]]]:
    """Batch process tasks."""
    return [tasks[i : i + batch_size] for i in range(0, len(tasks), batch_size)]


def create_task_id() -> str:
    """Create unique task ID."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"task_{timestamp}"


def format_workflow_input(workflow: Dict[str, Any], template: str) -> str:
    """Format workflow input with template."""
    try:
        return template.format(**workflow)
    except KeyError as e:
        logger.warning(f"Missing workflow variable: {e}")
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


def monitor_performance(func):
    """Performance monitoring decorator."""
    import time
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        duration = end_time - start_time
        logger.info(f"{func.__name__} completed in {duration:.2f} seconds")
        return result

    return wrapper
