#!/usr/bin/env python3

from __future__ import annotations

import json
import math
import os
import shutil
import statistics
import subprocess
import sys
import time

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Sequence, Set

from autotools.utils.commands import discover_tool_command_entries, get_tool_category
from autotools.utils.smoke import _build_default_case, _normalize_smoke_tests


DEFAULT_ITERATIONS = 5
DEFAULT_WARMUP = 1
DEFAULT_TIMEOUT_S = 30
DEFAULT_OUTPUT_DIR = "/data/benchmarks"
DEFAULT_WORKDIR = "/tmp/autotools-benchmarks"
DEFAULT_PROJECT_ROOT = "/app"


# STORES DOCKER BENCHMARK RUNTIME CONFIGURATION
@dataclass(frozen=True)
class BenchmarkConfig:
    iterations: int
    warmup: int
    timeout_s: int
    include: Set[str]
    exclude: Set[str]
    output_dir: Path
    workdir: Path
    project_root: Path
    platform: str
    python_version: str


# PARSES AN INTEGER ENVIRONMENT VARIABLE WITH A MINIMUM VALUE
def parse_int_env(env: Dict[str, str], name: str, default: int, minimum: int) -> int:
    raw_value = env.get(name, "").strip()
    if not raw_value: return default

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {raw_value!r}") from exc

    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}, got {value}")
    return value


# PARSES COMMA OR SPACE SEPARATED TOOL FILTERS
def parse_tool_filter(value: str | None) -> Set[str]:
    if not value: return set()
    normalized = value.replace(",", " ")
    return {item.strip() for item in normalized.split() if item.strip()}


# LOADS BENCHMARK CONFIGURATION FROM ENVIRONMENT VARIABLES
def load_config(env: Dict[str, str] | None = None) -> BenchmarkConfig:
    env = dict(os.environ if env is None else env)

    return BenchmarkConfig(
        iterations=parse_int_env(env, "BENCHMARK_ITERATIONS", DEFAULT_ITERATIONS, 1),
        warmup=parse_int_env(env, "BENCHMARK_WARMUP", DEFAULT_WARMUP, 0),
        timeout_s=parse_int_env(env, "BENCHMARK_TIMEOUT", DEFAULT_TIMEOUT_S, 1),
        include=parse_tool_filter(env.get("BENCHMARK_INCLUDE")),
        exclude=parse_tool_filter(env.get("BENCHMARK_EXCLUDE")),
        output_dir=Path(env.get("BENCHMARK_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)),
        workdir=Path(env.get("BENCHMARK_WORKDIR", DEFAULT_WORKDIR)),
        project_root=Path(env.get("BENCHMARK_PROJECT_ROOT", DEFAULT_PROJECT_ROOT)),
        platform=env.get("PLATFORM", "Ubuntu"),
        python_version=env.get("PYTHON_VERSION", platform_python_version()),
    )


# RETURNS THE CURRENT PYTHON MAJOR.MINOR VERSION
def platform_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


# NORMALIZES A VALUE FOR FILE AND DIRECTORY NAMES
def slugify(value: str) -> str:
    chars = [char.lower() if char.isalnum() else "-" for char in value.strip()]
    slug = "".join(chars).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "unknown"


# RETURNS THE PUBLIC CLI NAME FOR A TOOL PACKAGE
def public_tool_name(tool_name: str) -> str:
    return "test" if tool_name == "autotest" else tool_name


# DECIDES WHETHER A TOOL MATCHES INCLUDE AND EXCLUDE FILTERS
def should_run_tool(tool_name: str, public_name: str, include: Set[str], exclude: Set[str]) -> bool:
    if include and tool_name not in include and public_name not in include: return False
    if tool_name in exclude or public_name in exclude: return False
    return True


# DISCOVERS BENCHMARK CASES FROM TOOL SMOKE DEFINITIONS
def discover_benchmark_cases(config: BenchmarkConfig) -> List[Dict[str, Any]]:
    entries = discover_tool_command_entries()
    exclude = set(config.exclude)

    if "autotest" not in config.include and "test" not in config.include: exclude.update({"autotest", "test"})

    cases: List[Dict[str, Any]] = []
    case_root = config.workdir / "case-data"

    for tool_name in sorted(entries):
        mod, cmd = entries[tool_name]
        public_name = public_tool_name(tool_name)

        if not should_run_tool(tool_name, public_name, config.include, exclude): continue

        tool_dir = case_root / tool_name
        tool_dir.mkdir(parents=True, exist_ok=True)

        smoke_tests = _normalize_smoke_tests(getattr(mod, "SMOKE_TESTS", None))
        if not smoke_tests: smoke_tests = [_build_default_case(tool_name, cmd, tool_dir)]

        for case_name, args in smoke_tests:
            cases.append(
                {
                    "category": get_tool_category(mod),
                    "tool": public_name,
                    "tool_package": tool_name,
                    "case": case_name,
                    "args": list(args),
                }
            )

    return cases


# CHECKS WHETHER AN ARGUMENT LOOKS LIKE A FILESYSTEM PATH
def looks_like_path_arg(value: str) -> bool:
    if not value: return False
    path = Path(value)
    return (
        value.startswith(("/", "\\", "./", "../"))
        or "/" in value
        or "\\" in value
        or bool(path.suffix)
    )


# PREPARES CASE ARGUMENTS INSIDE AN ISOLATED ITERATION DIRECTORY
def prepare_case_args(args: Sequence[str], iteration_dir: Path, project_root: Path) -> List[str]:
    prepared: List[str] = []
    input_dir = iteration_dir / "inputs"
    output_dir = iteration_dir / "outputs"

    for arg in args:
        path_arg = Path(arg)
        source = path_arg if path_arg.is_absolute() else project_root / path_arg

        if source.is_file():
            input_dir.mkdir(parents=True, exist_ok=True)
            dest = input_dir / path_arg.name
            shutil.copy2(source, dest)
            prepared.append(str(dest))
            continue

        if looks_like_path_arg(arg):
            output_dir.mkdir(parents=True, exist_ok=True)
            filename = path_arg.name or "output"
            prepared.append(str(output_dir / filename))
            continue

        prepared.append(arg)

    return prepared


# BUILDS THE SUBPROCESS ENVIRONMENT FOR BENCHMARK COMMANDS
def benchmark_env(project_root: Path) -> Dict[str, str]:
    env = dict(os.environ)
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(project_root)
        if not existing_pythonpath
        else os.pathsep.join([str(project_root), existing_pythonpath])
    )
    env["CI"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.setdefault("TERM", "dumb")
    return env


# RUNS ONE CLI SUBPROCESS AND CAPTURES ITS DURATION AND OUTPUT
def run_subprocess(argv: Sequence[str], timeout_s: int, cwd: Path, env: Dict[str, str]) -> Dict[str, Any]:
    start = time.perf_counter()

    try:
        completed = subprocess.run(
            list(argv),
            cwd=str(cwd),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_s,
        )
        duration_s = time.perf_counter() - start
        output = completed.stdout or ""
        status = "OK" if completed.returncode == 0 else "FAIL"
        return {
            "status": status,
            "returncode": completed.returncode,
            "duration_s": round(duration_s, 6),
            "output": truncate_output(output) if status != "OK" else "",
        }
    except subprocess.TimeoutExpired as exc:
        duration_s = time.perf_counter() - start
        output = exc.stdout or ""
        if isinstance(output, bytes): output = output.decode("utf-8", errors="replace")
        return {
            "status": "TIMEOUT",
            "returncode": 124,
            "duration_s": round(duration_s, 6),
            "output": truncate_output(output),
        }


# TRUNCATES FAILURE OUTPUT STORED IN REPORTS
def truncate_output(output: str, limit: int = 2000) -> str:
    if len(output) <= limit: return output
    return output[:limit] + "\n... output truncated ..."


# CALCULATES SUMMARY STATISTICS FOR SUCCESSFUL RUN DURATIONS
def summarize_durations(durations_s: Sequence[float]) -> Dict[str, Any]:
    if not durations_s:
        return {
            "count": 0,
            "min_ms": 0.0,
            "mean_ms": 0.0,
            "median_ms": 0.0,
            "p95_ms": 0.0,
            "max_ms": 0.0,
        }

    durations_ms = sorted(duration * 1000 for duration in durations_s)
    p95_index = max(0, math.ceil(len(durations_ms) * 0.95) - 1)

    return {
        "count": len(durations_ms),
        "min_ms": round(durations_ms[0], 3),
        "mean_ms": round(statistics.mean(durations_ms), 3),
        "median_ms": round(statistics.median(durations_ms), 3),
        "p95_ms": round(durations_ms[p95_index], 3),
        "max_ms": round(durations_ms[-1], 3),
    }


# RUNS ONE BENCHMARK CASE WITH WARMUP AND MEASURED ITERATIONS
def run_case(case: Dict[str, Any], config: BenchmarkConfig, run_root: Path) -> Dict[str, Any]:
    runs: List[Dict[str, Any]] = []
    warmups: List[Dict[str, Any]] = []
    total_runs = config.warmup + config.iterations
    env = benchmark_env(config.project_root)

    print(f"- {case['tool']} / {case['case']} ({total_runs} runs)")

    for index in range(total_runs):
        is_warmup = index < config.warmup
        phase = "warmup" if is_warmup else "iteration"
        phase_index = index + 1 if is_warmup else index - config.warmup + 1
        iteration_dir = run_root / case["tool_package"] / case["case"] / f"{phase}-{phase_index}"
        iteration_dir.mkdir(parents=True, exist_ok=True)

        args = prepare_case_args(case["args"], iteration_dir, config.project_root)
        argv = [sys.executable, "-m", "autotools.cli", case["tool"], *args]
        result = run_subprocess(argv, config.timeout_s, iteration_dir, env)
        result.update({"phase": phase, "index": phase_index, "cmd": argv})

        marker = "." if result["status"] == "OK" else "x"
        print(marker, end="", flush=True)

        if is_warmup:
            warmups.append(result)
        else:
            runs.append(result)

    print()

    successful_durations = [run["duration_s"] for run in runs if run["status"] == "OK"]
    failed_runs = [run for run in runs + warmups if run["status"] != "OK"]

    return {
        "category": case["category"],
        "tool": case["tool"],
        "case": case["case"],
        "args": case["args"],
        "status": "OK" if not failed_runs else "FAIL",
        "stats": summarize_durations(successful_durations),
        "warmups": warmups,
        "runs": runs,
        "failures": failed_runs,
    }


# BUILDS THE JSON-SERIALIZABLE BENCHMARK REPORT
def build_report(config: BenchmarkConfig, results: List[Dict[str, Any]], started_at: str, finished_at: str) -> Dict[str, Any]:
    failed_cases = [result for result in results if result["status"] != "OK"]

    return {
        "metadata": {
            "started_at": started_at,
            "finished_at": finished_at,
            "platform": config.platform,
            "python_version": config.python_version,
            "iterations": config.iterations,
            "warmup": config.warmup,
            "timeout_s": config.timeout_s,
            "include": sorted(config.include),
            "exclude": sorted(config.exclude),
            "project_root": str(config.project_root),
            "case_count": len(results),
            "failed_case_count": len(failed_cases),
        },
        "results": results,
    }


# WRITES JSON AND MARKDOWN BENCHMARK REPORTS
def write_reports(report: Dict[str, Any], output_dir: Path) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    platform_slug = slugify(report["metadata"].get("platform", "unknown"))
    json_path = output_dir / f"benchmark-{platform_slug}-{stamp}.json"
    markdown_path = output_dir / f"benchmark-{platform_slug}-{stamp}.md"

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown_report(report), encoding="utf-8")

    return {"json": str(json_path), "markdown": str(markdown_path)}


# RENDERS A MARKDOWN SUMMARY REPORT
def render_markdown_report(report: Dict[str, Any]) -> str:
    metadata = report["metadata"]
    lines = [
        "# Open-AutoTools CLI Benchmark",
        "",
        f"- Started: {metadata['started_at']}",
        f"- Finished: {metadata['finished_at']}",
        f"- Platform: {metadata['platform']}",
        f"- Python: {metadata['python_version']}",
        f"- Iterations: {metadata['iterations']}",
        f"- Warmup: {metadata['warmup']}",
        f"- Timeout: {metadata['timeout_s']}s",
        "",
        "| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for result in report["results"]:
        stats = result["stats"]
        lines.append(
            "| {category} | {tool} | {case} | {status} | {count} | {min_ms:.3f} | "
            "{mean_ms:.3f} | {median_ms:.3f} | {p95_ms:.3f} | {max_ms:.3f} |".format(
                category=result["category"],
                tool=result["tool"],
                case=result["case"],
                status=result["status"],
                **stats,
            )
        )

    lines.append("")

    failed = [result for result in report["results"] if result["status"] != "OK"]
    if failed:
        lines.extend(["## Failed Cases", ""])
        for result in failed:
            lines.append(f"- {result['tool']} / {result['case']}")
        lines.append("")

    return "\n".join(lines)


# PRINTS A CONSOLE SUMMARY AFTER REPORTS ARE WRITTEN
def print_summary(report: Dict[str, Any], paths: Dict[str, str]) -> None:
    metadata = report["metadata"]
    print()
    print("Benchmark summary")
    print(f"Cases: {metadata['case_count']}")
    print(f"Failed cases: {metadata['failed_case_count']}")
    print(f"JSON report: {paths['json']}")
    print(f"Markdown report: {paths['markdown']}")


# RUNS ALL SELECTED BENCHMARK CASES AND RETURNS A REPORT
def run_benchmarks(config: BenchmarkConfig) -> Dict[str, Any]:
    started_at = datetime.now(timezone.utc).isoformat()
    run_root = config.workdir / datetime.now(timezone.utc).strftime("run-%Y%m%dT%H%M%SZ")
    run_root.mkdir(parents=True, exist_ok=True)

    cases = discover_benchmark_cases(config)
    if not cases:
        raise RuntimeError("No benchmark cases selected")

    print("Running Open-AutoTools CLI benchmarks")
    print(f"Platform: {config.platform}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Iterations: {config.iterations}")
    print(f"Warmup: {config.warmup}")
    print(f"Timeout: {config.timeout_s}s")
    print(f"Cases: {len(cases)}")
    print()

    results = [run_case(case, config, run_root) for case in cases]
    finished_at = datetime.now(timezone.utc).isoformat()
    return build_report(config, results, started_at, finished_at)


# CLI ENTRYPOINT FOR THE DOCKER BENCHMARK RUNNER
def main() -> int:
    try:
        config = load_config()
        report = run_benchmarks(config)
        paths = write_reports(report, config.output_dir)
        print_summary(report, paths)
        return 1 if report["metadata"]["failed_case_count"] else 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
