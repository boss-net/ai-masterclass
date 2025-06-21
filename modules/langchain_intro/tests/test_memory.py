import pytest
from modules.langchain_intro.langchain import ConversationMemory, LangChainAgent, VectorStoreMemory


def test_conversation_memory():
    agent = LangChainAgent()
    memory = ConversationMemory()

    # Add messages
    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi there!")

    # Get conversation history
    history = memory.get_history()
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_vector_store_memory():
    agent = LangChainAgent()
    memory = VectorStoreMemory()

    # Add documents
    memory.add_document("This is a test document about AI.")
    memory.add_document("Another document about machine learning.")

    # Search
    results = memory.search("AI")
    assert len(results) > 0
    assert "test document" in results[0].text.lower()


def test_memory_integration():
    agent = LangChainAgent()

    # Add conversation memory
    agent.set_memory(ConversationMemory())

    # Run with memory
    agent.run("What is your name?")

    # Verify memory is updated
    history = agent.get_memory().get_history()
    assert len(history) > 0
