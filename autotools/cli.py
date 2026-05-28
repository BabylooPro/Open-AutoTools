import click
import json as json_module
import os

from .utils.commands import get_tool_names, get_wrapped_tool_command, get_wrapped_tool_commands

def _public_tool_name(tool_name):
    return 'test' if tool_name == 'autotest' else tool_name

def _internal_tool_name(public_name):
    return 'autotest' if public_name == 'test' else public_name

def _load_dotenv_if_present():
    if not os.path.exists('.env'): return
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

def print_version(ctx, value):
    if not value or ctx.resilient_parsing: return
    _load_dotenv_if_present()
    from .utils.version import print_version as _print_version
    return _print_version(ctx, value)

def check_for_updates():
    from .utils.updates import check_for_updates as _check_for_updates
    return _check_for_updates()

def _ctx_has_perf_flag(ctx):
    current = ctx
    while current:
        if current.params.get('perf', False): return True
        current = getattr(current, 'parent', None)
    return False

def should_enable_metrics(ctx):
    if not _ctx_has_perf_flag(ctx): return False
    from .utils.performance import should_enable_metrics as _should_enable_metrics
    return _should_enable_metrics(ctx)

def init_metrics():
    from .utils.performance import init_metrics as _init_metrics
    return _init_metrics()

def finalize_metrics(ctx):
    from .utils.performance import finalize_metrics as _finalize_metrics
    return _finalize_metrics(ctx)

def get_metrics():
    from .utils.performance import get_metrics as _get_metrics
    return _get_metrics()

# CLICK COMMAND PROXY USED BY console_scripts AND TESTS WITHOUT IMPORTING EVERY TOOL
class LazyToolCommand(click.Command):
    def __init__(self, tool_name):
        self.tool_name = tool_name
        super().__init__(name=_public_tool_name(tool_name))

    def _load_command(self):
        cmd = get_wrapped_tool_command(self.tool_name)
        if cmd is None:
            raise click.ClickException(f"Unknown tool: {self.tool_name}")
        return cmd

    def main(self, *args, **kwargs):
        return self._load_command().main(*args, **kwargs)

# LAZY GROUP: LISTS TOOLS WITHOUT IMPORTING THEM, IMPORTS ONLY THE SELECTED COMMAND
class LazyAutoToolsGroup(click.Group):
    def list_commands(self, ctx):
        commands = set(super().list_commands(ctx))
        commands.update(_public_tool_name(tool_name) for tool_name in get_tool_names())
        return sorted(commands)

    def get_command(self, ctx, cmd_name):
        cmd = super().get_command(ctx, cmd_name)
        if cmd is not None: return cmd

        tool_name = _internal_tool_name(cmd_name)
        return get_wrapped_tool_command(tool_name)

# MAIN CLI ENTRY POINT - REGISTERS ALL COMMANDS AND HANDLES GLOBAL OPTIONS
@click.group(cls=LazyAutoToolsGroup, invoke_without_command=True)
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
        \b
        A suite of automated tools for various tasks:
            - autocaps: Convert text to uppercase
            - autolower: Convert text to lowercase
            - autopassword: Generate secure passwords and encryption keys
            - autoip: Display network information and run diagnostics
            - autoconvert: Convert text, images, audio, and video between formats
            - autocolor: Convert color codes between different formats (hex, RGB, HSL, etc)
            - autounit: Convert measurement units (meters to feet, liters to gallons, etc)
            - autozip: Compress files and directories into various archive formats (zip, tar.gz, etc)
            - autotodo: Create and manages a simple task list in a markdown file
            - autonote: Takes quick notes and saves them to a markdown file
            - test: Run the test suite (development only)

        \b
        Run 'autotools COMMAND --help' for more information on each command.
    """

    # INITIALIZE METRICS IF NEEDED
    _load_dotenv_if_present()
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

# LISTS TOOL SUBCOMMANDS (MACHINE-FRIENDLY)
@cli.command(name='list-tools')
@click.option('--json', 'as_json', is_flag=True, help='OUTPUT JSON')
def list_tools(as_json):
    tools = [_public_tool_name(tool_name) for tool_name in get_tool_names()]
    tools = sorted(set(tools))
    if as_json: click.echo(json_module.dumps(tools))
    else: click.echo("\n".join(tools))

# RUNS SMOKE TESTS FOR ALL DISCOVERED TOOLS (USED BY docker/run_tests.sh)
@cli.command()
@click.option('--workdir', type=click.Path(file_okay=False, dir_okay=True), default=None, help='WORK DIRECTORY FOR TEMP FILES')
@click.option('--timeout', type=int, default=30, help='PER-CASE TIMEOUT (SECONDS)')
@click.option('--include', 'include_tools', multiple=True, help='ONLY RUN THESE TOOLS (REPEATABLE)')
@click.option('--exclude', 'exclude_tools', multiple=True, help='SKIP THESE TOOLS (REPEATABLE)')
@click.option('--json', 'as_json', is_flag=True, help='OUTPUT JSON RESULTS')
@click.option('--verbose/--quiet', default=(os.getenv('VERBOSE', '1') == '1'), help='SHOW COMMAND OUTPUT')
def smoke(workdir, timeout, include_tools, exclude_tools, as_json, verbose):
    from .utils.smoke import run_smoke

    results = run_smoke(
        workdir=workdir,
        timeout_s=timeout,
        include=set(include_tools),
        exclude=set(exclude_tools),
        verbose=verbose,
        platform=os.getenv('PLATFORM') or 'Unknown Platform',
        print_table=not as_json
    )

    if as_json: click.echo(json_module.dumps(results, ensure_ascii=False))

    failed = [r for r in results if r.get('status') != 'OK']
    raise SystemExit(1 if failed else 0)

autocaps = LazyToolCommand('autocaps')
autolower = LazyToolCommand('autolower')
autopassword = LazyToolCommand('autopassword')
autoip = LazyToolCommand('autoip')
autoconvert = LazyToolCommand('autoconvert')
autocolor = LazyToolCommand('autocolor')
autounit = LazyToolCommand('autounit')
autozip = LazyToolCommand('autozip')
autotodo = LazyToolCommand('autotodo')
autonote = LazyToolCommand('autonote')
autotest = LazyToolCommand('autotest')

if __name__ == '__main__': cli()
