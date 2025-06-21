# RAG Utilities

import json
import logging
import os
import time
from datetime import datetime
from functools import wraps
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.py") -> Dict[str, Any]:
    """Load configuration from file."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return {}


def validate_document(doc: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Validate document against schema."""
    required_fields = schema.get("required", [])
    for field in required_fields:
        if field not in doc:
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


def batch_process(
    documents: List[Dict[str, Any]], batch_size: int = 10
) -> List[List[Dict[str, Any]]]:
    """Batch process documents."""
    return [documents[i : i + batch_size] for i in range(0, len(documents), batch_size)]


def create_document_id() -> str:
    """Create unique document ID."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"doc_{timestamp}"


def format_query(query: str, context: List[Dict[str, Any]]) -> str:
    """Format query with context."""
    context_str = "\n".join([doc["text"] for doc in context])
    return f"Query: {query}\nContext:\n{context_str}"


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


def validate_response(response: Dict[str, Any]) -> bool:
    """Validate API response format."""
    required_fields = ["id", "object", "created", "choices"]
    return all(field in response for field in required_fields)


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into chunks."""
    chunks = []
    text_length = len(text)

    for i in range(0, text_length, chunk_size - overlap):
        chunk = text[i : i + chunk_size]
        chunks.append(chunk)

    return chunks
