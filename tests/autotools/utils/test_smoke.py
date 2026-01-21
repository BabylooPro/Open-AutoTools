import os
import sys
import time
import pytest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
from types import ModuleType
import click

from autotools.utils.smoke import (
    _normalize_smoke_test_item,
    _normalize_smoke_tests,
    _build_default_case,
    _value_for_param,
    _run_subprocess,
    _print_summary,
    _tool_public_name,
    _should_run_tool,
    _get_smoke_tests,
    _smoke_root,
    _run_tool_smoke,
    run_smoke,
)


# FIXTURES
@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_click_command():
    def _create_cmd(name='test', **kwargs):
        return click.Command(name, callback=lambda: None, **kwargs)
    return _create_cmd


@pytest.fixture
def mock_module():
    def _create_mod(name='test_module', **attrs):
        mod = ModuleType(name)
        for k, v in attrs.items():
            setattr(mod, k, v)
        return mod
    return _create_mod

# TEST _normalize_smoke_test_item
# WITH DICT FORMAT
def test_normalize_smoke_test_item_dict():
    result = _normalize_smoke_test_item({'name': 'test1', 'args': ['arg1', 'arg2']}, 'default')
    assert result == ('test1', ['arg1', 'arg2'])

# WITH NO NAME
def test_normalize_smoke_test_item_dict_no_name():
    result = _normalize_smoke_test_item({'args': ['arg1']}, 'default')
    assert result == ('default', ['arg1'])

# WITH NO ARGS
def test_normalize_smoke_test_item_dict_no_args():
    result = _normalize_smoke_test_item({'name': 'test1'}, 'default')
    assert result == ('test1', [])

# WITH INVALID ARGS TYPE
def test_normalize_smoke_test_item_dict_invalid_args_type():
    with pytest.raises(TypeError, match="SMOKE_TESTS ITEM 'args' MUST BE A LIST"):
        _normalize_smoke_test_item({'name': 'test1', 'args': 'not-a-list'}, 'default')

# TEST _normalize_smoke_test_item
# WITH TUPLE FORMAT
def test_normalize_smoke_test_item_tuple():
    result = _normalize_smoke_test_item(('test1', ['arg1', 'arg2']), 'default')
    assert result == ('test1', ['arg1', 'arg2'])

# WITH NON-STRING FIRST ITEM
def test_normalize_smoke_test_item_tuple_non_string_first():
    with pytest.raises(TypeError):
        _normalize_smoke_test_item((123, ['arg1']), 'default')

# WITH WRONG LENGTH
def test_normalize_smoke_test_item_tuple_wrong_length():
    with pytest.raises(TypeError):
        _normalize_smoke_test_item(('test1', 'arg1', 'extra'), 'default')

# WITH NO NAME
def test_normalize_smoke_test_item_tuple_no_name():
    result = _normalize_smoke_test_item(('', ['arg1']), 'default')
    assert result == ('default', ['arg1'])

# WITH INVALID ARGS TYPE
def test_normalize_smoke_test_item_tuple_invalid_args_type():
    with pytest.raises(TypeError, match="SMOKE_TESTS TUPLE SECOND ITEM MUST BE A LIST"):
        _normalize_smoke_test_item(('test1', 'not-a-list'), 'default')

# WITH NO ARGS
def test_normalize_smoke_test_item_tuple_no_args():
    result = _normalize_smoke_test_item(('test1', None), 'default')
    assert result == ('test1', [])

# TEST _normalize_smoke_test_item
def test_normalize_smoke_test_item_list():
    result = _normalize_smoke_test_item(['arg1', 'arg2', 'arg3'], 'default')
    assert result == ('default', ['arg1', 'arg2', 'arg3'])

# WITH EMPTY LIST
def test_normalize_smoke_test_item_list_empty():
    result = _normalize_smoke_test_item([], 'default')
    assert result == ('default', [])

# WITH NON-STRING ITEMS
def test_normalize_smoke_test_item_list_non_string():
    result = _normalize_smoke_test_item([123, 456], 'default')
    assert result == ('default', ['123', '456'])

# WITH INVALID TYPE
def test_normalize_smoke_test_item_invalid_type():
    with pytest.raises(TypeError, match="SMOKE_TESTS ITEMS MUST BE dict OR"):
        _normalize_smoke_test_item(123, 'default')

# TEST _normalize_smoke_tests
# WITH EMPTY VALUE
def test_normalize_smoke_tests_empty():
    result = _normalize_smoke_tests(None)
    assert result == []

# WITH EMPTY LIST
def test_normalize_smoke_tests_empty_list():
    result = _normalize_smoke_tests([])
    assert result == []

# WITH LIST OF DICTS
def test_normalize_smoke_tests_list_of_dicts():
    result = _normalize_smoke_tests([
        {'name': 'test1', 'args': ['arg1']},
        {'name': 'test2', 'args': ['arg2']}
    ])
    assert len(result) == 2
    assert result[0] == ('test1', ['arg1'])
    assert result[1] == ('test2', ['arg2'])

# WITH LIST OF TUPLES
def test_normalize_smoke_tests_list_of_tuples():
    result = _normalize_smoke_tests([
        ('test1', ['arg1']),
        ('test2', ['arg2'])
    ])
    assert len(result) == 2
    assert result[0] == ('test1', ['arg1'])
    assert result[1] == ('test2', ['arg2'])

# WITH LIST OF LISTS
def test_normalize_smoke_tests_list_of_lists():
    result = _normalize_smoke_tests([['arg1'], ['arg2']])
    assert len(result) == 2
    assert result[0] == ('case1', ['arg1'])
    assert result[1] == ('case2', ['arg2'])

# WITH INVALID TYPE
def test_normalize_smoke_tests_invalid_type():
    with pytest.raises(TypeError, match="SMOKE_TESTS MUST BE A LIST"):
        _normalize_smoke_tests("not-a-list")

# TEST _build_default_case
# WITH AUTOCAPSCOLOR
def test_build_default_case_autocolor(temp_dir, mock_click_command):
    cmd = mock_click_command('autocolor')
    result = _build_default_case('autocolor', cmd, temp_dir)
    assert result == ('basic', ['#FF5733'])

# WITH AUTOCONVERT
def test_build_default_case_autoconvert(temp_dir, mock_click_command):
    cmd = mock_click_command('autoconvert')
    result = _build_default_case('autoconvert', cmd, temp_dir)
    assert result[0] == 'txt-json'
    assert len(result[1]) == 2
    assert Path(result[1][0]).exists()
    assert result[1][1].endswith('.json')

# WITH REQUIRED OPTIONS
def test_build_default_case_with_required_options(temp_dir, mock_click_command):
    cmd = mock_click_command('test')
    opt = click.Option(['--required'], required=True)
    cmd.params.append(opt)
    result = _build_default_case('test', cmd, temp_dir)
    assert result[0] == 'default'
    assert '--required' in result[1]

# WITH REQUIRED FLAG
def test_build_default_case_with_required_flag(temp_dir, mock_click_command):
    cmd = mock_click_command('test')
    opt = click.Option(['--flag'], is_flag=True, required=True)
    cmd.params.append(opt)
    result = _build_default_case('test', cmd, temp_dir)
    assert result[0] == 'default'
    assert '--flag' in result[1]

# WITH ARGUMENTS
def test_build_default_case_with_arguments(temp_dir, mock_click_command):
    cmd = mock_click_command('test')
    arg = click.Argument(['input'])
    cmd.params.append(arg)
    result = _build_default_case('test', cmd, temp_dir)
    assert result[0] == 'default'
    assert len(result[1]) >= 1

# WITH MULTIPLE ARGUMENTS
def test_build_default_case_with_multiple_arguments(temp_dir, mock_click_command):
    cmd = mock_click_command('test')
    arg = click.Argument(['input'], nargs=3)
    cmd.params.append(arg)
    result = _build_default_case('test', cmd, temp_dir)
    assert result[0] == 'default'
    assert len(result[1]) >= 3

# WITH NARGS NOT INT
def test_build_default_case_with_nargs_not_int(temp_dir, mock_click_command):
    cmd = mock_click_command('test')
    arg = Mock(spec=click.Argument)
    arg.nargs = '?'
    arg.__class__ = click.Argument

    with patch('autotools.utils.smoke._value_for_param', return_value='test_value'):
        cmd.params.append(arg)
        result = _build_default_case('test', cmd, temp_dir)
        assert result[0] == 'default'
        assert len(result[1]) >= 1

# WITH NO PARAMS
def test_build_default_case_no_params(temp_dir, mock_click_command):
    cmd = mock_click_command('test')
    result = _build_default_case('test', cmd, temp_dir)
    assert result[0] == 'default'
    assert isinstance(result[1], list)

# TEST _value_for_param
# WITH COLOR
def test_value_for_param_color(temp_dir):
    param = click.Option(['--color'])
    result = _value_for_param(param, temp_dir)
    assert result == '#FF5733'

# WITH INPUT PATH
def test_value_for_param_input_path(temp_dir):
    param = click.Option(['--input'])
    result = _value_for_param(param, temp_dir)
    assert Path(result).exists()
    assert result.endswith('.txt')

# WITH OUTPUT PATH
def test_value_for_param_output_path(temp_dir):
    param = click.Option(['--output'])
    result = _value_for_param(param, temp_dir)
    assert result.endswith('.zip')

# WITH ZIP PATH
def test_value_for_param_zip_path(temp_dir):
    param = click.Option(['--archive'])
    result = _value_for_param(param, temp_dir)
    assert result.endswith('.zip')

# WITH CLICK PATH
def test_value_for_param_click_path(temp_dir):
    param = click.Option(['--file'], type=click.Path())
    result = _value_for_param(param, temp_dir)
    assert Path(result).parent.exists()

# WITH CHOICE
def test_value_for_param_choice(temp_dir):
    param = click.Option(['--format'], type=click.Choice(['a', 'b', 'c']))
    result = _value_for_param(param, temp_dir)
    assert result in ['a', 'b', 'c']

# WITH DEFAULT
def test_value_for_param_default(temp_dir):
    param = click.Option(['--test'])
    result = _value_for_param(param, temp_dir)
    assert result == 'test'

# WITH SOURCE PATH
def test_value_for_param_source_path(temp_dir):
    param = click.Option(['--source'])
    result = _value_for_param(param, temp_dir)
    assert Path(result).exists()
    assert result.endswith('.txt')

# WITH FILE PATH
def test_value_for_param_file_path(temp_dir):
    param = click.Option(['--file'])
    result = _value_for_param(param, temp_dir)
    assert Path(result).parent.exists()

# WITH DIR PATH
def test_value_for_param_dir_path(temp_dir):
    param = click.Option(['--dir'])
    result = _value_for_param(param, temp_dir)
    assert Path(result).parent.exists()

# WITH FOLDER PATH
def test_value_for_param_folder_path(temp_dir):
    param = click.Option(['--folder'])
    result = _value_for_param(param, temp_dir)
    assert Path(result).parent.exists()

# WITH NO NAME
def test_value_for_param_no_name(temp_dir):
    param = click.Option(['--test'])
    result = _value_for_param(param, temp_dir)
    assert result == 'test'

# WITH EMPTY CHOICE
def test_value_for_param_choice_empty(temp_dir):
    param = click.Option(['--format'], type=click.Choice([]))
    result = _value_for_param(param, temp_dir)
    assert result == 'test'  # FALLBACK TO DEFAULT

# WITH NO TYPE
def test_value_for_param_no_type(temp_dir):
    param = click.Option(['--test'])
    if hasattr(param, 'type'): delattr(param, 'type')
    result = _value_for_param(param, temp_dir)
    assert result == 'test'

# TEST _run_subprocess
# WITH SUCCESS
def test_run_subprocess_success():
    argv = [sys.executable, '-c', 'print("test")']
    status, rc, duration, output = _run_subprocess(argv, timeout_s=10, verbose=False)
    assert status == 'OK'
    assert rc == 0
    assert duration > 0
    assert 'test' in output

# WITH FAILURE
def test_run_subprocess_failure():
    argv = [sys.executable, '-c', 'import sys; sys.exit(1)']
    status, rc, duration, _ = _run_subprocess(argv, timeout_s=10, verbose=False)
    assert status == 'X'
    assert rc == 1
    assert duration > 0

# WITH VERBOSE SUCCESS
@patch('autotools.utils.smoke.click.echo')
def test_run_subprocess_verbose_success(mock_echo):
    argv = [sys.executable, '-c', 'print("test")']
    status, _, _, _ = _run_subprocess(argv, timeout_s=10, verbose=True)
    assert status == 'OK'
    assert mock_echo.called

# WITH TIMEOUT
@patch('autotools.utils.smoke.click.echo')
def test_run_subprocess_timeout(mock_echo):
    argv = [sys.executable, '-c', 'import time; time.sleep(2)']
    status, rc, duration, _ = _run_subprocess(argv, timeout_s=1, verbose=False)
    assert status == 'TIMEOUT'
    assert rc == 124
    assert duration >= 1

# WITH VERBOSE TIMEOUT
@patch('autotools.utils.smoke.click.echo')
def test_run_subprocess_timeout_verbose(mock_echo):
    argv = [sys.executable, '-c', 'import time; time.sleep(2)']
    status, _, _, _ = _run_subprocess(argv, timeout_s=1, verbose=True)
    assert status == 'TIMEOUT'
    assert mock_echo.called

# WITH VERBOSE EMPTY OUTPUT
@patch('autotools.utils.smoke.click.echo')
def test_run_subprocess_verbose_empty_output(mock_echo):
    argv = [sys.executable, '-c', '']
    status, _, _, _ = _run_subprocess(argv, timeout_s=10, verbose=True)
    assert status == 'OK'

# WITH TIMEOUT NO STDOUT ATTR
@patch('autotools.utils.smoke.subprocess.run')
@patch('autotools.utils.smoke.click.echo')
def test_run_subprocess_timeout_no_stdout_attr(mock_echo, mock_run):
    mock_run.side_effect = subprocess.TimeoutExpired(['test'], 1)
    argv = [sys.executable, '-c', 'test']
    status, rc, _, _ = _run_subprocess(argv, timeout_s=1, verbose=False)
    assert status == 'TIMEOUT'
    assert rc == 124

# WITH PERMISSION ERROR (TREATED AS FAILURE)
@patch('autotools.utils.smoke.time.perf_counter')
@patch('autotools.utils.smoke.subprocess.run')
@patch('autotools.utils.smoke.click.echo')
def test_run_subprocess_permission_error_verbose(mock_echo, mock_run, mock_perf_counter):
    mock_perf_counter.side_effect = [0.0, 0.5]
    mock_run.side_effect = PermissionError("Denied")

    argv = [sys.executable, '-c', 'print("test")']
    status, rc, duration, output = _run_subprocess(argv, timeout_s=10, verbose=True)
    assert status == 'X'
    assert rc == 126
    assert duration == pytest.approx(0.5)
    assert "Denied" in output

    calls = [str(call) for call in mock_echo.call_args_list]
    assert any("PERMISSION ERROR" in c for c in calls)

# WITH PERMISSION ERROR (QUIET MODE)
@patch('autotools.utils.smoke.time.perf_counter')
@patch('autotools.utils.smoke.subprocess.run')
@patch('autotools.utils.smoke.click.echo')
def test_run_subprocess_permission_error_quiet(mock_echo, mock_run, mock_perf_counter):
    mock_perf_counter.side_effect = [0.0, 0.5]
    mock_run.side_effect = PermissionError("Denied")

    argv = [sys.executable, '-c', 'print("test")']
    status, rc, duration, output = _run_subprocess(argv, timeout_s=10, verbose=False)
    assert status == 'X'
    assert rc == 126
    assert duration == pytest.approx(0.5)
    assert "Denied" in output
    assert not mock_echo.called

# WITH PERMISSION ERROR (TREATED AS TIMEOUT)
@patch('autotools.utils.smoke.time.perf_counter')
@patch('autotools.utils.smoke.subprocess.run')
@patch('autotools.utils.smoke.click.echo')
def test_run_subprocess_permission_error_timeout(mock_echo, mock_run, mock_perf_counter):
    mock_perf_counter.side_effect = [0.0, 2.0]
    mock_run.side_effect = PermissionError("Denied")

    argv = [sys.executable, '-c', 'print("test")']
    status, rc, duration, output = _run_subprocess(argv, timeout_s=1, verbose=True)
    assert status == 'TIMEOUT'
    assert rc == 124
    assert duration == pytest.approx(2.0)
    assert output == ''

    calls = [str(call) for call in mock_echo.call_args_list]
    assert any("TIMEOUT" in c for c in calls)

# TEST _print_summary
# WITH SUCCESS AND FAILURE
@patch('autotools.utils.smoke.click.echo')
def test_print_summary(mock_echo):
    results = [
        {'category': 'Text', 'tool': 'autocaps', 'case': 'basic', 'status': 'OK'},
        {'category': 'Network', 'tool': 'autoip', 'case': 'test', 'status': 'X'},
    ]
    _print_summary(results, 'Test Platform')
    assert mock_echo.called
    calls = [str(call) for call in mock_echo.call_args_list]
    assert any('Test Platform' in str(call) for call in calls)

# WITH EMPTY RESULTS
@patch('autotools.utils.smoke.click.echo')
def test_print_summary_empty_results(mock_echo):
    _print_summary([], 'Test Platform')
    assert mock_echo.called

# WITH MISSING FIELDS
@patch('autotools.utils.smoke.click.echo')
def test_print_summary_missing_fields(mock_echo):
    results = [
        {'tool': 'autocaps'},  # MISSING CATEGORY, CASE, STATUS
    ]
    _print_summary(results, 'Test Platform')
    assert mock_echo.called

# TEST _tool_public_name
# WITH AUTOTEST
def test_tool_public_name_autotest():
    assert _tool_public_name('autotest') == 'test'

# WITH OTHER
def test_tool_public_name_other():
    assert _tool_public_name('autocaps') == 'autocaps'
    assert _tool_public_name('autocolor') == 'autocolor'

# TEST _should_run_tool
# WITH NO FILTERS
def test_should_run_tool_no_filters():
    assert _should_run_tool('autocaps', 'autocaps', set(), set()) is True

# WITH INCLUDE MATCH TOOL NAME
def test_should_run_tool_include_match_tool_name():
    assert _should_run_tool('autocaps', 'autocaps', {'autocaps'}, set()) is True

# WITH INCLUDE MATCH PUBLIC NAME
def test_should_run_tool_include_match_public_name():
    assert _should_run_tool('autotest', 'test', {'test'}, set()) is True

# WITH INCLUDE NO MATCH
def test_should_run_tool_include_no_match():
    assert _should_run_tool('autocaps', 'autocaps', {'autocolor'}, set()) is False

# WITH EXCLUDE TOOL NAME
def test_should_run_tool_exclude_tool_name():
    assert _should_run_tool('autocaps', 'autocaps', set(), {'autocaps'}) is False

# WITH EXCLUDE PUBLIC NAME
def test_should_run_tool_exclude_public_name():
    assert _should_run_tool('autotest', 'test', set(), {'test'}) is False

# WITH INCLUDE AND EXCLUDE
def test_should_run_tool_include_and_exclude():
    assert _should_run_tool('autocaps', 'autocaps', {'autocaps'}, {'autocaps'}) is False

# TEST _get_smoke_tests
# WITH FROM MODULE
def test_get_smoke_tests_from_module(temp_dir, mock_click_command, mock_module):
    mod = mock_module('test_module', SMOKE_TESTS=[{'name': 'test1', 'args': ['arg1']}])
    cmd = mock_click_command('test')
    result = _get_smoke_tests(mod, 'test', cmd, temp_dir)
    assert len(result) == 1
    assert result[0] == ('test1', ['arg1'])

# WITH DEFAULT
def test_get_smoke_tests_default(temp_dir, mock_click_command, mock_module):
    mod = mock_module('test_module')
    cmd = mock_click_command('test')
    result = _get_smoke_tests(mod, 'autocolor', cmd, temp_dir)
    assert len(result) == 1
    assert result[0][0] == 'basic'

# WITH EMPTY LIST
def test_get_smoke_tests_empty_list(temp_dir, mock_click_command, mock_module):
    mod = mock_module('test_module', SMOKE_TESTS=[])
    cmd = mock_click_command('test')
    result = _get_smoke_tests(mod, 'autocolor', cmd, temp_dir)
    assert len(result) == 1  # FALLBACK TO DEFAULT
    assert result[0][0] == 'basic'

# TEST _smoke_root
# WITH WORKDIR
def test_smoke_root_with_workdir(temp_dir):
    with _smoke_root(str(temp_dir)) as root:
        assert isinstance(root, Path)
        assert root.exists()
        assert str(root) == str(temp_dir)

# WITH TEMP DIR
def test_smoke_root_temp_dir():
    with _smoke_root(None) as root:
        assert isinstance(root, Path)
        assert root.exists()
        assert 'autotools_smoke_' in str(root)
    assert not root.exists()

# TEST _run_tool_smoke
# WITH SUCCESS
@patch('autotools.utils.smoke._run_subprocess')
def test_run_tool_smoke_success(mock_run):
    mock_run.return_value = ('OK', 0, 1.0, 'output')
    smoke_tests = [('test1', ['arg1']), ('test2', ['arg2'])]
    results = _run_tool_smoke('autocaps', 'autocaps', smoke_tests, timeout_s=10, verbose=False)
    assert len(results) == 2
    assert results[0]['status'] == 'OK'
    assert results[0]['tool'] == 'autocaps'
    assert results[0]['case'] == 'test1'

# WITH FAILURE
@patch('autotools.utils.smoke._run_subprocess')
def test_run_tool_smoke_failure(mock_run):
    mock_run.return_value = ('X', 1, 1.0, 'error')
    smoke_tests = [('test1', ['arg1'])]
    results = _run_tool_smoke('autocaps', 'autocaps', smoke_tests, timeout_s=10, verbose=False)
    assert len(results) == 1
    assert results[0]['status'] == 'X'
    assert results[0]['returncode'] == 1

# WITH TIMEOUT
@patch('autotools.utils.smoke._run_subprocess')
def test_run_tool_smoke_timeout(mock_run):
    mock_run.return_value = ('TIMEOUT', 124, 1.0, '')
    smoke_tests = [('test1', ['arg1'])]
    results = _run_tool_smoke('autocaps', 'autocaps', smoke_tests, timeout_s=10, verbose=False)
    assert len(results) == 1
    assert results[0]['status'] == 'X'  # TIMEOUT IS CONVERTED TO 'X'

# WITH VERBOSE OUTPUT
@patch('autotools.utils.smoke._run_subprocess')
def test_run_tool_smoke_verbose_output(mock_run):
    mock_run.return_value = ('OK', 0, 1.0, 'test output')
    smoke_tests = [('test1', ['arg1'])]
    results = _run_tool_smoke('autocaps', 'autocaps', smoke_tests, timeout_s=10, verbose=True)
    assert len(results) == 1
    assert results[0]['output'] == 'test output'

# WITH FAILURE OUTPUT
@patch('autotools.utils.smoke._run_subprocess')
def test_run_tool_smoke_failure_output(mock_run):
    mock_run.return_value = ('X', 1, 1.0, 'error output')
    smoke_tests = [('test1', ['arg1'])]
    results = _run_tool_smoke('autocaps', 'autocaps', smoke_tests, timeout_s=10, verbose=False)
    assert len(results) == 1
    assert results[0]['output'] == 'error output'  # OUTPUT INCLUDED FOR FAILURES

# WITH SUCCESS NO OUTPUT WHEN NOT VERBOSE
@patch('autotools.utils.smoke._run_subprocess')
def test_run_tool_smoke_success_no_output_when_not_verbose(mock_run):
    mock_run.return_value = ('OK', 0, 1.0, 'test output')
    smoke_tests = [('test1', ['arg1'])]
    results = _run_tool_smoke('autocaps', 'autocaps', smoke_tests, timeout_s=10, verbose=False)
    assert len(results) == 1
    assert results[0]['output'] == ''  # NO OUTPUT FOR SUCCESS WHEN NOT VERBOSE

# TEST run_smoke
# WITH BASIC
@patch('autotools.utils.smoke.discover_tool_command_entries')
@patch('autotools.utils.smoke._print_summary')
@patch('autotools.utils.smoke._run_tool_smoke')
def test_run_smoke_basic(mock_run_tool, mock_print, mock_discover, temp_dir, mock_click_command, mock_module):
    mod = mock_module('test')
    cmd = mock_click_command('autocaps')
    mock_discover.return_value = {'autocaps': (mod, cmd)}
    mock_run_tool.return_value = [{'status': 'OK', 'tool': 'autocaps', 'case': 'basic'}]
    
    results = run_smoke(
        workdir=str(temp_dir),
        timeout_s=10,
        include=set(),
        exclude=set(),
        verbose=False,
        platform='Test',
        print_table=True
    )
    assert len(results) == 1
    assert mock_print.called

# WITH NO TABLE
@patch('autotools.utils.smoke.discover_tool_command_entries')
@patch('autotools.utils.smoke._print_summary')
@patch('autotools.utils.smoke._run_tool_smoke')
def test_run_smoke_no_table(mock_run_tool, mock_print, mock_discover, temp_dir, mock_click_command, mock_module):
    mod = mock_module('test')
    cmd = mock_click_command('autocaps')
    mock_discover.return_value = {'autocaps': (mod, cmd)}
    mock_run_tool.return_value = [{'status': 'OK'}]
    
    run_smoke(
        workdir=str(temp_dir),
        timeout_s=10,
        include=set(),
        exclude=set(),
        verbose=False,
        platform='Test',
        print_table=False
    )
    assert not mock_print.called

# WITH EXCLUDE AUTOTEST
@patch('autotools.utils.smoke.discover_tool_command_entries')
@patch('autotools.utils.smoke._print_summary')
@patch('autotools.utils.smoke._run_tool_smoke')
def test_run_smoke_exclude_autotest(mock_run_tool, mock_print, mock_discover, temp_dir, mock_click_command, mock_module):
    mod = mock_module('test')
    cmd_autotest = mock_click_command('autotest')
    cmd_autocaps = mock_click_command('autocaps')
    mock_discover.return_value = {'autotest': (mod, cmd_autotest), 'autocaps': (mod, cmd_autocaps)}
    mock_run_tool.return_value = [{'status': 'OK'}]
    
    run_smoke(
        workdir=str(temp_dir),
        timeout_s=10,
        include=set(),
        exclude=set(),
        verbose=False,
        platform='Test',
        print_table=False
    )
    # AUTOTEST SHOULD BE EXCLUDED BY DEFAULT
    assert mock_run_tool.call_count == 1

# WITH INCLUDE AUTOTEST
@patch('autotools.utils.smoke.discover_tool_command_entries')
@patch('autotools.utils.smoke._print_summary')
@patch('autotools.utils.smoke._run_tool_smoke')
def test_run_smoke_include_autotest(mock_run_tool, mock_print, mock_discover, temp_dir, mock_click_command, mock_module):
    mod = mock_module('test')
    cmd = mock_click_command('autotest')
    mock_discover.return_value = {'autotest': (mod, cmd)}
    mock_run_tool.return_value = [{'status': 'OK'}]
    
    run_smoke(
        workdir=str(temp_dir),
        timeout_s=10,
        include={'test'},
        exclude=set(),
        verbose=False,
        platform='Test',
        print_table=False
    )
    # AUTOTEST SHOULD BE INCLUDED IF EXPLICITLY REQUESTED
    assert mock_run_tool.called

# WITH INCLUDE FILTER
@patch('autotools.utils.smoke.discover_tool_command_entries')
@patch('autotools.utils.smoke._print_summary')
@patch('autotools.utils.smoke._run_tool_smoke')
def test_run_smoke_include_filter(mock_run_tool, mock_print, mock_discover, temp_dir, mock_click_command, mock_module):
    mod = mock_module('test')
    mock_discover.return_value = {
        'autocaps': (mod, mock_click_command('autocaps')),
        'autocolor': (mod, mock_click_command('autocolor'))
    }
    mock_run_tool.return_value = [{'status': 'OK'}]
    
    run_smoke(
        workdir=str(temp_dir),
        timeout_s=10,
        include={'autocaps'},
        exclude=set(),
        verbose=False,
        platform='Test',
        print_table=False
    )
    assert mock_run_tool.call_count == 1

# WITH EXCLUDE FILTER
@patch('autotools.utils.smoke.discover_tool_command_entries')
@patch('autotools.utils.smoke._print_summary')
@patch('autotools.utils.smoke._run_tool_smoke')
def test_run_smoke_exclude_filter(mock_run_tool, mock_print, mock_discover, temp_dir, mock_click_command, mock_module):
    mod = mock_module('test')
    mock_discover.return_value = {
        'autocaps': (mod, mock_click_command('autocaps')),
        'autocolor': (mod, mock_click_command('autocolor'))
    }
    mock_run_tool.return_value = [{'status': 'OK'}]
    
    run_smoke(
        workdir=str(temp_dir),
        timeout_s=10,
        include=set(),
        exclude={'autocolor'},
        verbose=False,
        platform='Test',
        print_table=False
    )
    assert mock_run_tool.call_count == 1

# WITH NO WORKDIR
@patch('autotools.utils.smoke.discover_tool_command_entries')
@patch('autotools.utils.smoke._print_summary')
@patch('autotools.utils.smoke._run_tool_smoke')
def test_run_smoke_no_workdir(mock_run_tool, mock_print, mock_discover, mock_click_command, mock_module):
    mod = mock_module('test')
    cmd = mock_click_command('autocaps')
    mock_discover.return_value = {'autocaps': (mod, cmd)}
    mock_run_tool.return_value = [{'status': 'OK'}]
    
    results = run_smoke(
        workdir=None,
        timeout_s=10,
        include=set(),
        exclude=set(),
        verbose=False,
        platform='Test',
        print_table=False
    )
    assert len(results) == 1

# WITH CREATES TOOL DIR
@patch('autotools.utils.smoke.discover_tool_command_entries')
@patch('autotools.utils.smoke._print_summary')
@patch('autotools.utils.smoke._run_tool_smoke')
@patch('autotools.utils.smoke.time.time')
def test_run_smoke_creates_tool_dir(mock_time, mock_run_tool, mock_print, mock_discover, temp_dir, mock_click_command, mock_module):
    mock_time.return_value = 1234567890
    mod = mock_module('test')
    cmd = mock_click_command('autocaps')
    mock_discover.return_value = {'autocaps': (mod, cmd)}
    mock_run_tool.return_value = [{'status': 'OK'}]
    
    run_smoke(
        workdir=str(temp_dir),
        timeout_s=10,
        include=set(),
        exclude=set(),
        verbose=False,
        platform='Test',
        print_table=False
    )

# WITH INCLUDE AUTOTEST BY NAME
@patch('autotools.utils.smoke.discover_tool_command_entries')
@patch('autotools.utils.smoke._print_summary')
@patch('autotools.utils.smoke._run_tool_smoke')
def test_run_smoke_include_autotest_by_name(mock_run_tool, mock_print, mock_discover, temp_dir, mock_click_command, mock_module):
    mod = mock_module('test')
    cmd = mock_click_command('autotest')
    mock_discover.return_value = {'autotest': (mod, cmd)}
    mock_run_tool.return_value = [{'status': 'OK'}]
    
    run_smoke(
        workdir=str(temp_dir),
        timeout_s=10,
        include={'autotest'},
        exclude=set(),
        verbose=False,
        platform='Test',
        print_table=False
    )
    assert mock_run_tool.called
