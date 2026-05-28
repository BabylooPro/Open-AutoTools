import os
import sys
import threading

# PATCHES THREAD SET DAEMON METHOD TO PREVENT WARNINGS
def _patched_set_daemon(self, daemon):
    self.daemon = daemon

_original_set_daemon = None

def _should_show_spinner():
    if os.getenv('CI') or os.getenv('PYTEST_CURRENT_TEST'): return False
    if os.getenv('TERM', '').lower() == 'dumb': return False
    return bool(getattr(sys.stderr, 'isatty', lambda: False)())

def _create_spinner():
    global _original_set_daemon
    if _original_set_daemon is None:
        _original_set_daemon = threading.Thread.daemon
        threading.Thread.daemon = _patched_set_daemon

    from halo import Halo
    return Halo(spinner={'interval': 200, 'frames': ['   ', '.  ', '.. ', '...']})

# CONTEXT MANAGER FOR DISPLAYING LOADING ANIMATION
class LoadingAnimation:
    # INITIALIZES SPINNER WITH CUSTOM ANIMATION FRAMES
    def __init__(self):
        self._spinner = None
        self._enabled = _should_show_spinner()
        
    # STARTS THE LOADING ANIMATION
    def __enter__(self):
        if self._enabled:
            self._spinner = _create_spinner()
            self._spinner.start()
        return self
        
    # STOPS THE LOADING ANIMATION
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._spinner is not None: self._spinner.stop()
