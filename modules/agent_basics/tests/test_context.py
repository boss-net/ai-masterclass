import pytest
from modules.agent_basics.agents import ContextAgent


def test_context_management():
    agent = ContextAgent()

    # Set initial context
    agent.set_context({"user": "test_user", "history": []})

    # Get context
    context = agent.get_context()
    assert context["user"] == "test_user"
    assert isinstance(context["history"], list)


def test_context_persistence():
    agent = ContextAgent()

    # Set context
    agent.set_context({"user": "test_user"})

    # Process prompt (should maintain context)
    agent.process_prompt("Hello")

    # Verify context is maintained
    context = agent.get_context()
    assert context["user"] == "test_user"
