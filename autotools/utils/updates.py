import os
import json
import click
import urllib.request
import urllib.error
from importlib.metadata import version as get_version, distribution, PackageNotFoundError
from packaging.version import parse as parse_version

# CHECKS PYPI FOR AVAILABLE UPDATES TO THE PACKAGE
def check_for_updates():
    # SKIP UPDATE CHECK IN TEST ENVIRONMENT
    if os.getenv('PYTEST_CURRENT_TEST') or os.getenv('CI'): return None
    
    try:
        try:
            dist = distribution("Open-AutoTools")
            current_version = parse_version(dist.version)
        except PackageNotFoundError:
            return None

        pypi_url = "https://pypi.org/pypi/Open-AutoTools/json"
        req = urllib.request.Request(pypi_url)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                latest_version = data["info"]["version"]
                latest_parsed = parse_version(latest_version)
                
                if latest_parsed > current_version:
                    update_cmd = "pip install --upgrade Open-AutoTools"
                    return (
                        click.style(f"\nUpdate available: v{latest_version}", fg='red', bold=True) + "\n" +
                        click.style(f"Run '{update_cmd}' to update", fg='red')
                    )
    except urllib.error.URLError:
        pass

    return None 
