# RAG Configuration

# Model Settings
DEFAULT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# Vector Store Settings
VECTOR_STORE_TYPE = "chroma"
VECTOR_STORE_PATH = "./data/vector_store"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval Settings
TOP_K = 5
MIN_SCORE = 0.5
MAX_CONTEXT = 2000

# Generation Settings
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
MEMORY_WINDOW = 10

# Performance Settings
CACHE_ENABLED = True
CACHE_TTL = 300  # seconds
BATCH_SIZE = 10

# Storage Settings
DOCUMENT_STORE_TYPE = "sqlite"
DOCUMENT_STORE_PATH = "./data/document_store.db"
DOCUMENT_TTL = 86400  # 24 hours in seconds

# API Settings
OPENAI_API_BASE = "https://api.openai.com/v1"
API_TIMEOUT = 30  # seconds
RATE_LIMIT = 60  # requests per minute

# Security Settings
INPUT_VALIDATION = True
ERROR_MASKING = True
RATE_LIMITING = True

# Monitoring Settings
METRICS_ENABLED = True
METRIC_INTERVAL = 60  # seconds
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "./logs/rag.log"

# Document Processing
default_document_config = {
    "max_size": 1048576,  # 1MB
    "allowed_types": ["txt", "pdf", "docx"],
    "chunking": {"strategy": "sliding_window", "size": 1000, "overlap": 200},
}

# Error Handling
default_error_config = {
    "max_retries": 3,
    "backoff_factor": 2,
    "timeout": 30,
    "retry_on": ["timeout", "connection_error"],
}
