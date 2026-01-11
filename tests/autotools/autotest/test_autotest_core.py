import pytest
import sys
import subprocess
from unittest.mock import patch, MagicMock, Mock, call
from click.testing import CliRunner
from autotools.autotest.commands import (
    autotest,
    _install_test_dependencies,
    _build_test_command,
    _process_test_output_line,
    _parse_coverage_line,
    _get_coverage_color,
    _display_coverage_metrics,
    _run_test_process,
    _prepare_test_environment,
    _start_test_process,
    _process_test_output,
    _handle_test_result
)

# COMMON MOCKS
@pytest.fixture 
def mock_click(): 
    with patch('autotools.autotest.commands.click') as mock: yield mock
@pytest.fixture 
def mock_sys(): 
    with patch('autotools.autotest.commands.sys') as mock: yield mock
@pytest.fixture 
def mock_subprocess(): 
    with patch('autotools.autotest.commands.subprocess') as mock: yield mock

# HELPER TO CREATE MOCK PROCESS FOR TEST OUTPUT TESTS WITH CONFIGURABLE POLL AND READLINE BEHAVIOR
def create_mock_process(poll_returns, readline_returns, wait_return=0):
    mock_process = MagicMock()
    poll_count = {'count': 0}
    readline_count = {'count': 0}
    
    def poll_side_effect():
        poll_count['count'] += 1
        if poll_count['count'] <= poll_returns: return None
        return 0
    
    def readline_side_effect():
        readline_count['count'] += 1
        if readline_count['count'] <= len(readline_returns): return readline_returns[readline_count['count'] - 1]
        return ''
    
    mock_process.poll.side_effect = poll_side_effect
    mock_process.stdout.readline.side_effect = readline_side_effect
    mock_process.wait.return_value = wait_return

    return mock_process

# TESTS FOR INSTALL TEST DEPENDENCIES
# ALREADY INSTALLED
def test_install_test_dependencies_already_installed(mock_subprocess):
    with patch('builtins.__import__', return_value=MagicMock()):
        _install_test_dependencies()
        mock_subprocess.run.assert_not_called()

# MISSING PYTEST
def test_install_test_dependencies_missing_pytest(mock_subprocess, mock_sys, mock_click):
    def import_side_effect(name, *args, **kwargs):
        if name == 'pytest': raise ImportError()
        return MagicMock()

    with patch('builtins.__import__', side_effect=import_side_effect):
        mock_subprocess.run.return_value = MagicMock(returncode=0)
        _install_test_dependencies()
        mock_subprocess.run.assert_called_once()
        mock_sys.exit.assert_not_called()

# MISSING PYTEST_COV
def test_install_test_dependencies_missing_pytest_cov(mock_subprocess, mock_sys, mock_click):
    import_count = {'count': 0}

    def import_side_effect(name, *args, **kwargs):
        import_count['count'] += 1
        if name == 'pytest': return MagicMock()
        elif name == 'pytest_cov' and import_count['count'] == 2: raise ImportError()
        return MagicMock()
    
    with patch('builtins.__import__', side_effect=import_side_effect):
        mock_subprocess.run.return_value = MagicMock(returncode=0)
        _install_test_dependencies()
        mock_subprocess.run.assert_called_once()
        mock_sys.exit.assert_not_called()

# INSTALLATION FAILURE
def test_install_test_dependencies_installation_failure(mock_sys, mock_click):
    from autotools.autotest import commands

    def import_side_effect(name, *args, **kwargs):
        if name == 'pytest': raise ImportError()
        return MagicMock()
    
    with patch('builtins.__import__', side_effect=import_side_effect):
        real_called_process_error = commands.subprocess.CalledProcessError
        with patch.object(commands.subprocess, 'run') as mock_run:
            commands.subprocess.CalledProcessError = real_called_process_error
            error = commands.subprocess.CalledProcessError(1, 'pip')
            mock_run.side_effect = error
            _install_test_dependencies()
            mock_sys.exit.assert_called_once_with(1)

# TESTS FOR BUILD TEST COMMAND
# DEFAULT
def test_build_test_command_default():
    cmd = _build_test_command(False, False, False, False, None)
    assert sys.executable in cmd
    assert '-m' in cmd
    assert 'pytest' in cmd
    assert '--cov-report=term-missing' in cmd
    assert '--cov=autotools' in cmd
    assert 'tests' in cmd

# NO COVERAGE
def test_build_test_command_no_cov():
    cmd = _build_test_command(False, False, True, False, None)
    assert '--cov-report' not in ' '.join(cmd)
    assert '--cov=' not in ' '.join(cmd)

# HTML COVERAGE
def test_build_test_command_html():
    cmd = _build_test_command(False, False, False, True, None)
    assert '--cov-report=html' in cmd
    assert '--cov=autotools' in cmd

# WITH MODULE
@pytest.mark.parametrize('unit,integration,module,expected_path,should_not_contain', [
    (True, False, 'autocaps', 'tests/autotools/autocaps/unit', []),
    (False, True, 'autocaps', 'tests/autotools/autocaps/integration', []),
    (False, False, 'autolower', 'tests/autotools/autolower', []),
    (True, True, 'autocaps', 'tests/autotools/autocaps', ['/unit', '/integration']),
])
def test_build_test_command_with_module(unit, integration, module, expected_path, should_not_contain):
    cmd = _build_test_command(unit, integration, False, False, module)
    assert expected_path in cmd[-1]
    for not_contained in should_not_contain: assert not_contained not in cmd[-1]

# NO COVERAGE AND HTML
def test_build_test_command_module_no_cov_html():
    cmd = _build_test_command(False, False, True, True, 'autolower')
    assert '--cov-report' not in ' '.join(cmd)
    assert 'tests/autotools/autolower' in cmd[-1]

# TESTS FOR PROCESS TEST OUTPUT LINE
# EMPTY LINE
@pytest.mark.parametrize('line', ['', '   ', '\n', '...   ', '. . .'])
def test_process_test_output_line_empty(line):
    assert _process_test_output_line(line) is None

# WITH CONTENT
@pytest.mark.parametrize('line,expected_content', [
    ('test_autocaps_core.py::test_basic PASSED', 'test_basic'),
    ('autotools/autocaps/tests/test_autocaps_core.py::test_basic PASSED', 'test_basic'),
    ('test_file.py::test_function PASSED', None),
    ('autotools/test.py::test_function PASSED', None),
])
def test_process_test_output_line_with_content(line, expected_content):
    result = _process_test_output_line(line)
    assert result is not None
    if expected_content: assert expected_content in result

# FORMATTTING
@pytest.mark.parametrize('line,should_not_contain', [('test...autocaps....core', '..'),('test    autocaps    core', '    ')])
def test_process_test_output_line_formatting(line, should_not_contain):
    result = _process_test_output_line(line)
    assert result is not None
    assert should_not_contain not in result

# TESTS FOR PARSE COVERAGE LINE
# VALID
@pytest.mark.parametrize('line,expected', [
    ('TOTAL    627    105    134      0  81.47%', {
        'statements': 627, 'missed': 105, 'branches': 134,
        'branch_partial': 0, 'coverage': 81.47
    }),
    ('TOTAL    100    20  80.00%', {
        'statements': 100, 'missed': 20, 'coverage': 80.00
    }),
    ('TOTAL    100    20    50  80.00%', {
        'statements': 100, 'missed': 20, 'coverage': 50.0
    }),
])
def test_parse_coverage_line_valid(line, expected):
    result = _parse_coverage_line(line)
    for key, value in expected.items():
        if isinstance(value, float): assert result[key] == pytest.approx(value)
        else: assert result[key] == value

# PERCENTAGE ONLY
@pytest.mark.parametrize('line,expected_coverage', [
    ('Some text with 85.5% coverage', 85.5),
    ('Some text with 50.5% coverage', 50.5),
    ('TOTAL    100    20    abc    def  80.00%', 80.00),
])
def test_parse_coverage_line_percentage_only(line, expected_coverage):
    result = _parse_coverage_line(line)
    assert result['coverage'] == pytest.approx(expected_coverage)

# INVALID
@pytest.mark.parametrize('line', [
    'TOTAL invalid line',
    'TOTAL',
    'TOTAL    abc    def   xyz%',
])
def test_parse_coverage_line_invalid(line):
    result = _parse_coverage_line(line)
    assert result == {} or 'coverage' in result

# TEST FOR GET COVERAGE COLOR
@pytest.mark.parametrize('percentage,expected_color', [
    (80, 'green'), (100, 'green'), (90, 'green'),
    (60, 'yellow'), (79, 'yellow'), (70, 'yellow'),
    (59, 'red'), (0, 'red'), (30, 'red'),
])
def test_get_coverage_color(percentage, expected_color):
    assert _get_coverage_color(percentage) == expected_color

# TESTS FOR DISPLAY COVERAGE METRICS
# EMPTY
def test_display_coverage_metrics_empty(mock_click):
    _display_coverage_metrics({})
    mock_click.echo.assert_not_called()

# WITH DATA
@pytest.mark.parametrize('coverage_data,expected_text', [
    ({'statements': 100, 'missed': 20, 'coverage': 80.0}, 'Statements:'),
    ({'statements': 0, 'missed': 0}, 'Statements:'),
    ({'statements': 100, 'missed': 20, 'branches': 50, 'branch_partial': 5, 'coverage': 80.0}, 'Branches:'),
    ({'coverage': 75.5}, 'Overall:'),
])
def test_display_coverage_metrics_with_data(mock_click, coverage_data, expected_text):
    _display_coverage_metrics(coverage_data)
    style_calls = [call[0][0] for call in mock_click.style.call_args_list if call[0]]
    assert any(expected_text in str(arg) for arg in style_calls)

# ZERO BRANCHES
def test_display_coverage_metrics_zero_branches(mock_click):
    coverage_data = {'statements': 100, 'missed': 20, 'branches': 0, 'coverage': 80.0}
    _display_coverage_metrics(coverage_data)
    branches_calls = [str(call) for call in mock_click.echo.call_args_list if 'Branches:' in str(call)]
    assert len(branches_calls) == 0

# TESTS FOR PREPARE TEST ENVIRONMENT AND START TEST PROCESS
# PREPARE TEST ENVIRONMENT
@patch('autotools.autotest.commands.os')
def test_prepare_test_environment(mock_os):
    mock_os.environ = {'PATH': '/usr/bin'}
    mock_os.getcwd.return_value = '/test/path'
    env = _prepare_test_environment()
    assert env['PYTHONPATH'] == '/test/path'
    assert env['FORCE_COLOR'] == '1'

# START TEST PROCESS
def test_start_test_process(mock_subprocess):
    mock_process = MagicMock()
    mock_subprocess.Popen.return_value = mock_process
    cmd = ['python', '-m', 'pytest']
    env = {'PYTHONPATH': '/test'}
    result = _start_test_process(cmd, env)
    mock_subprocess.Popen.assert_called_once()
    assert result == mock_process

# TEST FOR PROCESS TEST OUTPUT
@pytest.mark.parametrize('poll_returns,readline_returns,expected_coverage,expected_empty,should_write', [
    (1, ['TOTAL    627    105    134      0  81.47%'], 81.47, False, True),
    (1, ['test_autocaps_core.py::test_basic PASSED'], None, True, True),
    (3, ['test1 PASSED', 'test2 PASSED', 'TOTAL    100    10  90.00%'], 90.00, False, True),
    (1, ['', 'TOTAL    100    10  90.00%'], 90.00, False, True),
    (1, ['   '], None, True, False),
])
def test_process_test_output(mock_sys, poll_returns, readline_returns, expected_coverage, expected_empty, should_write):
    mock_process = create_mock_process(poll_returns, readline_returns)
    result = _process_test_output(mock_process)
    if expected_empty: assert result == {}
    else: assert result['coverage'] == pytest.approx(expected_coverage)
    if should_write: assert mock_sys.stdout.write.called

# TESTS FOR HANDLE TEST RESULT
# SUCCESS
@patch('autotools.autotest.commands._display_coverage_metrics')
def test_handle_test_result_success(mock_display, mock_click, mock_sys):
    mock_process = MagicMock()
    mock_process.returncode = 0
    coverage_data = {'coverage': 85.0}
    _handle_test_result(mock_process, coverage_data)
    assert mock_click.echo.called
    mock_display.assert_called_once_with(coverage_data)
    mock_sys.exit.assert_not_called()

# FAILURE
def test_handle_test_result_failure(mock_sys, mock_click):
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_sys.exit.side_effect = SystemExit(1)
    with pytest.raises(SystemExit): _handle_test_result(mock_process, {})
    mock_sys.exit.assert_called_once_with(1)

# TESTS FOR RUN TEST PROCESS
# SUCCESS
@patch('autotools.autotest.commands._handle_test_result')
@patch('autotools.autotest.commands._process_test_output')
@patch('autotools.autotest.commands._start_test_process')
@patch('autotools.autotest.commands._prepare_test_environment')
def test_run_test_process_success(mock_prepare, mock_start, mock_process_output, mock_handle):
    mock_env = {'PYTHONPATH': '/test'}
    mock_prepare.return_value = mock_env
    mock_process = MagicMock()
    mock_start.return_value = mock_process
    mock_process_output.return_value = {'coverage': 85.0}
    cmd = ['python', '-m', 'pytest']
    _run_test_process(cmd)
    mock_handle.assert_called_once()

# EXCEPTIONS
@pytest.mark.parametrize('exception', [subprocess.CalledProcessError(1, 'pytest'), Exception('Test error')])
@patch('autotools.autotest.commands._prepare_test_environment')
def test_run_test_process_exceptions(mock_prepare, mock_sys, mock_click, exception):
    mock_prepare.side_effect = exception
    mock_sys.exit.side_effect = SystemExit(1)
    cmd = ['python', '-m', 'pytest']
    with pytest.raises(SystemExit): _run_test_process(cmd)
    mock_sys.exit.assert_called_once_with(1)

# TEST FOR AUTOTEST COMMAND
# BASIC
@patch('autotools.autotest.commands._run_test_process')
@patch('autotools.autotest.commands._build_test_command')
@patch('autotools.autotest.commands._install_test_dependencies')
@patch('autotools.autotest.commands.check_for_updates')
def test_autotest_command_basic(mock_updates, mock_install, mock_build, mock_run):
    mock_updates.return_value = None
    mock_build.return_value = ['python', '-m', 'pytest']
    runner = CliRunner()
    result = runner.invoke(autotest)
    assert result.exit_code == 0
    mock_install.assert_called_once()
    mock_build.assert_called_once()
    mock_run.assert_called_once()

# WITH UPDATE MESSAGE
@patch('autotools.autotest.commands._run_test_process')
@patch('autotools.autotest.commands._build_test_command')
@patch('autotools.autotest.commands._install_test_dependencies')
@patch('autotools.autotest.commands.check_for_updates')
def test_autotest_command_with_update(mock_updates, mock_install, mock_build, mock_run, mock_click):
    mock_updates.return_value = 'Update available'
    mock_build.return_value = ['python', '-m', 'pytest']
    runner = CliRunner()
    result = runner.invoke(autotest)
    assert result.exit_code == 0
    mock_click.echo.assert_called()

# WITH ALL OPTIONS
@patch('autotools.autotest.commands._run_test_process')
@patch('autotools.autotest.commands._build_test_command')
@patch('autotools.autotest.commands._install_test_dependencies')
@patch('autotools.autotest.commands.check_for_updates')
def test_autotest_command_all_options(mock_updates, mock_install, mock_build, mock_run):
    mock_updates.return_value = None
    runner = CliRunner()
    result = runner.invoke(autotest, ['--unit', '--integration', '--no-cov', '--html', '--module', 'autocaps'])
    assert result.exit_code == 0
    mock_build.assert_called_once_with(True, True, True, True, 'autocaps')
