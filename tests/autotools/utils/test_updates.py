import pytest
import os
import json
from unittest.mock import patch, MagicMock
from autotools.utils.updates import check_for_updates

# TEST FOR UPDATE CHECK IN TEST ENVIRONMENT
def test_check_for_updates_in_test_env(monkeypatch):
    monkeypatch.setenv('PYTEST_CURRENT_TEST', 'test')
    result = check_for_updates()
    assert result is None

# TEST FOR UPDATE CHECK IN CI ENVIRONMENT
def test_check_for_updates_in_ci_env(monkeypatch):
    monkeypatch.setenv('CI', 'true')
    result = check_for_updates()
    assert result is None

# TEST FOR UPDATE CHECK WITH PACKAGE NOT FOUND
@patch('autotools.utils.updates.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_package_not_found(mock_dist):
    from importlib.metadata import PackageNotFoundError
    mock_dist.side_effect = PackageNotFoundError("Package not found")
    result = check_for_updates()
    assert result is None

# TEST FOR UPDATE CHECK WITH PACKAGE NOT FOUND IN INNER TRY
@patch('urllib.request.urlopen')
@patch('autotools.utils.updates.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_package_not_found_inner(mock_dist, mock_urlopen):
    from importlib.metadata import PackageNotFoundError
    mock_dist.side_effect = PackageNotFoundError("Package not found")
    result = check_for_updates()
    assert result is None

# TEST FOR UPDATE CHECK WITH NO UPDATE AVAILABLE
@patch('urllib.request.urlopen')
@patch('autotools.utils.updates.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_no_update(mock_dist, mock_urlopen):
    mock_dist_obj = MagicMock()
    mock_dist_obj.version = "1.0.0"
    mock_dist.return_value = mock_dist_obj
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value.decode.return_value = json.dumps({"info": {"version": "1.0.0"}})
    mock_urlopen.return_value.__enter__.return_value = mock_response
    result = check_for_updates()
    assert result is None

# TEST FOR UPDATE CHECK WITH STATUS NOT 200
@patch('urllib.request.urlopen')
@patch('autotools.utils.updates.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_status_not_200(mock_dist, mock_urlopen):
    mock_dist_obj = MagicMock()
    mock_dist_obj.version = "1.0.0"
    mock_dist.return_value = mock_dist_obj
    mock_response = MagicMock()
    mock_response.status = 404
    mock_urlopen.return_value.__enter__.return_value = mock_response
    result = check_for_updates()
    assert result is None

# TEST FOR UPDATE CHECK WITH UPDATE AVAILABLE
@patch('urllib.request.urlopen')
@patch('autotools.utils.updates.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_update_available(mock_dist, mock_urlopen):
    mock_dist_obj = MagicMock()
    mock_dist_obj.version = "1.0.0"
    mock_dist.return_value = mock_dist_obj
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value.decode.return_value = json.dumps({"info": {"version": "2.0.0"}})
    mock_urlopen.return_value.__enter__.return_value = mock_response
    result = check_for_updates()
    assert result is not None
    assert "Update available" in result
    assert "2.0.0" in result

# TEST FOR UPDATE CHECK WITH URL ERROR
@patch('urllib.request.urlopen')
@patch('autotools.utils.updates.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_url_error(mock_dist, mock_urlopen):
    import urllib.error
    mock_dist_obj = MagicMock()
    mock_dist_obj.version = "1.0.0"
    mock_dist.return_value = mock_dist_obj
    mock_urlopen.side_effect = urllib.error.URLError("Connection error")
    result = check_for_updates()
    assert result is None
