import os
import sys
import json
import click
import urllib.request
import urllib.error
from datetime import datetime
from packaging.version import parse as parse_version
from importlib.metadata import version as get_version, PackageNotFoundError

# FORMATS AND DISPLAYS RELEASE DATE
def _format_release_date(upload_time, pkg_version):
    date_formats = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S"]
    for date_format in date_formats:
        try:
            published_date = datetime.strptime(upload_time, date_format)
            formatted_date = published_date.strftime("%d %B %Y at %H:%M:%S")
            prefix = "Pre-Released" if "rc" in pkg_version.lower() else "Released"
            click.echo(f"{prefix}: {formatted_date}")
            return True
        except ValueError:
            continue

    return False

# DISPLAYS RELEASE INFORMATION FROM PYPI DATA
def _display_release_info(data, pkg_version):
    releases = data["releases"]
    if pkg_version in releases and releases[pkg_version]:
        try:
            upload_time = releases[pkg_version][0]["upload_time"]
            _format_release_date(upload_time, pkg_version)
        except Exception:
            pass

# CHECKS AND DISPLAYS UPDATE INFORMATION
def _check_for_updates(current_version, latest_version):
    latest_parsed = parse_version(latest_version)
    if latest_parsed > current_version:
        update_cmd = "pip install --upgrade Open-AutoTools"
        click.echo(click.style(f"\nUpdate available: v{latest_version}", fg='red', bold=True))
        click.echo(click.style(f"Run '{update_cmd}' to update", fg='red'))

# FETCHES AND PROCESSES PYPI VERSION INFORMATION
def _fetch_pypi_version_info(pkg_version):
    pypi_url = "https://pypi.org/pypi/Open-AutoTools/json"
    try:
        req = urllib.request.Request(pypi_url)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status != 200:
                return
            
            data = json.loads(response.read().decode())
            latest_version = data["info"]["version"]
            current_version = parse_version(pkg_version)
            
            _display_release_info(data, pkg_version)
            _check_for_updates(current_version, latest_version)
    except urllib.error.URLError:
        pass

# PRINTS VERSION INFORMATION AND CHECKS FOR UPDATES
def print_version(ctx, value):
    if not value or ctx.resilient_parsing: return

    try:
        pkg_version = get_version('Open-AutoTools')
        click.echo(f"Open-AutoTools version {pkg_version}")

        module = sys.modules.get('autotools')
        module_file = getattr(module, '__file__', '') or ''
        if module and 'site-packages' not in module_file.lower():
            click.echo(click.style("Development mode: enabled", fg='yellow', bold=True))

        _fetch_pypi_version_info(pkg_version)

    except PackageNotFoundError: click.echo("Open-AutoTools version information not available")
    except Exception as e: click.echo(f"Error checking updates: {str(e)}")
    
    ctx.exit() 
