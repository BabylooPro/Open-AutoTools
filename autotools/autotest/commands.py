import click
import subprocess
import sys
import os
import re
from ..utils.updates import check_for_updates
from ..utils.text import safe_text

# CLI COMMAND TO RUN TEST SUITE WITH PYTEST
@click.command()
@click.option('--unit', '-u', is_flag=True, help='Run only unit tests')
@click.option('--integration', '-i', is_flag=True, help='Run only integration tests')
@click.option('--no-cov', is_flag=True, help='Disable coverage report')
@click.option('--html', is_flag=True, help='Generate HTML coverage report')
@click.option('--module', '-m', help='Test specific module (e.g., autocaps, autolower)')
def autotest(unit, integration, no_cov, html, module):
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
        click.echo(safe_text(click.style("\n[X] pytest and/or pytest-cov not found. Installing...", fg='yellow', bold=True)))
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pytest', 'pytest-cov'], check=True)
            click.echo(safe_text(click.style("[OK] Successfully installed pytest and pytest-cov", fg='green', bold=True)))
        except subprocess.CalledProcessError as e:
            click.echo(safe_text(click.style(f"\n[X] Failed to install dependencies: {str(e)}", fg='red', bold=True)))
            sys.exit(1)

# BUILDS THE TEST COMMAND ARGUMENTS BY ADDING THE CORRECT TEST PATH AND OPTIONS
def _build_test_command(unit, integration, no_cov, html, module):
    cmd = [sys.executable, '-m', 'pytest', '-vv', '--capture=no', '--showlocals', '--log-cli-level=DEBUG', '-s']
    
    if not no_cov:
        if html: cmd.extend(['--cov-report=html', '--cov=autotools'])
        else: cmd.extend(['--cov-report=term-missing', '--cov=autotools'])
    
    if module:
        test_path = f'tests/autotools/{module}'
        if unit and not integration: test_path = f'{test_path}/unit'
        elif integration and not unit: test_path = f'{test_path}/integration'
        cmd.append(test_path)
    else:
        cmd.append('tests')
    
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

# EXTRACTS COVERAGE DATA FROM TOTAL LINE
def _parse_coverage_line(line):
    parts = line.split()
    try:
        if len(parts) >= 4:
            stmts = int(parts[1])
            missed = int(parts[2])
            
            # CHECK IF BRANCHES ARE PRESENT
            if len(parts) >= 6 and parts[3].isdigit() and parts[4].isdigit():
                branches = int(parts[3])
                branch_partial = int(parts[4])
                coverage_pct = float(parts[5].rstrip('%'))
                return {
                    'statements': stmts,
                    'missed': missed,
                    'branches': branches,
                    'branch_partial': branch_partial,
                    'coverage': coverage_pct
                }

            coverage_pct = float(parts[3].rstrip('%'))
            return {'statements': stmts, 'missed': missed, 'coverage': coverage_pct}
    except (ValueError, IndexError):
        match = re.search(r'(\d+\.\d+)%', line)
        if match: return {'coverage': float(match.group(1))}
    return {}

# DETERMINES COLOR BASED ON COVERAGE PERCENTAGE
def _get_coverage_color(percentage):
    if percentage >= 80: return 'green'
    if percentage >= 60: return 'yellow'
    return 'red'

# DISPLAYS COVERAGE METRICS
def _display_coverage_metrics(coverage_data):
    if not coverage_data: return

    click.echo()
    click.echo(click.style("COVERAGE METRICS", fg='blue', bold=True))

    # STATEMENTS COVERAGE
    if 'statements' in coverage_data and 'missed' in coverage_data:
        stmts = coverage_data['statements']
        missed = coverage_data['missed']
        covered = stmts - missed
        stmts_pct = (covered / stmts * 100) if stmts > 0 else 0
        color = _get_coverage_color(stmts_pct)
        click.echo(click.style(f"Statements: {covered}/{stmts} ({stmts_pct:.2f}%)", fg=color, bold=True))

    # BRANCHES COVERAGE
    if 'branches' in coverage_data and coverage_data['branches'] > 0:
        branches = coverage_data['branches']
        branch_partial = coverage_data.get('branch_partial', 0)
        branch_covered = branches - branch_partial
        branch_pct = (branch_covered / branches * 100) if branches > 0 else 0
        color = _get_coverage_color(branch_pct)
        click.echo(click.style(f"Branches: {branch_covered}/{branches} ({branch_pct:.2f}%)", fg=color, bold=True))

    # OVERALL COVERAGE
    if 'coverage' in coverage_data:
        overall = coverage_data['coverage']
        color = _get_coverage_color(overall)
        click.echo(click.style(f"Overall: {overall:.2f}%", fg=color, bold=True))

# RUNS THE TEST PROCESS AND CAPTURES OUTPUT
def _run_test_process(cmd):
    try:
        env = _prepare_test_environment()
        process = _start_test_process(cmd, env)
        coverage_data = _process_test_output(process)
        _handle_test_result(process, coverage_data)
    except subprocess.CalledProcessError as e:
        click.echo(safe_text(click.style(f"\n[X] TESTS FAILED WITH RETURN CODE {e.returncode}", fg='red', bold=True)))
        sys.exit(1)
    except Exception as e:
        click.echo(safe_text(click.style(f"\n[X] ERROR RUNNING TESTS: {str(e)}", fg='red', bold=True)))
        sys.exit(1)

# PREPARES ENVIRONMENT FOR TEST PROCESS
def _prepare_test_environment():
    env = dict(os.environ)
    env['PYTHONPATH'] = os.getcwd()
    env['FORCE_COLOR'] = '1'
    return env

# STARTS THE TEST PROCESS
def _start_test_process(cmd, env):
    return subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )

# PROCESSES TEST OUTPUT AND EXTRACTS COVERAGE DATA
def _process_test_output(process):
    coverage_data = {}
    
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None: break
        
        if 'TOTAL' in line and '%' in line:
            coverage_data = _parse_coverage_line(line)
            sys.stdout.write(line)
            sys.stdout.flush()
            continue
        
        processed_line = _process_test_output_line(line)
        if processed_line:
            sys.stdout.write(processed_line + '\n')
            sys.stdout.flush()
    
    process.wait()
    return coverage_data

# HANDLES TEST RESULT AND DISPLAYS COVERAGE
def _handle_test_result(process, coverage_data):
    if process.returncode == 0:
        click.echo(safe_text(click.style("\n[OK] ALL TESTS PASSED !", fg='green', bold=True)))
        _display_coverage_metrics(coverage_data)
    else:
        click.echo(safe_text(click.style("\n[X] SOME TESTS FAILED!", fg='red', bold=True)))
        sys.exit(1) 
