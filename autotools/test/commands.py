import click
import subprocess
import sys
import os
import re
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
        try:
            subprocess.run(['pip', 'install', 'pytest', 'pytest-cov'], check=True)
            click.echo(click.style("✅ Successfully installed pytest and pytest-cov", fg='green', bold=True))
        except subprocess.CalledProcessError as e:
            click.echo(click.style(f"\n❌ Failed to install dependencies: {str(e)}", fg='red', bold=True))
            sys.exit(1)
    
    # BASE COMMAND WITH ENHANCED VERBOSITY
    cmd = [
        sys.executable,             # USE SYSTEM PYTHON EXECUTABLE
        '-m', 'pytest',            # RUN PYTEST AS MODULE
        '-vv',                     # VERY VERBOSE OUTPUT
        '--capture=no',            # SHOW PRINT STATEMENTS
        '--showlocals',            # SHOW LOCAL VARIABLES IN TRACEBACKS
        '--log-cli-level=DEBUG',   # SHOW DEBUG LOGS
        '-s',                      # DISABLE CAPTURE
    ]
    
    # COVERAGE OPTIONS
    if not no_cov:
        if html:
            cmd.extend(['--cov-report=html', '--cov=autotools'])
        else:
            cmd.extend(['--cov-report=term-missing', '--cov=autotools'])
    
    # TEST SELECTION
    if module:
        test_path = f'autotools/{module}/tests'
        if unit and not integration:
            test_path = f'{test_path}/unit'
        elif integration and not unit:
            test_path = f'{test_path}/integration'
        cmd.append(test_path)
    else:
        cmd.append('autotools')
    
    # SHOW COMMAND BEING RUN
    click.echo(click.style("\nRunning tests with command:", fg='blue', bold=True))
    click.echo(" ".join(cmd))
    click.echo()
    
    # RUN TESTS
    try:
        env = dict(os.environ)
        env['PYTHONPATH'] = os.getcwd()
        env['FORCE_COLOR'] = '1'  # FORCE COLORS IN OUTPUT
        
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # READ AND PROCESS OUTPUT IN REAL-TIME
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                # CLEAN THE LINE
                line = line.strip()
                if line:  # ONLY PROCESS NON-EMPTY LINES
                    if '::' in line and 'autotools/' in line:
                        # REMOVE PARENT DIRECTORY PATHS
                        line = line.split('autotools/')[-1].replace('/tests/', '/')
                        # REMOVE MODULE PARENT DIRECTORY
                        parts = line.split('/')
                        if len(parts) > 1:
                            line = parts[-1]
                    # REMOVE MULTIPLE SPACES AND DOTS
                    line = re.sub(r'\s+', ' ', line)
                    line = re.sub(r'\.+', '.', line)
                    # REMOVE EMPTY LINES WITH JUST DOTS OR SPACES
                    if line.strip('. '):
                        sys.stdout.write(line + '\n')
                        sys.stdout.flush()
        
        process.wait()
        if process.returncode == 0:
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
