"""
Error handling example for bosskit
"""

from bosskit import BossKit
from bosskit.exceptions import ModelError

bk = BossKit()

try:
    # Try using a non-existent model
    response = bk.model("non-existent-model").chat("Hello")
except ModelError as e:
    print(f"Error: {e}")

try:
    # Try sending invalid input
    response = bk.chat(123)  # Invalid input type
except TypeError as e:
    print(f"Type error: {e}")
