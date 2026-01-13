import click
from .core import run
from ..utils.loading import LoadingAnimation
from ..utils.updates import check_for_updates
from ..utils.text import safe_text

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
    with LoadingAnimation():
        output = run(
            test=test, speed=speed, monitor=monitor, interval=interval,
            ports=ports, dns=dns, location=location, no_ip=no_ip
        )
    click.echo(safe_text(output))
    update_msg = check_for_updates()
    if update_msg: click.echo(update_msg) 
