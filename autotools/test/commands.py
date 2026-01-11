import click
import subprocess
import sys
import os
import re
from ..utils.updates import check_for_updates

# CLI COMMAND TO RUN TEST SUITE WITH PYTEST
@click.command()
@click.option('--unit', '-u', is_flag=True, help='Run only unit tests')
@click.option('--integration', '-i', is_flag=True, help='Run only integration tests')
@click.option('--no-cov', is_flag=True, help='Disable coverage report')
@click.option('--html', is_flag=True, help='Generate HTML coverage report')
@click.option('--module', '-m', help='Test specific module (e.g., autocaps, autolower)')
def test(unit, integration, no_cov, html, module):
    _install_test_dependencies()
    
    cmd = _build_test_command(unit, integration, no_cov, html, module)
    
    click.echo(click.style("\nRunning tests with command:", fg='blue', bold=True))
    click.echo(" ".join(cmd))
    click.echo()
    
    _run_test_process(cmd)

    update_msg = check_for_updates()
    if update_msg: click.echo(update_msg)

# INSTALLS TEST DEPENDENCIES IF MISSING BY RUNNING PIP INSTALL COMMAND
def _install_test_dependencies():
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

# BUILDS THE TEST COMMAND ARGUMENTS BY ADDING THE CORRECT TEST PATH AND OPTIONS
def _build_test_command(unit, integration, no_cov, html, module):
    cmd = [sys.executable, '-m', 'pytest', '-vv', '--capture=no', '--showlocals', '--log-cli-level=DEBUG', '-s']
    
    if not no_cov:
        if html: cmd.extend(['--cov-report=html', '--cov=autotools'])
        else: cmd.extend(['--cov-report=term-missing', '--cov=autotools'])
    
    if module:
        test_path = f'autotools/{module}/tests'
        if unit and not integration: test_path = f'{test_path}/unit'
        elif integration and not unit: test_path = f'{test_path}/integration'
        cmd.append(test_path)
    else:
        cmd.append('autotools')
    
    return cmd

# PROCESSES TEST OUTPUT LINE BY REMOVING UNNECESSARY CHARACTERS AND FORMATTING
def _process_test_output_line(line):
    if not line: return None
    line = line.strip()
    if not line: return None
    
    if '::' in line and 'autotools/' in line:
        line = line.split('autotools/')[-1].replace('/tests/', '/')
        parts = line.split('/')
        if len(parts) > 1: line = parts[-1]
    
    line = re.sub(r'\s+', ' ', line)
    line = re.sub(r'\.+', '.', line)
    
    if line.strip('. '): return line

    return None

# RUNS THE TEST PROCESS AND HANDLES OUTPUT BY PROCESSING THE OUTPUT LINE BY LINE
def _run_test_process(cmd):
    try:
        env = dict(os.environ)
        env['PYTHONPATH'] = os.getcwd()
        env['FORCE_COLOR'] = '1'
        
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None: break
            processed_line = _process_test_output_line(line)
            if processed_line:
                sys.stdout.write(processed_line + '\n')
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
