import pytest

import autotools.utils as utils


# TEST FOR LAZY UTILS EXPORTS
def test_utils_lazy_exports():
    from autotools.utils.loading import LoadingAnimation
    from autotools.utils.updates import check_for_updates
    from autotools.utils.version import print_version

    assert utils.__getattr__('LoadingAnimation') is LoadingAnimation
    assert utils.__getattr__('check_for_updates') is check_for_updates
    assert utils.__getattr__('print_version') is print_version


# TEST FOR LAZY UTILS EXPORTS UNKNOWN NAME
def test_utils_lazy_exports_unknown_name():
    with pytest.raises(AttributeError, match="no attribute 'missing'"):
        utils.__getattr__('missing')
