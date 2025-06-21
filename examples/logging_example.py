"""
Logging example for bosskit
"""

import logging

from bosskit import BossKit

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize with logging enabled
bk = BossKit(enable_logging=True)

# Example chat with logging
response = bk.chat("What is the weather like today?")
print("Response:", response)

# Log custom message
bk.logger.info("Custom log message")
