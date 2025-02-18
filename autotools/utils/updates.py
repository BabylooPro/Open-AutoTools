import click
import requests
from importlib.metadata import version as get_version
from packaging.version import parse as parse_version
import pkg_resources

def check_for_updates():
    """CHECK IF AN UPDATE IS AVAILABLE AND RETURN UPDATE MESSAGE IF NEEDED"""
    try:
        dist = pkg_resources.get_distribution("Open-AutoTools")
        current_version = parse_version(dist.version)

        pypi_url = "https://pypi.org/pypi/Open-AutoTools/json"
        response = requests.get(pypi_url)
        
        if response.status_code == 200:
            data = response.json()
            latest_version = data["info"]["version"]
            latest_parsed = parse_version(latest_version)
            
            if latest_parsed > current_version:
                update_cmd = "pip install --upgrade Open-AutoTools"
                return (
                    click.style(f"\nUpdate available: v{latest_version}", fg='red', bold=True) + "\n" +
                    click.style(f"Run '{update_cmd}' to update", fg='red')
                )
    except Exception as e:
        print(f"Error checking updates: {str(e)}")
    
    return None 
