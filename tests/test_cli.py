import os
import json as json_module
import pytest
from click import Context, Option
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from autotools.cli import cli, _display_command_options, _display_commands, _display_usage_examples, autotools


# FIXTURES
@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def mock_check_updates_none():
    with patch('autotools.cli.check_for_updates', return_value=None) as mock:
        yield mock


@pytest.fixture
def mock_check_updates_available():
    with patch('autotools.cli.check_for_updates', return_value="Update available: v1.0.0") as mock:
        yield mock

# HELPERS
def _create_mock_command(name):
    cmd = MagicMock()
    cmd.name = name
    return cmd

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
def test_autotools_command(cli_runner, mock_check_updates_none):
    result = cli_runner.invoke(cli, ['autotools'])
    assert result.exit_code == 0
    assert "Open-AutoTools Commands:" in result.output

# TEST FOR AUTOTOOLS COMMAND WITH UPDATE
def test_autotools_command_with_update(cli_runner, mock_check_updates_available):
    result = cli_runner.invoke(cli, ['autotools'])
    assert result.exit_code == 0
    assert "Update Available:" in result.output

# TEST FOR CLI HELP OPTION
def test_cli_help_option(cli_runner, mock_check_updates_none):
    result = cli_runner.invoke(cli, ['--help'])
    assert result.exit_code == 0

# TEST FOR CLI HELP OPTION WITH UPDATE
def test_cli_help_option_with_update(cli_runner, mock_check_updates_available):
    result = cli_runner.invoke(cli, ['--help'])
    assert result.exit_code == 0

# TEST FOR CLI WITH METRICS ENABLED
@patch('autotools.cli.autotools')
@patch('autotools.cli.should_enable_metrics')
@patch('autotools.cli.init_metrics')
@patch('autotools.cli.get_metrics')
@patch('autotools.cli.check_for_updates')
def test_cli_with_metrics_enabled(mock_updates, mock_get_metrics, mock_init_metrics, mock_should_enable, mock_autotools, cli_runner):
    mock_should_enable.return_value = True
    mock_metrics = MagicMock()
    mock_get_metrics.return_value = mock_metrics
    mock_updates.return_value = None
    mock_autotools.return_value = None
    
    result = cli_runner.invoke(cli, ['autotools'])
    assert result.exit_code == 0
    mock_init_metrics.assert_called_once()

    assert mock_metrics.step_start.called
    assert mock_metrics.step_end.called
    assert mock_metrics.end_startup.called

# TEST FOR CLI NO SUBCOMMAND WITH METRICS
@patch('autotools.cli.autotools')
@patch('autotools.cli.should_enable_metrics')
@patch('autotools.cli.init_metrics')
@patch('autotools.cli.get_metrics')
@patch('autotools.cli.finalize_metrics')
@patch('autotools.cli.check_for_updates')
def test_cli_no_subcommand_with_metrics(mock_updates, mock_finalize, mock_get_metrics, mock_init_metrics, mock_should_enable, mock_autotools, cli_runner):
    mock_should_enable.return_value = True
    mock_metrics = MagicMock()
    mock_get_metrics.return_value = mock_metrics
    mock_updates.return_value = None
    mock_autotools.return_value = None
    
    result = cli_runner.invoke(cli, [])
    assert result.exit_code == 0
    mock_finalize.assert_called_once()
    assert mock_metrics.end_process.called

# TEST FOR EXECUTE WITH METRICS DISABLED
@patch('autotools.utils.commands.should_enable_metrics')
@patch('autotools.utils.commands.get_metrics')
def test_execute_with_metrics_disabled(mock_get_metrics, mock_should_enable):
    from autotools.utils.commands import _execute_with_metrics
    
    mock_should_enable.return_value = False
    mock_callback = MagicMock(return_value='result')
    mock_ctx = MagicMock()
    
    result = _execute_with_metrics(mock_ctx, mock_callback, 'arg1', 'arg2', kwarg1='value1')
    
    assert result == 'result'
    mock_callback.assert_called_once_with('arg1', 'arg2', kwarg1='value1')

# TEST FOR WRAP COMMAND WITH CTX PARAMETER
@patch('autotools.utils.commands._execute_with_metrics')
def test_wrap_command_with_ctx_parameter(mock_execute):
    from autotools.utils.commands import _wrap_command_with_metrics
    from click import Command, Context
    
    def test_callback(ctx, arg1, arg2): return f"{arg1}-{arg2}"
    
    mock_execute.return_value = 'test-result'
    mock_cmd = Command('test_cmd')
    mock_cmd.callback = test_callback
    
    wrapped_cmd = _wrap_command_with_metrics(mock_cmd)
    wrapped_callback = wrapped_cmd.callback
    
    mock_ctx = Context(mock_cmd)
    mock_ctx.params = {}
    
    with mock_ctx.scope(): result = wrapped_callback('val1', 'val2')
    
    mock_execute.assert_called_once()
    call_args = mock_execute.call_args[0]
    assert isinstance(call_args[0], Context)
    assert call_args[1] == test_callback
    assert isinstance(call_args[2], Context)
    assert call_args[3] == 'val1'
    assert call_args[4] == 'val2'
    assert result == 'test-result'

# TEST FOR WRAP COMMAND WITH EXISTING PERF OPTION
@patch('autotools.utils.commands._execute_with_metrics')
def test_wrap_command_with_existing_perf_option(mock_execute):
    from autotools.utils.commands import _wrap_command_with_metrics
    from click import Command, Context, Option
    
    def test_callback(arg1, arg2): return f"{arg1}-{arg2}"
    
    mock_execute.return_value = 'test-result'
    mock_cmd = Command('test_cmd')
    mock_cmd.callback = test_callback

    perf_option = Option(['--perf'], is_flag=True, help='Display performance metrics')
    mock_cmd.params.append(perf_option)
    
    wrapped_cmd = _wrap_command_with_metrics(mock_cmd)
    wrapped_callback = wrapped_cmd.callback
    
    perf_options = [param for param in wrapped_cmd.params if isinstance(param, Option) and '--perf' in param.opts]
    assert len(perf_options) == 1
    
    mock_ctx = Context(mock_cmd)
    mock_ctx.params = {}
    
    with mock_ctx.scope(): result = wrapped_callback('val1', 'val2')
    
    assert result == 'test-result'
    mock_execute.assert_called_once()
    call_args = mock_execute.call_args[0]
    assert isinstance(call_args[0], Context)
    assert call_args[1] == test_callback
    assert call_args[2] == 'val1'
    assert call_args[3] == 'val2'

# TEST FOR CLI WITH METRICS DISABLED
@patch('autotools.cli.autotools')
@patch('autotools.cli.should_enable_metrics')
@patch('autotools.cli.check_for_updates')
def test_cli_with_metrics_disabled_at_init(mock_updates, mock_should_enable, mock_autotools, cli_runner):
    mock_should_enable.return_value = False
    mock_updates.return_value = None
    mock_autotools.return_value = None
    
    result = cli_runner.invoke(cli, [])
    assert result.exit_code == 0
    mock_should_enable.assert_called()

# TEST FOR CLI NO SUBCOMMAND WITH METRICS DISABLED
@patch('autotools.cli.autotools')
@patch('autotools.cli.should_enable_metrics')
@patch('autotools.cli.init_metrics')
@patch('autotools.cli.get_metrics')
@patch('autotools.cli.finalize_metrics')
@patch('autotools.cli.check_for_updates')
def test_cli_no_subcommand_with_metrics_disabled_at_finalize(mock_updates, mock_finalize, mock_get_metrics, mock_init_metrics, mock_should_enable, mock_autotools, cli_runner):
    call_count = {'count': 0}
    
    def should_enable_side_effect(ctx):
        call_count['count'] += 1
        if call_count['count'] == 1: return True
        return False
    
    mock_should_enable.side_effect = should_enable_side_effect
    mock_metrics = MagicMock()
    mock_get_metrics.return_value = mock_metrics
    mock_updates.return_value = None
    mock_autotools.return_value = None
    
    result = cli_runner.invoke(cli, [])
    assert result.exit_code == 0
    mock_finalize.assert_not_called()

# TEST FOR EXECUTE WITH METRICS ENABLED AND PROCESS_START IS NONE
@patch('autotools.utils.commands.should_enable_metrics')
@patch('autotools.utils.commands.init_metrics')
@patch('autotools.utils.commands.get_metrics')
@patch('autotools.utils.commands.track_step')
@patch('autotools.utils.commands.finalize_metrics')
def test_execute_with_metrics_enabled_process_start_none(mock_finalize, mock_track_step, mock_get_metrics, mock_init_metrics, mock_should_enable):
    from autotools.utils.commands import _execute_with_metrics
    from contextlib import nullcontext
    
    mock_should_enable.return_value = True
    mock_callback = MagicMock(return_value='result')
    mock_ctx = MagicMock()
    mock_ctx.invoked_subcommand = 'test_cmd'
    mock_ctx.command.name = 'test_cmd'
    
    mock_metrics = MagicMock()
    mock_metrics.process_start = None
    mock_metrics.process_end = None
    mock_get_metrics.return_value = mock_metrics
    mock_track_step.return_value = nullcontext()
    
    result = _execute_with_metrics(mock_ctx, mock_callback, 'arg1', 'arg2')
    
    mock_init_metrics.assert_called_once()
    mock_get_metrics().end_startup.assert_called_once()
    mock_metrics.start_command.assert_called_once()
    mock_track_step.assert_called_once_with('command_test_cmd')
    mock_metrics.end_command.assert_called_once()
    mock_metrics.end_process.assert_called_once()
    mock_finalize.assert_called_once_with(mock_ctx)
    assert result == 'result'

# TEST FOR EXECUTE WITH METRICS ENABLED AND PROCESS_START IS NOT NONE
@patch('autotools.utils.commands.should_enable_metrics')
@patch('autotools.utils.commands.get_metrics')
@patch('autotools.utils.commands.track_step')
@patch('autotools.utils.commands.finalize_metrics')
def test_execute_with_metrics_enabled_process_start_not_none(mock_finalize, mock_track_step, mock_get_metrics, mock_should_enable):
    from autotools.utils.commands import _execute_with_metrics
    from contextlib import nullcontext
    
    mock_should_enable.return_value = True
    mock_callback = MagicMock(return_value='result')
    mock_ctx = MagicMock()
    mock_ctx.invoked_subcommand = 'test_cmd'
    mock_ctx.command.name = 'test_cmd'
    
    mock_metrics = MagicMock()
    mock_metrics.process_start = 123.0
    mock_metrics.process_end = None
    mock_get_metrics.return_value = mock_metrics
    mock_track_step.return_value = nullcontext()
    
    result = _execute_with_metrics(mock_ctx, mock_callback, 'arg1', 'arg2')
    
    mock_metrics.start_command.assert_called_once()
    mock_track_step.assert_called_once_with('command_test_cmd')
    mock_metrics.end_command.assert_called_once()
    mock_metrics.end_process.assert_called_once()
    mock_finalize.assert_called_once_with(mock_ctx)
    assert result == 'result'

# TEST FOR EXECUTE WITH METRICS ENABLED AND PROCESS_END IS NOT NONE
@patch('autotools.utils.commands.should_enable_metrics')
@patch('autotools.utils.commands.get_metrics')
@patch('autotools.utils.commands.track_step')
@patch('autotools.utils.commands.finalize_metrics')
def test_execute_with_metrics_enabled_process_end_not_none(mock_finalize, mock_track_step, mock_get_metrics, mock_should_enable):
    from autotools.utils.commands import _execute_with_metrics
    from contextlib import nullcontext
    
    mock_should_enable.return_value = True
    mock_callback = MagicMock(return_value='result')
    mock_ctx = MagicMock()
    mock_ctx.invoked_subcommand = 'test_cmd'
    mock_ctx.command.name = 'test_cmd'
    
    mock_metrics = MagicMock()
    mock_metrics.process_start = 123.0
    mock_metrics.process_end = 456.0
    mock_get_metrics.return_value = mock_metrics
    mock_track_step.return_value = nullcontext()
    
    result = _execute_with_metrics(mock_ctx, mock_callback, 'arg1', 'arg2')
    
    mock_metrics.start_command.assert_called_once()
    mock_track_step.assert_called_once_with('command_test_cmd')
    mock_metrics.end_command.assert_called_once()
    mock_metrics.end_process.assert_not_called()
    mock_finalize.assert_not_called()
    assert result == 'result'


# TEST FOR list-tools (PLAIN TEXT)
@patch('autotools.cli.get_wrapped_tool_commands')
def test_list_tools_plain(mock_get_wrapped, cli_runner):
    cmd_autocaps = _create_mock_command('autocaps')
    cmd_unnamed = _create_mock_command(None)
    cmd_autotest = _create_mock_command('autotest')

    mock_get_wrapped.return_value = {
        'autotest': cmd_autotest,
        'autocaps': cmd_autocaps,
        'tool_with_no_cmd_name': cmd_unnamed,
        'tool_with_no_cmd_name_2': cmd_unnamed,
    }

    result = cli_runner.invoke(cli, ['list-tools'])
    assert result.exit_code == 0

    lines = [l.strip() for l in result.output.splitlines() if l.strip()]
    assert lines == sorted(set(lines))
    assert 'autocaps' in lines
    assert 'test' in lines
    assert 'tool_with_no_cmd_name' in lines


# TEST FOR list-tools (JSON)
@patch('autotools.cli.get_wrapped_tool_commands')
def test_list_tools_json(mock_get_wrapped, cli_runner):
    cmd_autocaps = _create_mock_command('autocaps')
    cmd_autotest = _create_mock_command('autotest')

    mock_get_wrapped.return_value = {'autocaps': cmd_autocaps, 'autotest': cmd_autotest}

    result = cli_runner.invoke(cli, ['list-tools', '--json'])
    assert result.exit_code == 0

    tools = json_module.loads(result.output)
    assert tools == sorted(tools)
    assert 'autocaps' in tools
    assert 'test' in tools


# TEST FOR smoke (JSON SUCCESS)
def test_smoke_command_json_success(monkeypatch, cli_runner):
    from autotools.utils import smoke as smoke_module

    calls = {}

    def fake_run_smoke(*, workdir, timeout_s, include, exclude, verbose, platform, print_table):
        calls['args'] = {
            'workdir': workdir,
            'timeout_s': timeout_s,
            'include': include,
            'exclude': exclude,
            'verbose': verbose,
            'platform': platform,
            'print_table': print_table,
        }
        return [{'tool': 'autocaps', 'case': 'basic', 'status': 'OK'}]

    monkeypatch.setattr(smoke_module, 'run_smoke', fake_run_smoke)
    monkeypatch.setenv('PLATFORM', 'UnitTest')

    with cli_runner.isolated_filesystem():
        os.mkdir('wd')
        result = cli_runner.invoke(
            cli,
            [
                'smoke',
                '--workdir',
                'wd',
                '--timeout',
                '5',
                '--include',
                'autocaps',
                '--exclude',
                'autoip',
                '--json',
                '--verbose',
            ],
        )

    assert result.exit_code == 0
    assert json_module.loads(result.output)[0]['status'] == 'OK'

    assert calls['args']['timeout_s'] == 5
    assert calls['args']['include'] == {'autocaps'}
    assert calls['args']['exclude'] == {'autoip'}
    assert calls['args']['verbose'] is True
    assert calls['args']['platform'] == 'UnitTest'
    assert calls['args']['print_table'] is False


# TEST FOR smoke (FAILURE EXIT CODE)
def test_smoke_command_failure_exit_code(monkeypatch, cli_runner):
    from autotools.utils import smoke as smoke_module

    def fake_run_smoke(*, workdir, timeout_s, include, exclude, verbose, platform, print_table):
        return [{'tool': 'autocaps', 'case': 'basic', 'status': 'FAIL'}]

    monkeypatch.setattr(smoke_module, 'run_smoke', fake_run_smoke)
    monkeypatch.delenv('PLATFORM', raising=False)

    with cli_runner.isolated_filesystem():
        os.mkdir('wd')
        result = cli_runner.invoke(cli, ['smoke', '--workdir', 'wd', '--timeout', '1', '--quiet'])

    assert result.exit_code == 1
