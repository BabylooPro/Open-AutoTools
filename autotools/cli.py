import click
from importlib.metadata import version as get_version, PackageNotFoundError
import pkg_resources
import requests
from packaging.version import parse as parse_version
from dotenv import load_dotenv
from datetime import datetime
import base64
import json as json_module
from translate import Translator
import yt_dlp
import argparse
from urllib.parse import urlparse

# IMPORT COMMANDS FROM EACH MODULE
from .autocaps.commands import autocaps
from .autolower.commands import autolower
from .autodownload.commands import autodownload
from .autopassword.commands import autopassword
from .autotranslate.commands import autotranslate
from .autoip.commands import autoip
from .autospell.commands import autospell
from .test.commands import test
from .utils.updates import check_for_updates
from .utils.version import print_version

# LOAD ENVIRONMENT VARIABLES FROM .ENV FILE
load_dotenv()

# CLI FUNCTION DEFINITION
@click.group()
@click.option('--version', '--v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help='Show version and check for updates')
@click.option('--help', '-h', is_flag=True, callback=lambda ctx, param, value: 
              None if not value else (click.echo(ctx.get_help() + '\n' + 
              (check_for_updates() or '')) or ctx.exit()),
              is_eager=True, expose_value=False, help='Show this message and exit.')
def cli():
    """A suite of automated tools for various tasks.
    
    Run 'autotools COMMAND --help' for more information on each command."""
    pass

# REGISTER COMMANDS
cli.add_command(autocaps)
cli.add_command(autolower)
cli.add_command(autodownload)
cli.add_command(autopassword)
cli.add_command(autotranslate)
cli.add_command(autoip)
cli.add_command(autospell)
cli.add_command(test)

# MAIN COMMAND DEFINITION
@cli.command()
def autotools():
    """Display available commands and tool information."""
    # SHOW COMMANDS LIST WITH BETTER FORMATTING
    ctx = click.get_current_context()
    commands = cli.list_commands(ctx)
    
    click.echo(click.style("\nOpen-AutoTools Commands:", fg='blue', bold=True))
    for cmd in sorted(commands):
        if cmd != 'autotools':
            cmd_obj = cli.get_command(ctx, cmd)
            help_text = cmd_obj.help or cmd_obj.short_help or ''
            click.echo(f"\n{click.style(cmd, fg='green', bold=True)}")
            click.echo(f"  {help_text}")
            
            # GET OPTIONS FOR EACH COMMAND
            if hasattr(cmd_obj, 'params'):
                click.echo(click.style("\n  Options:", fg='yellow'))
                for param in cmd_obj.params:
                    if isinstance(param, click.Option):
                        opts = '/'.join(param.opts)
                        help_text = param.help or ''
                        click.echo(f"    {click.style(opts, fg='yellow')}")
                        click.echo(f"      {help_text}")

    # SHOW USAGE EXAMPLES
    click.echo(click.style("\nUsage Examples:", fg='blue', bold=True))
    click.echo("  autotools --help         Show this help message")
    click.echo("  autotools --version      Show version information")
    click.echo("  autotools COMMAND        Run a specific command")
    click.echo("  autotools COMMAND --help Show help for a specific command")

    # CHECK FOR UPDATES
    update_msg = check_for_updates()
    if update_msg:
        click.echo(click.style("\nUpdate Available:", fg='red', bold=True))
        click.echo(update_msg)

# ENTRY POINT
if __name__ == '__main__':
    cli()
