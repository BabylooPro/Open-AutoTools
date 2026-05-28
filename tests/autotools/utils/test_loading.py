import sys
import threading
import types
from types import SimpleNamespace

import autotools.utils.loading as loading


# TEST FOR THREAD DAEMON PATCH HELPER
def test_patched_set_daemon_sets_daemon_flag():
    thread_like = SimpleNamespace(daemon=False)
    loading._patched_set_daemon(thread_like, True)
    assert thread_like.daemon is True


# TEST FOR SPINNER VISIBILITY WITH DUMB TERMINAL
def test_should_show_spinner_false_for_dumb_terminal(monkeypatch):
    monkeypatch.delenv('CI', raising=False)
    monkeypatch.delenv('PYTEST_CURRENT_TEST', raising=False)
    monkeypatch.setenv('TERM', 'dumb')
    assert loading._should_show_spinner() is False


# TEST FOR SPINNER VISIBILITY WITH TTY
def test_should_show_spinner_uses_stderr_tty(monkeypatch):
    monkeypatch.delenv('CI', raising=False)
    monkeypatch.delenv('PYTEST_CURRENT_TEST', raising=False)
    monkeypatch.setenv('TERM', 'xterm')
    monkeypatch.setattr(sys, 'stderr', SimpleNamespace(isatty=lambda: True))
    assert loading._should_show_spinner() is True


# TEST FOR SPINNER VISIBILITY WITHOUT TTY
def test_should_show_spinner_false_without_tty(monkeypatch):
    monkeypatch.delenv('CI', raising=False)
    monkeypatch.delenv('PYTEST_CURRENT_TEST', raising=False)
    monkeypatch.setenv('TERM', 'xterm')
    monkeypatch.setattr(sys, 'stderr', SimpleNamespace(isatty=lambda: False))
    assert loading._should_show_spinner() is False


# TEST FOR SPINNER CREATION PATCHES THREADING AND IMPORTS HALO LAZILY
def test_create_spinner_imports_halo_lazily(monkeypatch):
    created = {}

    class FakeHalo:
        def __init__(self, spinner):
            created['spinner'] = spinner

    halo_module = types.ModuleType('halo')
    halo_module.Halo = FakeHalo
    original_set_daemon = threading.Thread.setDaemon
    monkeypatch.setitem(sys.modules, 'halo', halo_module)
    monkeypatch.setattr(loading, '_original_set_daemon', None)

    try:
        spinner = loading._create_spinner()
        second_spinner = loading._create_spinner()
    finally:
        threading.Thread.setDaemon = original_set_daemon
        loading._original_set_daemon = None

    assert isinstance(spinner, FakeHalo)
    assert isinstance(second_spinner, FakeHalo)
    assert created['spinner']['interval'] == 200
    assert threading.Thread.setDaemon is original_set_daemon


# TEST FOR LOADING ANIMATION ENABLED PATH
def test_loading_animation_starts_and_stops_spinner(monkeypatch):
    class FakeSpinner:
        def __init__(self):
            self.started = False
            self.stopped = False

        def start(self):
            self.started = True

        def stop(self):
            self.stopped = True

    spinner = FakeSpinner()
    monkeypatch.setattr(loading, '_should_show_spinner', lambda: True)
    monkeypatch.setattr(loading, '_create_spinner', lambda: spinner)

    with loading.LoadingAnimation() as animation:
        assert animation._spinner is spinner
        assert spinner.started is True

    assert spinner.stopped is True


# TEST FOR LOADING ANIMATION DISABLED PATH
def test_loading_animation_disabled_does_not_create_spinner(monkeypatch):
    monkeypatch.setattr(loading, '_should_show_spinner', lambda: False)
    monkeypatch.setattr(loading, '_create_spinner', lambda: (_ for _ in ()).throw(AssertionError('not called')))

    with loading.LoadingAnimation() as animation:
        assert animation._spinner is None
