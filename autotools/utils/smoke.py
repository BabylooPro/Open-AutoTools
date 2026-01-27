import os
import sys
import time
import click
import tempfile
import subprocess

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple
from .commands import discover_tool_command_entries

# DEFAULT CATEGORIES (USED ONLY FOR OUTPUT TABLE)
_CATEGORY_BY_TOOL = {
    'autocaps': 'Text',
    'autolower': 'Text',
    'autopassword': 'Security',
    'autoip': 'Network',
    'autoconvert': 'Files',
    'autozip': 'Files',
    'autocolor': 'Color',
    'autotodo': 'Task',
    'autounit': 'Conversion',
}

# NORMALIZES SMOKE TEST DEFINITIONS TO A LIST OF (NAME, ARGS)
def _normalize_smoke_test_item(item: Any, default_name: str) -> Tuple[str, List[str]]:
    if isinstance(item, dict):
        name = item.get('name') or default_name
        args = item.get('args') or []
        if not isinstance(args, list):
            raise TypeError("SMOKE_TESTS ITEM 'args' MUST BE A LIST")
        return str(name), [str(x) for x in args]

    if isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[0], str):
        name = item[0] or default_name
        args = item[1] or []
        if not isinstance(args, list):
            raise TypeError("SMOKE_TESTS TUPLE SECOND ITEM MUST BE A LIST")
        return str(name), [str(x) for x in args]

    if isinstance(item, list): return default_name, [str(x) for x in item]
    raise TypeError("SMOKE_TESTS ITEMS MUST BE dict OR (name, args) OR args-list")

def _normalize_smoke_tests(value: Any) -> List[Tuple[str, List[str]]]:
    if not value: return []
    if not isinstance(value, list):
        raise TypeError("SMOKE_TESTS MUST BE A LIST")

    tests: List[Tuple[str, List[str]]] = []
    for idx, item in enumerate(value):
        tests.append(_normalize_smoke_test_item(item, default_name=f"case{idx + 1}"))

    return tests

# BUILDS A BASIC INVOCATION FOR A TOOL USING CLICK PARAMS (BEST-EFFORT)
def _build_default_case(tool: str, cmd: click.Command, tool_dir: Path) -> Tuple[str, List[str]]:
    if tool == 'autocolor': return ('basic', ['#FF5733'])

    if tool == 'autoconvert':
        input_path = tool_dir / 'input.txt'
        input_path.parent.mkdir(parents=True, exist_ok=True)
        input_path.write_text('SMOKE TEST\n', encoding='utf-8')

        output_path = tool_dir / 'output.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return ('txt-json', [str(input_path), str(output_path)])

    required_opts = [p for p in cmd.params if isinstance(p, click.Option) and p.required]
    args_params = [p for p in cmd.params if isinstance(p, click.Argument)]
    argv: List[str] = []

    for opt in required_opts:
        flag = (opt.opts[0] if opt.opts else f'--{opt.name}')
        if opt.is_flag:
            argv.append(flag)
            continue
        argv.extend([flag, _value_for_param(opt, tool_dir)])

    for arg in args_params:
        count = 1
        if isinstance(arg.nargs, int) and arg.nargs > 1: count = arg.nargs
        for _ in range(count): argv.append(_value_for_param(arg, tool_dir))

    return ('default', argv)

# GENERATES A VALUE FOR A CLICK PARAM (BEST-EFFORT)
def _value_for_param(param: click.Parameter, tool_dir: Path) -> str:
    name = (param.name or '').lower()
    if 'color' in name: return '#FF5733'

    looks_like_path = any(k in name for k in ['file', 'path', 'source', 'input', 'output', 'dir', 'folder', 'archive'])
    if isinstance(getattr(param, 'type', None), click.Path) or looks_like_path:
        if any(k in name for k in ['input', 'source']):
            p = tool_dir / f'{param.name or "input"}.txt'
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('SMOKE TEST\n', encoding='utf-8')
            return str(p)

        suffix = '.zip' if 'zip' in name or 'archive' in name or 'output' in name else '.out'
        p = tool_dir / f'{param.name or "output"}{suffix}'
        p.parent.mkdir(parents=True, exist_ok=True)
        return str(p)

    t = getattr(param, 'type', None)
    if isinstance(t, click.Choice) and t.choices: return str(t.choices[0])

    return 'test'

# VERBOSE HELPERS (KEEP _run_subprocess SIMPLE)
# FOR CMD
def _echo_cmd(argv: Sequence[str], verbose: bool) -> None:
    if not verbose: return
    click.echo(click.style(f"$ {' '.join(argv)}", fg='cyan', bold=True))

# FOR OUTPUT
def _echo_output(output: str, verbose: bool) -> None:
    if not verbose: return
    if not output.strip(): return
    click.echo(output.rstrip())

# FOR DURATION
def _echo_duration(duration: float, verbose: bool) -> None:
    if not verbose: return
    click.echo(click.style(f"({duration:.2f}s)", fg='bright_black'))

# FOR TIMEOUT
def _echo_timeout(timeout_s: int, verbose: bool) -> None:
    if not verbose: return
    click.echo(click.style(f"TIMEOUT AFTER {timeout_s}s", fg='red', bold=True))

# FOR PERMISSION ERROR
def _echo_permission_error(err: Exception, verbose: bool) -> None:
    if not verbose: return
    click.echo(click.style(f"PERMISSION ERROR: {err}", fg='red', bold=True))

# RUNS ONE COMMAND AND RETURNS (STATUS, RC, DURATION_S, OUTPUT)
def _run_subprocess(argv: Sequence[str], timeout_s: int, verbose: bool) -> Tuple[str, int, float, str]:
    start = time.perf_counter()
    try:
        completed = subprocess.run(
            list(argv),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_s,
            env=dict(os.environ),
        )
        
        duration = time.perf_counter() - start
        output = completed.stdout or ''
        status = 'OK' if completed.returncode == 0 else 'X'

        _echo_cmd(argv, verbose)
        _echo_output(output, verbose)
        _echo_duration(duration, verbose)

        return status, completed.returncode, duration, output
    except PermissionError as e:
        duration = time.perf_counter() - start
        if duration >= timeout_s:
            _echo_cmd(argv, verbose)
            _echo_timeout(timeout_s, verbose)
            return 'TIMEOUT', 124, duration, ''

        _echo_cmd(argv, verbose)
        _echo_permission_error(e, verbose)
        return 'X', 126, duration, str(e)
    except subprocess.TimeoutExpired as e:
        duration = time.perf_counter() - start
        output = (e.stdout or '') if hasattr(e, 'stdout') else ''

        _echo_cmd(argv, verbose)
        _echo_timeout(timeout_s, verbose)

        return 'TIMEOUT', 124, duration, output

# PRINTS A SUMMARY TABLE (SIMILAR TO docker/run_tests.sh)
def _print_summary(results: List[Dict[str, Any]], platform: str) -> None:
    click.echo(f"\n=== Smoke Test Results Summary for {platform} ===")
    click.echo("┌────────────────┬──────────────────┬──────────────┬────────┐")
    click.echo("│ Category      │ Tool            │ Feature      │ Status │")
    click.echo("├────────────────┼──────────────────┼──────────────┼────────┤")

    for r in results:
        category = r.get('category', 'Other')
        tool = r.get('tool', '')
        feature = r.get('case', '')
        status = r.get('status', '')
        click.echo(f"│ {category:<12} │ {tool:<14} │ {feature:<12} │ {status:<6} │")

    click.echo("└────────────────┴──────────────────┴──────────────┴────────┘")

# RETURNS THE PUBLIC CLI NAME FOR A TOOL PACKAGE
def _tool_public_name(tool_name: str) -> str:
    return 'test' if tool_name == 'autotest' else tool_name

# DECIDES WHETHER A TOOL SHOULD RUN GIVEN include/exclude FILTERS
def _should_run_tool(tool_name: str, public_name: str, include: set[str], exclude: set[str]) -> bool:
    if include and tool_name not in include and public_name not in include: return False
    if tool_name in exclude or public_name in exclude: return False
    return True

# CHOOSES SMOKE TESTS FOR A TOOL (MODULE-DEFINED OR DEFAULT)
def _get_smoke_tests(mod: Any, tool_name: str, cmd: click.Command, tool_dir: Path) -> List[Tuple[str, List[str]]]:
    smoke_tests = _normalize_smoke_tests(getattr(mod, 'SMOKE_TESTS', None))
    if smoke_tests: return smoke_tests
    return [_build_default_case(tool_name, cmd, tool_dir)]

# WORKDIR CONTEXT (CLEANUP ONLY WHEN WE CREATED THE TEMP DIR)
@contextmanager
def _smoke_root(workdir: Optional[str]) -> Iterator[Path]:
    if workdir:
        root = Path(workdir)
        root.mkdir(parents=True, exist_ok=True)
        yield root
        return

    with tempfile.TemporaryDirectory(prefix='autotools_smoke_') as d: yield Path(d)

# RUNS ALL CASES FOR A TOOL AND RETURNS RESULT ROWS
def _run_tool_smoke(
    tool_name: str,
    public_name: str,
    smoke_tests: List[Tuple[str, List[str]]],
    timeout_s: int,
    verbose: bool,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for case_name, case_args in smoke_tests:
        argv = [sys.executable, '-m', 'autotools.cli', public_name, *case_args]
        status, rc, duration_s, output = _run_subprocess(argv, timeout_s=timeout_s, verbose=verbose)

        rows.append({
            'category': _CATEGORY_BY_TOOL.get(tool_name, 'Other'),
            'tool': public_name,
            'case': case_name,
            'status': status if status in ('OK', 'X') else 'X',
            'returncode': rc,
            'duration_s': round(duration_s, 3),
            'cmd': argv,
            'output': output if (verbose or status != 'OK') else '',
        })

    return rows

# MAIN SMOKE ENTRYPOINT
def run_smoke(
    workdir: Optional[str],
    timeout_s: int,
    include: set[str],
    exclude: set[str],
    verbose: bool,
    platform: str,
    print_table: bool = True,
) -> List[Dict[str, Any]]:
    entries = discover_tool_command_entries()

    if 'test' not in include and 'autotest' not in include: exclude = set(exclude) | {'autotest', 'test'}

    with _smoke_root(workdir) as root:
        run_root = root / f"smoke_{int(time.time())}"
        run_root.mkdir(parents=True, exist_ok=True)

        results: List[Dict[str, Any]] = []
        for tool_name in sorted(entries):
            mod, cmd = entries[tool_name]
            public_name = _tool_public_name(tool_name)

            if not _should_run_tool(tool_name, public_name, include, exclude): continue

            tool_dir = run_root / tool_name
            tool_dir.mkdir(parents=True, exist_ok=True)

            smoke_tests = _get_smoke_tests(mod, tool_name, cmd, tool_dir)
            results.extend(_run_tool_smoke(tool_name, public_name, smoke_tests, timeout_s=timeout_s, verbose=verbose))

        if print_table: _print_summary(results, platform=platform)

        return results

