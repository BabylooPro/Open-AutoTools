import os
import sys

DEFAULT_UPDATE_TIMEOUT_S = 0.75
UPDATE_CACHE_TTL_S = 24 * 60 * 60
FAILED_UPDATE_CACHE_TTL_S = 6 * 60 * 60

# RETURNS TRUE WHEN UPDATE CHECK CACHE SHOULD BE USED
def _cache_enabled():
    if 'pytest' in sys.modules: return False
    disabled = os.getenv('AUTOTOOLS_DISABLE_UPDATE_CACHE', '').lower() in ('1', 'true', 'yes')
    return not disabled

# RETURNS THE USER-SPECIFIC UPDATE CHECK CACHE PATH
def _update_cache_path():
    from pathlib import Path

    custom_path = os.getenv('AUTOTOOLS_UPDATE_CACHE')
    if custom_path: return Path(custom_path)

    if os.name == 'nt':
        cache_root = Path(os.getenv('LOCALAPPDATA') or Path.home() / 'AppData' / 'Local')
    elif sys.platform == 'darwin':
        cache_root = Path.home() / 'Library' / 'Caches'
    else:
        cache_root = Path(os.getenv('XDG_CACHE_HOME') or Path.home() / '.cache')

    return cache_root / 'Open-AutoTools' / 'update-check.json'

# READS A FRESH UPDATE CHECK RESULT FROM CACHE
def _read_cached_update(current_version: str):
    if not _cache_enabled(): return False, None

    try:
        import json
        import time

        data = json.loads(_update_cache_path().read_text(encoding='utf-8'))
        if data.get('current_version') != current_version: return False, None

        checked_at = float(data.get('checked_at', 0))
        ttl = FAILED_UPDATE_CACHE_TTL_S if data.get('status') == 'error' else UPDATE_CACHE_TTL_S
        if time.time() - checked_at > ttl: return False, None

        return True, data.get('message')
    except (OSError, ValueError, TypeError):
        return False, None

# WRITES UPDATE CHECK RESULT TO CACHE
def _write_cached_update(current_version: str, message, status='ok'):
    if not _cache_enabled(): return

    try:
        import json
        import time

        path = _update_cache_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            'checked_at': time.time(),
            'current_version': current_version,
            'status': status,
            'message': message,
        }
        path.write_text(json.dumps(payload), encoding='utf-8')
    except OSError:
        pass

# CHECKS PYPI FOR AVAILABLE UPDATES TO THE PACKAGE
def check_for_updates(timeout=DEFAULT_UPDATE_TIMEOUT_S):
    # SKIP UPDATE CHECK IN TEST ENVIRONMENT
    if os.getenv('PYTEST_CURRENT_TEST') or os.getenv('CI'): return None
    
    import click
    import json
    import urllib.error
    import urllib.request
    from importlib.metadata import distribution, PackageNotFoundError
    from packaging.version import parse as parse_version

    try:
        try:
            dist = distribution("Open-AutoTools")
            current_version_text = dist.version
            current_version = parse_version(current_version_text)
        except PackageNotFoundError:
            return None

        cache_hit, cached_message = _read_cached_update(current_version_text)
        if cache_hit: return cached_message

        pypi_url = "https://pypi.org/pypi/Open-AutoTools/json"
        req = urllib.request.Request(pypi_url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                latest_version = data["info"]["version"]
                latest_parsed = parse_version(latest_version)
                
                if latest_parsed > current_version:
                    update_cmd = "pip install --upgrade Open-AutoTools"
                    message = (
                        click.style(f"\nUpdate available: v{latest_version}", fg='red', bold=True) + "\n" +
                        click.style(f"Run '{update_cmd}' to update", fg='red')
                    )
                    _write_cached_update(current_version_text, message)
                    return message

        _write_cached_update(current_version_text, None)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError, json.JSONDecodeError):
        try:
            current_version_text
        except UnboundLocalError:
            return None
        _write_cached_update(current_version_text, None, status='error')
        pass

    return None 
