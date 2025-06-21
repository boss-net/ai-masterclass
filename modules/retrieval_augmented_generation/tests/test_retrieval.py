import pytest
from modules.retrieval_augmented_generation.local_rag import LocalVectorStore, RAGAgent


def test_retrieval_accuracy():
    agent = RAGAgent()

    # Add test documents
    agent.add_documents(
        [
            "This is a test document about AI.",
            "Another document about machine learning.",
        ]
    )

    # Test retrieval
    results = agent.retrieve_context("AI")
    assert len(results) > 0
    assert "test document" in results[0].text.lower()


def test_context_generation():
    agent = RAGAgent()

    # Add documents
    agent.add_documents(["This is a test document about AI."])

    # Generate response with context
    response = agent.process_query("What is discussed in the document?")
    assert isinstance(response, str)
    assert "AI" in response.lower()


def test_error_handling():
    agent = RAGAgent()

    # Test with invalid query
    response = agent.process_query(None)
    assert response is None

    # Test with empty documents
    agent.add_documents([])
    response = agent.process_query("Test")
    assert "no documents found" in response.lower()
