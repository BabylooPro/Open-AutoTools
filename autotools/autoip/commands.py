import click
from .core import run
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates
from ..utils.text import safe_text, is_ci_environment, mask_sensitive_info

# TOOL CATEGORY (USED BY 'autotools smoke')
TOOL_CATEGORY = 'Network'

# SMOKE TEST CASES (USED BY 'autotools smoke')
SMOKE_TESTS = [
    {'name': 'basic', 'args': ['--no-ip']},
    {'name': 'connectivity', 'args': ['--test']},
    {'name': 'dns', 'args': ['--dns']},
    {'name': 'ports', 'args': ['--ports']},
]

# CLI COMMAND TO DISPLAY NETWORK INFORMATION AND RUN DIAGNOSTICS
@click.command()
@click.option('--test', '-t', is_flag=True, help='Run connectivity tests')
@click.option('--speed', '-s', is_flag=True, help='Run internet speed test')
@click.option('--monitor', '-m', is_flag=True, help='Monitor network traffic')
@click.option('--interval', '-i', default=1, help='Monitoring interval in seconds')
@click.option('--ports', '-p', is_flag=True, help='Check common ports status')
@click.option('--dns', '-d', is_flag=True, help='Show DNS servers')
@click.option('--location', '-l', is_flag=True, help='Show IP location info')
@click.option('--no-ip', '-n', is_flag=True, help='Hide IP addresses')
def autoip(test, speed, monitor, interval, ports, dns, location, no_ip):
    """
        DISPLAYS NETWORK INFORMATION AND RUNS DIAGNOSTICS.

        \b
        FEATURES:
            - Show IP addresses (public and private)
            - RUN CONNECTIVITY TESTS
            - Measure internet speed
            - Monitor network traffic
            - Check port status
            - Display DNS servers
            - Show IP location information

        \b
        EXAMPLES:
            autoip
            autoip --test
            autoip --speed
            autoip --monitor --interval 5
            autoip --ports --dns --location
            autoip --no-ip
    """

    with LoadingAnimation():
        output = run(
            test=test, speed=speed, monitor=monitor, interval=interval,
            ports=ports, dns=dns, location=location, no_ip=no_ip
        )

    if is_ci_environment(): output = mask_sensitive_info(output, mask_ips=True)
    
    click.echo(safe_text(output))
    update_msg = check_for_updates()
    if update_msg: click.echo(update_msg) 
