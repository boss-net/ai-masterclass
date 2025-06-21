import pytest
from agents import BasicAgent


def test_basic_agent_creation():
    agent = BasicAgent()
    assert agent is not None


def test_agent_response():
    agent = BasicAgent()
    response = agent.process_prompt("Hello")
    assert isinstance(response, str)
    assert len(response) > 0


def test_agent_error_handling():
    agent = BasicAgent()
    with pytest.raises(ValueError):
        agent.process_prompt(None)
