from unittest.mock import MagicMock, patch

import pytest

from bosskit.commands import Commands
from bosskit.io import IO
from bosskit.models import Model


@pytest.fixture
def mock_io():
    return MagicMock(spec=IO)


@pytest.fixture
def mock_model():
    return MagicMock(spec=Model)


@pytest.fixture
def commands(mock_io, mock_model):
    return Commands(mock_io, mock_model)


def test_is_command(commands):
    assert commands.is_command("/test") is True
    assert commands.is_command("test") is False
    assert commands.is_command(" /test") is True


def test_get_commands(commands):
    commands_list = commands.get_commands()
    assert all(cmd.startswith("/") for cmd in commands_list)
    assert len(commands_list) > 0


def test_command_execution(commands, mock_io):
    mock_io.input.return_value = "test input"

    with patch.object(commands, "cmd_test", return_value=None) as mock_cmd:
        commands.execute("/test")
        mock_cmd.assert_called_once()

    with patch.object(commands, "cmd_test", side_effect=Exception("Test error")) as mock_cmd:
        commands.execute("/test")
        mock_io.error.assert_called_once()


def test_command_validation(commands):
    assert commands.is_command("/test") is True
    assert commands.is_command("test") is False
    assert commands.is_command(" /test") is True
    assert commands.is_command("/test ") is True
    assert commands.is_command("/test/test") is True


def test_command_completion(commands):
    completions = commands.get_completions("/")
    assert isinstance(completions, list)
    assert all(isinstance(c, str) for c in completions)
    assert len(completions) > 0


def test_command_help(commands, mock_io):
    commands.help()
    mock_io.print.assert_called()


@patch("bosskit.commands.Commands.get_commands")
def test_command_list(mock_get_commands, commands, mock_io):
    mock_get_commands.return_value = ["/cmd1", "/cmd2"]
    commands.list_commands()
    mock_io.print.assert_called()


@patch("bosskit.commands.Commands.get_completions")
def test_command_complete(mock_get_completions, commands, mock_io):
    mock_get_completions.return_value = ["test"]
    result = commands.complete("", 0)
    assert result == "test"


@patch("bosskit.commands.Commands.get_completions")
def test_command_complete_empty(mock_get_completions, commands, mock_io):
    mock_get_completions.return_value = []
    result = commands.complete("", 0)
    assert result is None


def test_command_execution_success(commands, mock_io):
    mock_io.input.return_value = "test input"

    with patch.object(commands, "cmd_test", return_value="Command executed successfully") as mock_cmd:
        result = commands.execute("/test")
        mock_cmd.assert_called_once()

        assert result.exit_code == 0
        assert "Command executed successfully" in result.output
