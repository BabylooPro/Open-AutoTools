from halo import Halo

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
