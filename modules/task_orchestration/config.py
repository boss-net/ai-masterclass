# Task Orchestration Configuration

# Task Settings
MAX_TASKS = 100
TASK_TIMEOUT = 300  # seconds
RETRY_DELAY = 1  # seconds
MAX_RETRIES = 3

# Workflow Settings
MAX_WORKFLOWS = 50
WORKFLOW_TIMEOUT = 600  # seconds
MAX_CONCURRENT = 10

# Priority Settings
PRIORITY_LEVELS = 5
DEFAULT_PRIORITY = 3
PRIORITY_QUEUE_SIZE = 100

# Resource Management
RESOURCE_POOL_SIZE = 20
MEMORY_LIMIT = 1024 * 1024 * 1024  # 1GB
CPU_LIMIT = 100  # percentage

# Error Handling
ERROR_TTL = 3600  # seconds
MAX_ERROR_RETRIES = 5
ERROR_BACKOFF = 2  # exponential backoff factor

# Performance Settings
BATCH_SIZE = 10
CACHE_ENABLED = True
CACHE_TTL = 300  # seconds

# Monitoring Settings
METRICS_ENABLED = True
METRIC_INTERVAL = 60  # seconds
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "./logs/task_orchestration.log"

# Storage Settings
TASK_STORE_TYPE = "sqlite"
TASK_STORE_PATH = "./data/task_store.db"
TASK_STORE_TTL = 86400  # 24 hours in seconds

# API Settings
API_TIMEOUT = 30  # seconds
RATE_LIMIT = 60  # requests per minute
INPUT_VALIDATION = True

# Security Settings
AUTH_ENABLED = True
RATE_LIMITING = True
ERROR_MASKING = True
