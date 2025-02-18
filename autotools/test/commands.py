import click
import subprocess
import sys
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates

@click.command()
@click.option('--unit', '-u', is_flag=True, help='Run only unit tests')
@click.option('--integration', '-i', is_flag=True, help='Run only integration tests')
@click.option('--no-cov', is_flag=True, help='Disable coverage report')
@click.option('--html', is_flag=True, help='Generate HTML coverage report')
@click.option('--module', '-m', help='Test specific module (e.g., autocaps, autolower)')
def test(unit, integration, no_cov, html, module):
    """Run test suite with various options."""
    # CHECK IF PYTEST IS INSTALLED
    try:
        import pytest
        import pytest_cov
    except ImportError:
        click.echo(click.style("\n❌ pytest and/or pytest-cov not found. Installing...", fg='yellow', bold=True))
        with LoadingAnimation():
            try:
                subprocess.run(['pip', 'install', 'pytest', 'pytest-cov'], check=True)
                click.echo(click.style("✅ Successfully installed pytest and pytest-cov", fg='green', bold=True))
            except subprocess.CalledProcessError as e:
                click.echo(click.style(f"\n❌ Failed to install dependencies: {str(e)}", fg='red', bold=True))
                sys.exit(1)
    
    cmd = ['python', '-m', 'pytest', '-v'] # BASE COMMAND
    
    # COVERAGE OPTIONS
    if not no_cov:
        cmd.extend(['--cov=autotools'])
        if html:
            cmd.extend(['--cov-report=html'])
        else:
            cmd.extend(['--cov-report=term-missing'])
    
    # TEST SELECTION
    test_path = 'autotools'
    if module:
        if unit and not integration:
            cmd.append(f'autotools/{module}/tests/test_{module}_core.py')
        elif integration and not unit:
            cmd.append(f'autotools/{module}/tests/test_{module}_integration.py')
        else:
            cmd.append(f'autotools/{module}/tests')
    
    # SHOW COMMAND BEING RUN
    click.echo(click.style("\nRunning tests with command:", fg='blue', bold=True))
    click.echo(" ".join(cmd))
    click.echo()
    
    # RUN TESTS
    try:
        with LoadingAnimation():
            result = subprocess.run(cmd, check=True)
            if result.returncode == 0:
                click.echo(click.style("\n✅ All tests passed!", fg='green', bold=True))
            else:
                click.echo(click.style("\n❌ Some tests failed!", fg='red', bold=True))
                sys.exit(1)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"\n❌ Tests failed with return code {e.returncode}", fg='red', bold=True))
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"\n❌ Error running tests: {str(e)}", fg='red', bold=True))
        sys.exit(1)
    
    # UPDATE CHECK AT THE END
    update_msg = check_for_updates()
    if update_msg:
        click.echo(update_msg) 
