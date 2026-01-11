import threading
from halo import Halo

# PATCHES THREAD SET DAEMON METHOD TO PREVENT WARNINGS
def _patched_set_daemon(self, daemon):
    self.daemon = daemon

_original_set_daemon = threading.Thread.setDaemon
threading.Thread.setDaemon = _patched_set_daemon

# CONTEXT MANAGER FOR DISPLAYING LOADING ANIMATION
class LoadingAnimation:
    # INITIALIZES SPINNER WITH CUSTOM ANIMATION FRAMES
    def __init__(self):
        self._spinner = Halo(spinner={'interval': 200, 'frames': ['   ', '.  ', '.. ', '...']})
        
    # STARTS THE LOADING ANIMATION
    def __enter__(self):
        self._spinner.start()
        return self
        
    # STOPS THE LOADING ANIMATION
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._spinner.stop()
