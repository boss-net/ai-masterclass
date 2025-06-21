"""
Model integration example for bosskit
"""

from bosskit import BossKit
from bosskit.models import ChatMessage

# Initialize with specific model
bk = BossKit(default_model="gpt-4")

# Create chat messages
messages = [
    ChatMessage(role="system", content="You are a helpful assistant."),
    ChatMessage(role="user", content="Explain machine learning in simple terms."),
]

# Get response
response = bk.chat(messages)
print(f"Response: {response}")

# Use streaming
for chunk in bk.stream_chat(messages):
    print(chunk, end="", flush=True)

# Use embeddings
embedding = bk.embed("Hello world")
print(f"Embedding length: {len(embedding)}")
