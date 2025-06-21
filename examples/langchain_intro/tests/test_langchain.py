import pytest
from modules.langchain_intro.langchain import LangChainAgent


def test_langchain_agent_creation():
    agent = LangChainAgent()
    assert agent is not None


def test_agent_run():
    agent = LangChainAgent()
    response = agent.run("What is the weather?")
    assert isinstance(response, str)
    assert len(response) > 0


def test_agent_with_memory():
    agent = LangChainAgent()
    agent.run("Remember that I like pizza")
    response = agent.run("What do I like?")
    assert "pizza" in response.lower()
