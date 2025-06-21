import pytest
from modules.retrieval_augmented_generation.local_rag import RAGAgent


def test_rag_agent_creation():
    agent = RAGAgent()
    assert agent is not None


def test_document_addition():
    agent = RAGAgent()
    agent.add_documents(["test.txt"])
    assert len(agent.get_documents()) > 0


def test_query_with_context():
    agent = RAGAgent()

    # Add test document
    agent.add_documents(["test.txt"])

    # Query should return relevant information
    response = agent.query("What is in the test document?")
    assert isinstance(response, str)
    assert len(response) > 0
