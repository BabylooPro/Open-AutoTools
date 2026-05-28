import pytest
import os
import json
import sys
import time
from unittest.mock import patch, MagicMock
from autotools.utils.updates import DEFAULT_UPDATE_TIMEOUT_S, check_for_updates
import autotools.utils.updates as updates_module


class FakePath:
    def __init__(self, *parts):
        self.parts = tuple(str(part) for part in parts)

    @classmethod
    def home(cls):
        return cls('HOME')

    def __truediv__(self, other):
        return FakePath(*self.parts, other)

    def __str__(self):
        return '/'.join(self.parts)

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
@patch('importlib.metadata.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_package_not_found(mock_dist):
    from importlib.metadata import PackageNotFoundError
    mock_dist.side_effect = PackageNotFoundError("Package not found")
    result = check_for_updates()
    assert result is None

# TEST FOR UPDATE CHECK WITH PACKAGE NOT FOUND IN INNER TRY
@patch('urllib.request.urlopen')
@patch('importlib.metadata.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_package_not_found_inner(mock_dist, mock_urlopen):
    from importlib.metadata import PackageNotFoundError
    mock_dist.side_effect = PackageNotFoundError("Package not found")
    result = check_for_updates()
    assert result is None

# TEST FOR UPDATE CHECK WITH NO UPDATE AVAILABLE
@patch('urllib.request.urlopen')
@patch('importlib.metadata.distribution')
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
@patch('importlib.metadata.distribution')
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

# TEST FOR UPDATE CHECK DEFAULT TIMEOUT BUDGET
@patch('urllib.request.urlopen')
@patch('importlib.metadata.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_uses_short_default_timeout(mock_dist, mock_urlopen):
    mock_dist_obj = MagicMock()
    mock_dist_obj.version = "1.0.0"
    mock_dist.return_value = mock_dist_obj
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value.decode.return_value = json.dumps({"info": {"version": "1.0.0"}})
    mock_urlopen.return_value.__enter__.return_value = mock_response

    result = check_for_updates()

    assert result is None
    assert mock_urlopen.call_args.kwargs['timeout'] == DEFAULT_UPDATE_TIMEOUT_S
    assert DEFAULT_UPDATE_TIMEOUT_S <= 1.0

# TEST FOR UPDATE CHECK CACHE HIT SKIPS NETWORK
@patch('urllib.request.urlopen')
@patch('importlib.metadata.distribution')
@patch('autotools.utils.updates._cache_enabled')
@patch('autotools.utils.updates._update_cache_path')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_cache_hit_skips_network(mock_cache_path, mock_cache_enabled, mock_dist, mock_urlopen, tmp_path):
    cache_path = tmp_path / 'update-check.json'
    cache_path.write_text(
        json.dumps({
            'checked_at': time.time(),
            'current_version': '1.0.0',
            'status': 'ok',
            'message': 'cached update message',
        }),
        encoding='utf-8',
    )
    mock_cache_path.return_value = cache_path
    mock_cache_enabled.return_value = True
    mock_dist_obj = MagicMock()
    mock_dist_obj.version = "1.0.0"
    mock_dist.return_value = mock_dist_obj

    result = check_for_updates()

    assert result == 'cached update message'
    mock_urlopen.assert_not_called()


# TEST FOR UPDATE CACHE ENABLED FLAG
def test_cache_enabled_respects_disable_env(monkeypatch):
    monkeypatch.delitem(sys.modules, 'pytest', raising=False)
    monkeypatch.delenv('AUTOTOOLS_DISABLE_UPDATE_CACHE', raising=False)

    assert updates_module._cache_enabled() is True

    monkeypatch.setenv('AUTOTOOLS_DISABLE_UPDATE_CACHE', 'yes')
    assert updates_module._cache_enabled() is False


# TEST FOR CUSTOM UPDATE CACHE PATH
def test_update_cache_path_custom(monkeypatch, tmp_path):
    cache_path = tmp_path / 'custom-cache.json'
    monkeypatch.setenv('AUTOTOOLS_UPDATE_CACHE', str(cache_path))

    assert updates_module._update_cache_path() == cache_path


# TEST FOR DEFAULT UPDATE CACHE PATHS BY PLATFORM
def test_update_cache_path_defaults_by_platform(monkeypatch):
    import pathlib

    monkeypatch.delenv('AUTOTOOLS_UPDATE_CACHE', raising=False)
    monkeypatch.setattr(pathlib, 'Path', FakePath)

    monkeypatch.setattr(updates_module.os, 'name', 'nt', raising=False)
    monkeypatch.setenv('LOCALAPPDATA', 'LOCAL')
    assert str(updates_module._update_cache_path()) == 'LOCAL/Open-AutoTools/update-check.json'

    monkeypatch.setattr(updates_module.os, 'name', 'posix', raising=False)
    monkeypatch.setattr(updates_module.sys, 'platform', 'darwin')
    assert str(updates_module._update_cache_path()) == 'HOME/Library/Caches/Open-AutoTools/update-check.json'

    monkeypatch.setattr(updates_module.sys, 'platform', 'linux')
    monkeypatch.setenv('XDG_CACHE_HOME', 'XDG')
    assert str(updates_module._update_cache_path()) == 'XDG/Open-AutoTools/update-check.json'


# TEST FOR CACHE VERSION MISMATCH
def test_read_cached_update_version_mismatch(monkeypatch, tmp_path):
    cache_path = tmp_path / 'update-check.json'
    cache_path.write_text(
        json.dumps({
            'checked_at': time.time(),
            'current_version': '2.0.0',
            'status': 'ok',
            'message': 'cached',
        }),
        encoding='utf-8',
    )
    monkeypatch.setattr(updates_module, '_cache_enabled', lambda: True)
    monkeypatch.setattr(updates_module, '_update_cache_path', lambda: cache_path)

    assert updates_module._read_cached_update('1.0.0') == (False, None)


# TEST FOR CACHE TTL EXPIRY
def test_read_cached_update_expired(monkeypatch, tmp_path):
    cache_path = tmp_path / 'update-check.json'
    cache_path.write_text(
        json.dumps({
            'checked_at': time.time() - updates_module.UPDATE_CACHE_TTL_S - 1,
            'current_version': '1.0.0',
            'status': 'ok',
            'message': 'cached',
        }),
        encoding='utf-8',
    )
    monkeypatch.setattr(updates_module, '_cache_enabled', lambda: True)
    monkeypatch.setattr(updates_module, '_update_cache_path', lambda: cache_path)

    assert updates_module._read_cached_update('1.0.0') == (False, None)


# TEST FOR CACHE READ ERRORS
def test_read_cached_update_invalid_json(monkeypatch, tmp_path):
    cache_path = tmp_path / 'update-check.json'
    cache_path.write_text('not json', encoding='utf-8')
    monkeypatch.setattr(updates_module, '_cache_enabled', lambda: True)
    monkeypatch.setattr(updates_module, '_update_cache_path', lambda: cache_path)

    assert updates_module._read_cached_update('1.0.0') == (False, None)


# TEST FOR WRITING CACHE PAYLOAD
def test_write_cached_update_writes_payload(monkeypatch, tmp_path):
    cache_path = tmp_path / 'nested' / 'update-check.json'
    monkeypatch.setattr(updates_module, '_cache_enabled', lambda: True)
    monkeypatch.setattr(updates_module, '_update_cache_path', lambda: cache_path)

    updates_module._write_cached_update('1.0.0', 'message', status='error')

    data = json.loads(cache_path.read_text(encoding='utf-8'))
    assert data['current_version'] == '1.0.0'
    assert data['status'] == 'error'
    assert data['message'] == 'message'


# TEST FOR CACHE WRITE ERRORS
def test_write_cached_update_ignores_os_error(monkeypatch):
    class BadParent:
        def mkdir(self, **_kwargs):
            raise OSError('cannot create cache dir')

    class BadPath:
        parent = BadParent()

        def write_text(self, *_args, **_kwargs):
            raise AssertionError('write should not be reached')

    monkeypatch.setattr(updates_module, '_cache_enabled', lambda: True)
    monkeypatch.setattr(updates_module, '_update_cache_path', lambda: BadPath())

    updates_module._write_cached_update('1.0.0', None)


# TEST FOR UPDATE CHECK WITH UPDATE AVAILABLE
@patch('urllib.request.urlopen')
@patch('importlib.metadata.distribution')
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
@patch('importlib.metadata.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_url_error(mock_dist, mock_urlopen):
    import urllib.error
    mock_dist_obj = MagicMock()
    mock_dist_obj.version = "1.0.0"
    mock_dist.return_value = mock_dist_obj
    mock_urlopen.side_effect = urllib.error.URLError("Connection error")
    result = check_for_updates()
    assert result is None


# TEST FOR UPDATE CHECK ERROR BEFORE CURRENT VERSION IS AVAILABLE
@patch('importlib.metadata.distribution')
@patch.dict('os.environ', {}, clear=True)
def test_check_for_updates_distribution_os_error(mock_dist):
    mock_dist.side_effect = OSError('metadata read failed')

    assert check_for_updates() is None
