import click
import pytest
import autotools.utils.commands as commands_module
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock


# FIXTURES
@pytest.fixture
def mock_module():
    def _create_mod(name='autotools.foo.commands', **attrs):
        mod = ModuleType(name)
        for k, v in attrs.items():
            setattr(mod, k, v)
        return mod
    return _create_mod


@pytest.fixture
def mock_click_command():
    def _create_cmd(name='test', callback=None):
        return click.Command(name, callback=callback or (lambda: None))
    return _create_cmd


# HELPERS
def _setup_discover_mocks(monkeypatch, tool_packages, import_func):
    monkeypatch.setattr(commands_module, '_iter_tool_packages', lambda: tool_packages)
    monkeypatch.setattr(commands_module, '_import_tool_commands_module', import_func)


# TEST FOR ITER TOOL PACKAGES (FILTERS)
def test_iter_tool_packages_filters(monkeypatch):
    infos = [
        SimpleNamespace(ispkg=False, name='not_a_pkg'),
        SimpleNamespace(ispkg=True, name='_private'),
        SimpleNamespace(ispkg=True, name='__pycache__'),
        SimpleNamespace(ispkg=True, name='utils'),
        SimpleNamespace(ispkg=True, name='cli'),
        SimpleNamespace(ispkg=True, name='autocaps'),
    ]

    monkeypatch.setattr(commands_module.pkgutil, 'iter_modules', lambda _path: infos)
    assert list(commands_module._iter_tool_packages()) == ['autocaps']

# TEST FOR IMPORT TOOL COMMANDS MODULE (MISSING)
def test_import_tool_commands_module_missing_returns_none(monkeypatch):
    def fake_import_module(full_name):
        err = ModuleNotFoundError('MISSING')
        err.name = full_name
        raise err

    monkeypatch.setattr(commands_module.importlib, 'import_module', fake_import_module)

    assert commands_module._import_tool_commands_module('fake_tool') is None

# TEST FOR IMPORT TOOL COMMANDS MODULE (RERAISES OTHER MISSING)
def test_import_tool_commands_module_reraises_other_missing(monkeypatch):
    def fake_import_module(_full_name):
        err = ModuleNotFoundError('MISSING DEP')
        err.name = 'some_other_dep'
        raise err

    monkeypatch.setattr(commands_module.importlib, 'import_module', fake_import_module)

    with pytest.raises(ModuleNotFoundError):
        commands_module._import_tool_commands_module('fake_tool')

# TEST FOR DISCOVER TOOL COMMAND ENTRIES (SKIPS MISSING MODULE)
def test_discover_tool_command_entries_skips_missing_module(monkeypatch):
    _setup_discover_mocks(monkeypatch, ['fake_tool'], lambda _tool: None)
    assert commands_module.discover_tool_command_entries() == {}

# TEST FOR DISCOVER TOOL COMMAND ENTRIES (SKIPS MODULE WITHOUT CLICK COMMANDS)
def test_discover_tool_command_entries_skips_module_without_click_commands(monkeypatch, mock_module):
    mod = mock_module('autotools.fake_tool.commands', NOT_A_COMMAND=123)
    _setup_discover_mocks(monkeypatch, ['fake_tool'], lambda _tool: mod)
    assert commands_module.discover_tool_command_entries() == {}

# TEST FOR DISCOVER TOOL COMMAND ENTRIES (SELECTS NAMED COMMAND)
def test_discover_tool_command_entries_selects_named_command(monkeypatch, mock_module, mock_click_command):
    mod = mock_module('autotools.foo.commands', NOT_A_COMMAND=123)
    mod.other = mock_click_command('other')
    mod.foo = mock_click_command('foo')
    _setup_discover_mocks(monkeypatch, ['foo'], lambda _tool: mod)

    entries = commands_module.discover_tool_command_entries()
    assert entries['foo'][0] is mod
    assert entries['foo'][1].name == 'foo'

# TEST FOR DISCOVER TOOL COMMAND ENTRIES (SELECTS SINGLE COMMAND)
def test_discover_tool_command_entries_selects_single_command(monkeypatch, mock_module, mock_click_command):
    mod = mock_module('autotools.foo.commands')
    mod.only = mock_click_command('other')
    _setup_discover_mocks(monkeypatch, ['foo'], lambda _tool: mod)

    entries = commands_module.discover_tool_command_entries()
    assert entries['foo'][1].name == 'other'

# TEST FOR DISCOVER TOOL COMMAND ENTRIES (MULTIPLE COMMANDS RAISES)
def test_discover_tool_command_entries_multiple_commands_raises(monkeypatch, mock_module, mock_click_command):
    mod = mock_module('autotools.foo.commands')
    mod.a = mock_click_command('a')
    mod.b = mock_click_command('b')
    _setup_discover_mocks(monkeypatch, ['foo'], lambda _tool: mod)

    with pytest.raises(RuntimeError, match=r'MULTIPLE CLICK COMMANDS FOUND IN autotools\.foo\.commands: a, b'):
        commands_module.discover_tool_command_entries()

# TEST FOR WRAP COMMAND WITH METRICS (IS IDEMPOTENT)
def test_wrap_command_with_metrics_is_idempotent(mock_click_command):
    cmd = mock_click_command('test_cmd')
    cmd._autotools_metrics_wrapped = True
    assert commands_module._wrap_command_with_metrics(cmd) is cmd

# TEST FOR REGISTER COMMANDS (MAPS AUTOTEST TO TEST)
def test_register_commands_maps_autotest_to_test(monkeypatch, mock_click_command):
    cmd_autotest = mock_click_command('autotest')
    cmd_autocaps = mock_click_command('autocaps')

    monkeypatch.setattr(commands_module, 'get_wrapped_tool_commands', lambda: {'autocaps': cmd_autocaps, 'autotest': cmd_autotest})
    group = MagicMock()
    commands_module.register_commands(group)

    group.add_command.assert_any_call(cmd_autotest, name='test')
    group.add_command.assert_any_call(cmd_autocaps)
