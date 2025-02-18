from halo import Halo

class LoadingAnimation:
    """A CONTEXT MANAGER FOR DISPLAYING A LOADING ANIMATION"""
    def __init__(self):
        self._spinner = Halo(spinner={
            'interval': 200,
            'frames': ['   ', '.  ', '.. ', '...'],
        })
        
    def __enter__(self):
        self._spinner.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._spinner.stop() 
