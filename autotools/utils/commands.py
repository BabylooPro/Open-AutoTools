import click
import inspect
import importlib
import pkgutil
from types import ModuleType
from typing import Dict, Iterable, List, Tuple

from .performance import init_metrics, finalize_metrics, get_metrics, should_enable_metrics, track_step

__all__ = [
    'discover_tool_command_entries',
    'get_wrapped_tool_commands',
    'register_commands',
    'get_tool_category'
]

# PACKAGES THAT SHOULD NEVER BE TREATED AS TOOLS
_EXCLUDED_TOOL_PACKAGES = {'utils', '__pycache__'}

# ITERATES ALL TOP-LEVEL TOOL PACKAGES (autotools/<tool>/)
def _iter_tool_packages() -> Iterable[str]:
    import autotools as autotools_pkg
    for module_info in pkgutil.iter_modules(autotools_pkg.__path__):
        if not module_info.ispkg: continue
        name = module_info.name
        if name.startswith('_'): continue
        if name in _EXCLUDED_TOOL_PACKAGES: continue
        if name == 'cli': continue
        yield name

# IMPORTS autotools.<tool>.commands IF IT EXISTS
def _import_tool_commands_module(tool_name: str) -> ModuleType | None:
    full_name = f'autotools.{tool_name}.commands'
    try:
        return importlib.import_module(full_name)
    except ModuleNotFoundError as e:
        if e.name == full_name: return None
        raise

# EXTRACTS ALL CLICK COMMAND OBJECTS FROM A MODULE
def _extract_click_commands(mod: ModuleType) -> List[click.Command]:
    commands: List[click.Command] = []
    for value in mod.__dict__.values():
        if isinstance(value, click.core.Command): commands.append(value)
    return commands

# SELECTS THE APPROPRIATE COMMAND FROM A LIST OF COMMANDS FOR A GIVEN TOOL NAME
def _select_command_for_tool(cmds: List[click.Command], tool_name: str, mod_name: str) -> click.Command:
    selected = None
    for c in cmds:
        if c.name == tool_name:
            selected = c
            break

    if selected is None:
        if len(cmds) == 1:
            selected = cmds[0]
        else:
            names = ', '.join(sorted({c.name or '<unnamed>' for c in cmds}))
            raise RuntimeError(f"MULTIPLE CLICK COMMANDS FOUND IN {mod_name}: {names}")

    return selected

# DISCOVERS TOOL COMMANDS AS (MODULE, CLICK COMMAND) BY TOOL PACKAGE NAME
def discover_tool_command_entries() -> Dict[str, Tuple[ModuleType, click.Command]]:
    entries: Dict[str, Tuple[ModuleType, click.Command]] = {}
    for tool_name in _iter_tool_packages():
        mod = _import_tool_commands_module(tool_name)
        if mod is None: continue
        cmds = _extract_click_commands(mod)
        if not cmds: continue

        selected = _select_command_for_tool(cmds, tool_name, mod.__name__)
        entries[tool_name] = (mod, selected)

    return entries

# RETURNS WRAPPED TOOL COMMANDS (USED BY CLI GROUP AND CONSOLE_SCRIPTS EXPORTS)
def get_wrapped_tool_commands() -> Dict[str, click.Command]:
    wrapped: Dict[str, click.Command] = {}
    for tool_name, (_mod, cmd) in discover_tool_command_entries().items():
        wrapped[tool_name] = _wrap_command_with_metrics(cmd)
    return wrapped

# EXECUTES COMMAND WITH PERFORMANCE TRACKING
def _execute_with_metrics(ctx, original_callback, *args, **kwargs):
    metrics = get_metrics()
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
    if getattr(cmd, '_autotools_metrics_wrapped', False): return cmd

    original_callback = cmd.callback
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
    cmd._autotools_metrics_wrapped = True
    return cmd

# EXTRACTS TOOL CATEGORY FROM MODULE (FALLBACK TO 'Other' IF NOT DEFINED)
def get_tool_category(mod: ModuleType) -> str:
    return getattr(mod, 'TOOL_CATEGORY', 'Other')

# FUNCTION TO REGISTER ALL COMMANDS TO CLI GROUP
def register_commands(cli_group):
    wrapped = get_wrapped_tool_commands()
    for tool_name in sorted(wrapped):
        cmd = wrapped[tool_name]
        if tool_name == 'autotest': cli_group.add_command(cmd, name='test')
        else: cli_group.add_command(cmd)
