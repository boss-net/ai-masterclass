# Retrieval-Augmented Generation

This module implements Retrieval-Augmented Generation (RAG) systems.

## Overview

RAG combines retrieval-based and generative approaches to create more accurate and context-aware responses. This module includes:
- Document retrieval
- Context-aware generation
- Hybrid search
- Local vector store implementation

## Usage

```python
from local_rag import RAGAgent

agent = RAGAgent()

# Add documents to the knowledge base
agent.add_documents(["document1.txt", "document2.txt"])

# Generate responses with context
response = agent.query("What is discussed in the documents?")
```

## Requirements

See `requirements.txt` for module-specific dependencies.

## Tests

Run module-specific tests:

```bash
pytest tests/
```

## Documentation

Additional documentation can be found in the `docs` directory.
