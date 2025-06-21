"""
Caching example for bosskit
"""

from bosskit import BossKit

# Initialize with caching enabled
bk = BossKit(enable_caching=True)

# First request (will be cached)
response1 = bk.chat("What is the capital of France?")
print("First request:", response1)

# Second request (will use cache)
response2 = bk.chat("What is the capital of France?")
print("Second request (cached):", response2)

# Clear cache
bk.clear_cache()

# Third request (cache cleared)
response3 = bk.chat("What is the capital of France?")
print("Third request (cache cleared):", response3)
