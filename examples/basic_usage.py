"""
Basic usage example for bosskit
"""

from bosskit import BossKit

# Initialize the bosskit instance
bk = BossKit()

# Example of using a model
response = bk.model("gpt-3.5-turbo").chat("Hello, how are you?")
print(f"Model response: {response}")
