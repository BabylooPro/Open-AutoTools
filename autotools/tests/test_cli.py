import pytest
from click import Context, Option
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from autotools.cli import cli, _display_command_options, _display_commands, _display_usage_examples, autotools

# TEST FOR DISPLAY COMMAND OPTIONS
def test_display_command_options():
    mock_cmd = MagicMock()
    mock_cmd.params = []
    _display_command_options(mock_cmd)    
    mock_option = Option(['--test', '-t'], help='Test option')
    mock_cmd.params = [mock_option]
    _display_command_options(mock_cmd)

# TEST FOR DISPLAY COMMAND OPTIONS NO PARAMS ATTRIBUTE
def test_display_command_options_no_params():
    mock_cmd = MagicMock()
    del mock_cmd.params
    _display_command_options(mock_cmd)

# TEST FOR DISPLAY COMMANDS
def test_display_commands():
    ctx = Context(cli)
    commands = cli.list_commands(ctx)
    _display_commands(ctx, commands)

# TEST FOR DISPLAY USAGE EXAMPLES
def test_display_usage_examples():
    _display_usage_examples()

# TEST FOR AUTOTOOLS COMMAND
@patch('autotools.cli.check_for_updates')
def test_autotools_command(mock_updates):
    mock_updates.return_value = None
    runner = CliRunner()
    result = runner.invoke(cli, ['autotools'])
    assert result.exit_code == 0
    assert "Open-AutoTools Commands:" in result.output

# TEST FOR AUTOTOOLS COMMAND WITH UPDATE
@patch('autotools.cli.check_for_updates')
def test_autotools_command_with_update(mock_updates):
    mock_updates.return_value = "Update available: v1.0.0"
    runner = CliRunner()
    result = runner.invoke(cli, ['autotools'])
    assert result.exit_code == 0
    assert "Update Available:" in result.output

# TEST FOR CLI HELP OPTION
@patch('autotools.cli.check_for_updates')
def test_cli_help_option(mock_updates):
    mock_updates.return_value = None
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0

# TEST FOR CLI HELP OPTION WITH UPDATE
@patch('autotools.cli.check_for_updates')
def test_cli_help_option_with_update(mock_updates):
    mock_updates.return_value = "Update available"
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
