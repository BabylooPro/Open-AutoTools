import click
import inspect

from ..autocaps.commands import autocaps as _autocaps
from ..autolower.commands import autolower as _autolower
from ..autopassword.commands import autopassword as _autopassword
from ..autoip.commands import autoip as _autoip
from ..autotest.commands import autotest as _autotest
from ..autoconvert.commands import autoconvert as _autoconvert
from ..autocolor.commands import autocolor as _autocolor
from .performance import init_metrics, finalize_metrics, get_metrics, should_enable_metrics, track_step

__all__ = [
    'autocaps',
    'autolower',
    'autopassword',
    'autoip',
    'autotest',
    'autoconvert',
    'autocolor',
    'register_commands'
]

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
    return cmd

# WRAP COMMANDS WITH METRICS
autocaps = _wrap_command_with_metrics(_autocaps)
autolower = _wrap_command_with_metrics(_autolower)
autopassword = _wrap_command_with_metrics(_autopassword)
autoip = _wrap_command_with_metrics(_autoip)
autoconvert = _wrap_command_with_metrics(_autoconvert)
autocolor = _wrap_command_with_metrics(_autocolor)
autotest = _wrap_command_with_metrics(_autotest)

# FUNCTION TO REGISTER ALL COMMANDS TO CLI GROUP
def register_commands(cli_group):
    cli_group.add_command(autocaps)
    cli_group.add_command(autolower)
    cli_group.add_command(autopassword)
    cli_group.add_command(autoip)
    cli_group.add_command(autoconvert)
    cli_group.add_command(autocolor)
    cli_group.add_command(autotest, name='test')
