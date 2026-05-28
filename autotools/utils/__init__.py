__all__ = ['LoadingAnimation', 'check_for_updates', 'print_version']

def __getattr__(name):
    if name == 'LoadingAnimation':
        from .loading import LoadingAnimation
        return LoadingAnimation
    if name == 'check_for_updates':
        from .updates import check_for_updates
        return check_for_updates
    if name == 'print_version':
        from .version import print_version
        return print_version

    raise AttributeError(f"module 'autotools.utils' has no attribute {name!r}")
