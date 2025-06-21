# LangChain Configuration

# Model Settings
DEFAULT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# Memory Settings
MEMORY_BACKEND = "sqlite"
MEMORY_PATH = "./data/langchain_memory.db"
MEMORY_TTL = 86400  # 24 hours in seconds

# Vector Store Settings
VECTOR_STORE_TYPE = "chroma"
VECTOR_STORE_PATH = "./data/vector_store"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Chain Settings
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
MAX_CONCURRENT = 5

# Tool Settings
default_tool_config = {
    "api": {"timeout": 30, "rate_limit": 60, "retry_count": 3},
    "file": {"max_size": 1048576, "allowed_types": ["txt", "pdf", "docx"]},  # 1MB
    "web": {"max_requests": 10, "timeout": 10, "retry_count": 3},
}

# Performance Settings
CACHE_ENABLED = True
CACHE_TTL = 300  # seconds
BATCH_SIZE = 10

# Security Settings
RATE_LIMIT = 60  # requests per minute
INPUT_VALIDATION = True
ERROR_MASKING = True

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "./logs/langchain.log"
