from pathlib import Path

import pytest

from bosskit.models.base import BaseModel, ModelMessage, ModelSettings


@pytest.fixture
def base_model():
    settings = ModelSettings(name="test-model", edit_format="whole", use_repo_map=True)
    return BaseModel(settings)


def test_model_settings():
    settings = ModelSettings(name="test-model", edit_format="whole", use_repo_map=True)
    assert settings.name == "test-model"
    assert settings.edit_format == "whole"
    assert settings.use_repo_map is True


def test_model_message():
    message = ModelMessage(role="user", content="test message")
    assert message.role == "user"
    assert message.content == "test message"


def test_abstract_methods(base_model):
    with pytest.raises(NotImplementedError):
        base_model.validate_environment()

    with pytest.raises(NotImplementedError):
        base_model.get_model_info()

    with pytest.raises(NotImplementedError):
        base_model.send_completion([])

    with pytest.raises(NotImplementedError):
        base_model.token_count([])

    with pytest.raises(NotImplementedError):
        base_model.token_count_for_image(Path("test.jpg"))
