import click
from importlib.metadata import version as get_version, PackageNotFoundError
import pkg_resources
import requests
from packaging.version import parse as parse_version
from datetime import datetime

# VERSION CALLBACK
def print_version(ctx, param, value):
    """PRINT VERSION AND CHECK FOR UPDATES"""
    if not value or ctx.resilient_parsing:
        return
    
    try:
        # GET CURRENT VERSION
        pkg_version = get_version('Open-AutoTools')
        click.echo(f"Open-AutoTools version {pkg_version}")

        # GET DISTRIBUTION INFO
        dist = pkg_resources.get_distribution("Open-AutoTools")
        current_version = parse_version(dist.version)

        # GET LATEST VERSION FROM PYPI
        pypi_url = "https://pypi.org/pypi/Open-AutoTools/json"
        response = requests.get(pypi_url)
        
        # CHECK IF RESPONSE IS SUCCESSFUL
        if response.status_code == 200:
            data = response.json()
            latest_version = data["info"]["version"]
            releases = data["releases"]
            
            # GET RELEASE DATE
            if pkg_version in releases and releases[pkg_version]:
                try:
                    upload_time = releases[pkg_version][0]["upload_time"]
                    for date_format in [
                        "%Y-%m-%dT%H:%M:%S",
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                        "%Y-%m-%d %H:%M:%S"
                    ]:
                        # TRY TO PARSE DATE
                        try:
                            published_date = datetime.strptime(upload_time, date_format)
                            formatted_date = published_date.strftime("%d %B %Y at %H:%M:%S")
                            # CHECK IF VERSION IS RC
                            if "rc" in pkg_version.lower():
                                click.echo(f"Pre-Released: {formatted_date}")
                            else:
                                click.echo(f"Released: {formatted_date}")
                            break
                        except ValueError:
                            continue
                except Exception:
                    pass  # SKIP DATE IF PARSING FAILS
            
            # CHECK FOR UPDATES
            latest_parsed = parse_version(latest_version)
            
            # COMPARE VERSIONS AND PRINT UPDATE MESSAGE IF NEEDED
            if latest_parsed > current_version:
                update_cmd = "pip install --upgrade Open-AutoTools"
                click.echo(click.style(f"\nUpdate available: v{latest_version}", fg='red', bold=True))
                click.echo(click.style(f"Run '{update_cmd}' to update", fg='red'))

    # EXCEPTIONS FOR ERRORS
    except pkg_resources.DistributionNotFound:
        click.echo("Package distribution not found")
    except PackageNotFoundError:
        click.echo("Open-AutoTools version information not available")
    except Exception as e:
        click.echo(f"Error checking updates: {str(e)}")
    
    ctx.exit() 
