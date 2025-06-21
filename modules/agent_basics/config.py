# Agent Basics Configuration

# Basic Settings
DEFAULT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 2000
TEMPERATURE = 0.7

# Context Settings
MAX_HISTORY_LENGTH = 10
CONTEXT_TTL = 3600  # seconds

# Performance Settings
RATE_LIMIT = 60  # requests per minute
CACHE_TTL = 300  # seconds

# Error Handling
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Storage
MEMORY_BACKEND = "sqlite"
MEMORY_PATH = "./data/agent_memory.db"

# API Settings
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_API_TIMEOUT = 30  # seconds

# Tool Integration
default_tool_config = {"max_retries": 3, "timeout": 10, "rate_limit": 5}
