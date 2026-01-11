import click
import requests
import base64
import argparse
import json as json_module
import sys

from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlparse
from packaging.version import parse as parse_version
from importlib.metadata import version as get_version, PackageNotFoundError

from .utils.version import print_version
from .utils.updates import check_for_updates
from .utils.commands import autocaps, autolower, autopassword, autoip, autotest
from .utils.performance import init_metrics, finalize_metrics, get_metrics, should_enable_metrics, track_step

load_dotenv()

# MAIN CLI ENTRY POINT - REGISTERS ALL COMMANDS AND HANDLES GLOBAL OPTIONS
@click.group(invoke_without_command=True)
@click.option('--version', '--v', is_flag=True, callback=lambda ctx, param, value: print_version(ctx, value),
              expose_value=False, is_eager=True, help='Show version and check for updates')
@click.option('--help', '-h', is_flag=True, callback=lambda ctx, param, value: 
              None if not value else (click.echo(ctx.get_help() + '\n' + 
              (check_for_updates() or '')) or ctx.exit()),
              is_eager=True, expose_value=False, help='Show this message and exit.')
@click.option('--perf', is_flag=True, help='Display performance metrics')
@click.pass_context
def cli(ctx, perf):
    """
        A suite of automated tools for various tasks:\n
        - autocaps: Convert text to uppercase\n
        - autolower: Convert text to lowercase\n
        - autopassword: Generate secure passwords and encryption keys\n
        - autoip: Display network information and run diagnostics\n
        - test: Run the test suite\n
        \n
        Run 'autotools COMMAND --help' for more information on each command.\n
    """

    # INITIALIZE METRICS IF NEEDED
    if should_enable_metrics(ctx):
        init_metrics()
        get_metrics().step_start('startup')
        get_metrics().step_end()
        get_metrics().end_startup()
    
    # IF NO COMMAND INVOKED, SHOW HELP
    if ctx.invoked_subcommand is None:
        autotools()
        if should_enable_metrics(ctx):
            get_metrics().end_process()
            finalize_metrics(ctx)

# EXECUTES COMMAND WITH PERFORMANCE TRACKING
def _execute_with_metrics(ctx, original_callback, *args, **kwargs):
    metrics = get_metrics()
    # REMOVE 'perf' FROM kwargs IF PRESENT (IT'S NOT PART OF THE ORIGINAL CALLBACK SIGNATURE)
    kwargs.pop('perf', None)
    
    if not should_enable_metrics(ctx): return original_callback(*args, **kwargs)
    
    if metrics.process_start is None:
        init_metrics()
        get_metrics().end_startup()
    
    metrics.start_command()
    cmd_name = ctx.invoked_subcommand or ctx.command.name or 'unknown'
    try:
        with track_step(f'command_{cmd_name}'): result = original_callback(*args, **kwargs)
        metrics.end_command()
        return result
    finally:
        if metrics.process_end is None:
            metrics.end_process()
            finalize_metrics(ctx)

# WRAPS COMMANDS WITH PERFORMANCE TRACKING
def _wrap_command_with_metrics(cmd):
    import inspect
    original_callback = cmd.callback
    
    # ADD --perf OPTION TO THE COMMAND SO IT CAN BE USED DIRECTLY ON SUBCOMMANDS
    has_perf_option = any(param.opts == ['--perf'] for param in cmd.params if isinstance(param, click.Option))
    if not has_perf_option:
        perf_option = click.Option(['--perf'], is_flag=True, help='Display performance metrics')
        cmd.params.append(perf_option)
    
    sig = inspect.signature(original_callback)
    expects_ctx = 'ctx' in sig.parameters
    
    if expects_ctx:
        @click.pass_context
        def wrapped_callback(ctx, *args, **kwargs):
            return _execute_with_metrics(ctx, original_callback, ctx, *args, **kwargs)
    else:
        def wrapped_callback(*args, **kwargs):
            ctx = click.get_current_context()
            return _execute_with_metrics(ctx, original_callback, *args, **kwargs)
    
    cmd.callback = wrapped_callback
    return cmd

cli.add_command(_wrap_command_with_metrics(autocaps))
cli.add_command(_wrap_command_with_metrics(autolower))
cli.add_command(_wrap_command_with_metrics(autopassword))
cli.add_command(_wrap_command_with_metrics(autoip))
cli.add_command(_wrap_command_with_metrics(autotest), name='test')

# DISPLAYS COMMAND OPTIONS
def _display_command_options(cmd_obj):
    if not hasattr(cmd_obj, 'params'): return
    click.echo(click.style("\n  Options:", fg='yellow'))
    for param in cmd_obj.params:
        if isinstance(param, click.Option):
            opts = '/'.join(param.opts)
            help_text = param.help or ''
            click.echo(f"    {click.style(opts, fg='yellow')}")
            click.echo(f"      {help_text}")

# DISPLAYS ALL AVAILABLE COMMANDS
def _display_commands(ctx, commands):
    click.echo(click.style("\nOpen-AutoTools Commands:", fg='blue', bold=True))
    for cmd in sorted(commands):
        if cmd == 'autotools': continue
        cmd_obj = cli.get_command(ctx, cmd)
        help_text = cmd_obj.help or cmd_obj.short_help or ''
        click.echo(f"\n{click.style(cmd, fg='green', bold=True)}")
        click.echo(f"  {help_text}")
        _display_command_options(cmd_obj)

# DISPLAYS USAGE EXAMPLES
def _display_usage_examples():
    click.echo(click.style("\nUsage Examples:", fg='blue', bold=True))
    click.echo("  autotools --help         Show this help message")
    click.echo("  autotools --version      Show version information")
    click.echo("  autotools COMMAND        Run a specific command")
    click.echo("  autotools COMMAND --help Show help for a specific command")

# DISPLAYS ALL AVAILABLE COMMANDS WITH THEIR OPTIONS AND USAGE EXAMPLES
@cli.command()
def autotools():
    ctx = click.get_current_context()
    commands = cli.list_commands(ctx)

    _display_commands(ctx, commands)
    _display_usage_examples()

    update_msg = check_for_updates()
    if update_msg:
        click.echo(click.style("\nUpdate Available:", fg='red', bold=True))
        click.echo(update_msg)

if __name__ == '__main__': cli()
