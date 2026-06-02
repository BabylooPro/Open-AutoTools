from __future__ import annotations

import json
import os
import time

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


FINAL_RESULT_JSON = "final_result.json"
FINAL_RESULT_MARKDOWN = "final_result.md"
TOP_CASE_GAP_COUNT = 10


# WRITES TEXT THROUGH A TEMPORARY FILE BEFORE REPLACING THE DESTINATION
def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp")
    temp_path.write_text(content, encoding="utf-8")
    temp_path.replace(path)


# RETURNS A POSIX-LIKE PATH RELATIVE TO THE BENCHMARK OUTPUT DIRECTORY
def relative_report_path(output_dir: Path, path: Path) -> str:
    try:
        return path.relative_to(output_dir).as_posix()
    except ValueError:
        return path.as_posix()


# FINDS ALL PER-RUNNER BENCHMARK JSON REPORTS UNDER THE OUTPUT DIRECTORY
def benchmark_report_paths(output_dir: Path) -> List[Path]:
    if not output_dir.exists(): return []
    return sorted(path for path in output_dir.rglob("benchmark.json") if path.is_file())


# LOADS EXISTING PER-RUNNER REPORTS AND SKIPS REPORTS STILL BEING WRITTEN
def load_existing_benchmark_reports(output_dir: Path) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    skipped: List[Dict[str, str]] = []

    for path in benchmark_report_paths(output_dir):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            skipped.append({"path": relative_report_path(output_dir, path), "error": str(exc)})
            continue

        if not isinstance(report, dict) or not isinstance(report.get("metadata"), dict):
            skipped.append({"path": relative_report_path(output_dir, path), "error": "invalid benchmark report"})
            continue

        entries.append({"path": path, "report": report})

    entries.sort(key=benchmark_report_sort_key)
    return {"entries": entries, "skipped": skipped}


# SORTS REPORT ENTRIES BY RUN, RUNNER, PYTHON VERSION, THEN PATH
def benchmark_report_sort_key(entry: Dict[str, Any]) -> tuple[str, str, str, str]:
    report = entry["report"]
    metadata = report["metadata"]
    return (
        str(metadata.get("run_id", "")),
        str(metadata.get("platform", "")),
        str(metadata.get("python_version", "")),
        str(entry["path"]),
    )


# BUILDS A COMPACT SUMMARY FOR ONE PER-RUNNER REPORT
def summarize_report_entry(entry: Dict[str, Any], output_dir: Path) -> Dict[str, Any]:
    path = entry["path"]
    report = entry["report"]
    metadata = report["metadata"]
    platform = str(metadata.get("platform", "unknown"))
    python_version = str(metadata.get("python_version", "unknown"))
    failed_case_count = int(metadata.get("failed_case_count") or 0)

    return {
        "run_id": str(metadata.get("run_id", "unknown")),
        "runner": f"{platform} Python {python_version}",
        "platform": platform,
        "python_version": python_version,
        "status": "OK" if failed_case_count == 0 else "FAIL",
        "started_at": str(metadata.get("started_at", "")),
        "finished_at": str(metadata.get("finished_at", "")),
        "case_count": int(metadata.get("case_count") or 0),
        "failed_case_count": failed_case_count,
        "report_path": relative_report_path(output_dir, path),
    }


# BUILDS A COMPACT SUMMARY FOR ONE BENCHMARK CASE RESULT
def summarize_result_entry(summary: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    stats = result.get("stats") if isinstance(result.get("stats"), dict) else {}

    return {
        "run_id": summary["run_id"],
        "runner": summary["runner"],
        "platform": summary["platform"],
        "python_version": summary["python_version"],
        "category": result.get("category", ""),
        "tool": result.get("tool", ""),
        "case": result.get("case", ""),
        "status": result.get("status", ""),
        "count": stats.get("count", 0),
        "min_ms": stats.get("min_ms", 0.0),
        "mean_ms": stats.get("mean_ms", 0.0),
        "median_ms": stats.get("median_ms", 0.0),
        "p95_ms": stats.get("p95_ms", 0.0),
        "max_ms": stats.get("max_ms", 0.0),
    }


# BUILDS THE FINAL BENCHMARK RESULT FROM ALL EXISTING PER-RUNNER REPORTS
def build_final_result(output_dir: Path, generated_at: str) -> Dict[str, Any]:
    loaded = load_existing_benchmark_reports(output_dir)
    reports: List[Dict[str, Any]] = []
    results: List[Dict[str, Any]] = []

    for entry in loaded["entries"]:
        summary = summarize_report_entry(entry, output_dir)
        reports.append(summary)

        report_results = entry["report"].get("results", [])
        if not isinstance(report_results, list): continue

        for result in report_results:
            if isinstance(result, dict):
                results.append(summarize_result_entry(summary, result))

    run_ids = sorted({report["run_id"] for report in reports})
    runners = sorted({report["runner"] for report in reports})
    platforms = sorted({report["platform"] for report in reports})
    python_versions = sorted({report["python_version"] for report in reports})

    return {
        "metadata": {
            "generated_at": generated_at,
            "output_dir": str(output_dir),
            "report_count": len(reports),
            "run_count": len(run_ids),
            "runner_count": len(runners),
            "case_count": sum(report["case_count"] for report in reports),
            "failed_case_count": sum(report["failed_case_count"] for report in reports),
            "result_count": len(results),
            "skipped_report_count": len(loaded["skipped"]),
            "runs": run_ids,
            "runners": runners,
            "platforms": platforms,
            "python_versions": python_versions,
        },
        "reports": reports,
        "results": results,
        "runner_drift": runner_drift_stats(results, run_ids),
        "skipped_reports": loaded["skipped"],
    }


# WRITES THE FINAL RESULT FOR EVERY EXISTING RUNNER REPORT
def write_final_result(output_dir: Path) -> Dict[str, str]:
    final_result = build_final_result(output_dir, datetime.now(timezone.utc).isoformat())
    json_path = output_dir / FINAL_RESULT_JSON
    markdown_path = output_dir / FINAL_RESULT_MARKDOWN

    atomic_write_text(json_path, json.dumps(final_result, indent=2, ensure_ascii=False) + "\n")
    atomic_write_text(markdown_path, render_final_markdown_report(final_result))

    return {"final_json": str(json_path), "final_markdown": str(markdown_path)}


# ESCAPES VALUES FOR MARKDOWN TABLE CELLS
def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


# RETURNS A FLOAT VALUE OR 0.0 WHEN OLD REPORTS CONTAIN UNEXPECTED DATA
def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


# FORMATS A DIFF AGAINST A BASELINE VALUE
def format_diff(value: float, baseline: float) -> str:
    diff = value - baseline
    return f"{diff:+.3f}"


# FORMATS A PERCENT DIFF AGAINST A BASELINE VALUE
def format_percent_diff(value: float, baseline: float) -> str:
    if baseline <= 0: return "0.0%"
    return f"{((value - baseline) / baseline) * 100:+.1f}%"


# BUILDS AGGREGATED STATS BY RUNNER, OPTIONALLY LIMITED TO ONE RUN
def runner_stats(results: List[Dict[str, Any]], run_id: str | None = None) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}

    for result in results:
        if run_id is not None and result["run_id"] != run_id: continue

        runner = result["runner"]
        stats = grouped.setdefault(
            runner,
            {
                "runner": runner,
                "runs": set(),
                "cases": 0,
                "failed": 0,
                "mean_total_ms": 0.0,
                "p95_total_ms": 0.0,
                "max_ms": 0.0,
            },
        )

        stats["runs"].add(result["run_id"])
        stats["cases"] += 1
        if result["status"] != "OK": stats["failed"] += 1
        stats["mean_total_ms"] += safe_float(result["mean_ms"])
        stats["p95_total_ms"] += safe_float(result["p95_ms"])
        stats["max_ms"] = max(stats["max_ms"], safe_float(result["max_ms"]))

    rows: List[Dict[str, Any]] = []
    for stats in grouped.values():
        cases = stats["cases"]
        rows.append(
            {
                "runner": stats["runner"],
                "run_count": len(stats["runs"]),
                "case_count": cases,
                "failed_case_count": stats["failed"],
                "avg_mean_ms": stats["mean_total_ms"] / cases if cases else 0.0,
                "total_mean_ms": stats["mean_total_ms"],
                "avg_p95_ms": stats["p95_total_ms"] / cases if cases else 0.0,
                "max_ms": stats["max_ms"],
            }
        )

    return sorted(rows, key=lambda row: (row["avg_mean_ms"], row["runner"]))


# RETURNS THE BIGGEST FASTEST-TO-SLOWEST CASE GAPS ACROSS RUNNERS
def case_gap_stats(results: List[Dict[str, Any]], limit: int = TOP_CASE_GAP_COUNT) -> List[Dict[str, Any]]:
    grouped: Dict[tuple[str, str, str, str], List[Dict[str, Any]]] = {}

    for result in results:
        key = (
            result["run_id"],
            str(result["category"]),
            str(result["tool"]),
            str(result["case"]),
        )
        grouped.setdefault(key, []).append(result)

    rows: List[Dict[str, Any]] = []
    for (run_id, category, tool, case), case_results in grouped.items():
        if len(case_results) < 2: continue

        sorted_results = sorted(case_results, key=lambda result: safe_float(result["mean_ms"]))
        fastest = sorted_results[0]
        slowest = sorted_results[-1]
        fastest_mean = safe_float(fastest["mean_ms"])
        slowest_mean = safe_float(slowest["mean_ms"])
        if slowest_mean <= fastest_mean: continue

        rows.append(
            {
                "run_id": run_id,
                "category": category,
                "tool": tool,
                "case": case,
                "fastest_runner": fastest["runner"],
                "slowest_runner": slowest["runner"],
                "fastest_mean_ms": fastest_mean,
                "slowest_mean_ms": slowest_mean,
                "diff_ms": slowest_mean - fastest_mean,
                "diff_pct": ((slowest_mean - fastest_mean) / fastest_mean) * 100 if fastest_mean > 0 else 0.0,
            }
        )

    rows.sort(key=lambda row: (row["diff_pct"], row["diff_ms"]), reverse=True)
    return rows[:limit]


# RENDERS THE FINAL REPORT HEADER
def render_final_header(metadata: Dict[str, Any]) -> List[str]:
    return [
        "# Open-AutoTools Benchmark Diff",
        "",
        f"- Generated: {metadata['generated_at']}",
        f"- Reports: {metadata['report_count']} across {metadata['run_count']} runs",
        f"- Runners: {metadata['runner_count']}",
        f"- Case samples: {metadata['case_count']}",
        f"- Failed cases: {metadata['failed_case_count']}",
        "",
    ]


# RENDERS THE GLOBAL RUNNER DIFF SECTION
def render_global_runner_diff(results: List[Dict[str, Any]]) -> List[str]:
    rows = runner_stats(results)
    lines = ["## Global Runner Diff", ""]

    if not rows:
        lines.append("No benchmark results found.")
        return lines

    baseline = rows[0]["avg_mean_ms"]
    lines.extend(
        [
            "| Runner | Runs | Cases | Failed | Avg mean ms | Total mean ms | Avg P95 ms | Max ms | Diff ms | Diff % |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for row in rows:
        lines.append(
            "| {runner} | {run_count} | {case_count} | {failed_case_count} | "
            "{avg_mean_ms:.3f} | {total_mean_ms:.3f} | {avg_p95_ms:.3f} | {max_ms:.3f} | "
            "{diff_ms} | {diff_pct} |".format(
                runner=markdown_cell(row["runner"]),
                run_count=row["run_count"],
                case_count=row["case_count"],
                failed_case_count=row["failed_case_count"],
                avg_mean_ms=row["avg_mean_ms"],
                total_mean_ms=row["total_mean_ms"],
                avg_p95_ms=row["avg_p95_ms"],
                max_ms=row["max_ms"],
                diff_ms=format_diff(row["avg_mean_ms"], baseline),
                diff_pct=format_percent_diff(row["avg_mean_ms"], baseline),
            )
        )

    return lines


# BUILDS PER-RUNNER AVG MEAN MS FOR A SINGLE RUN, KEYED BY RUNNER
def runner_run_means(results: List[Dict[str, Any]], run_id: str) -> Dict[str, float]:
    return {row["runner"]: row["avg_mean_ms"] for row in runner_stats(results, run_id)}


# BUILDS RAW FIRST-VS-LAST RUN DRIFT PER RUNNER FOR PERSISTENCE AND RENDERING
def runner_drift_stats(results: List[Dict[str, Any]], run_ids: Any) -> Dict[str, Any]:
    if not isinstance(run_ids, list) or len(run_ids) < 2:
        return {"first_run": None, "last_run": None, "runners": []}

    first_run = str(run_ids[0])
    last_run = str(run_ids[-1])
    first_means = runner_run_means(results, first_run)
    last_means = runner_run_means(results, last_run)

    rows: List[Dict[str, Any]] = []
    for runner in sorted(set(first_means) & set(last_means)):
        first = first_means[runner]
        last = last_means[runner]
        rows.append(
            {
                "runner": runner,
                "first_avg_mean_ms": first,
                "last_avg_mean_ms": last,
                "diff_ms": last - first,
                "diff_pct": ((last - first) / first) * 100 if first > 0 else 0.0,
            }
        )

    return {"first_run": first_run, "last_run": last_run, "runners": rows}


# RENDERS THE FIRST-VS-LAST RUN DRIFT PER RUNNER
def render_runner_run_drift(results: List[Dict[str, Any]], run_ids: Any) -> List[str]:
    lines = ["## Runner Drift (First vs Last Run)", ""]
    drift = runner_drift_stats(results, run_ids)

    if not drift["runners"]:
        if drift["first_run"] is None:
            lines.append("Need at least two runs to compute drift.")
        else:
            lines.append("No runner present in both first and last run.")
        return lines

    lines.extend(
        [
            f"- First run: {drift['first_run']}",
            f"- Last run: {drift['last_run']}",
            "",
            "| Runner | First avg ms | Last avg ms | Diff ms | Diff % |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )

    for row in drift["runners"]:
        first = row["first_avg_mean_ms"]
        last = row["last_avg_mean_ms"]
        lines.append(
            "| {runner} | {first:.3f} | {last:.3f} | {diff_ms} | {diff_pct} |".format(
                runner=markdown_cell(row["runner"]),
                first=first,
                last=last,
                diff_ms=format_diff(last, first),
                diff_pct=format_percent_diff(last, first),
            )
        )

    return lines


# RENDERS ONE RUNNER DIFF ROW FOR A SINGLE RUN
def render_run_diff_row(run_id: str, fastest_runner: str, baseline: float, row: Dict[str, Any]) -> str:
    return "| {run_id} | {fastest} | {runner} | {avg_mean_ms:.3f} | {diff_ms} | {diff_pct} | {failed} |".format(
        run_id=markdown_cell(run_id),
        fastest=markdown_cell(fastest_runner),
        runner=markdown_cell(row["runner"]),
        avg_mean_ms=row["avg_mean_ms"],
        diff_ms=format_diff(row["avg_mean_ms"], baseline),
        diff_pct=format_percent_diff(row["avg_mean_ms"], baseline),
        failed=row["failed_case_count"],
    )


# RENDERS THE PER-RUN DIFF SECTION
def render_diff_by_run(results: List[Dict[str, Any]], run_ids: Any) -> List[str]:
    lines = [
        "## Diff By Run",
        "",
        "| Run | Fastest | Runner | Avg mean ms | Diff ms | Diff % | Failed |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    rows_written = False

    if isinstance(run_ids, list):
        for run_id in run_ids:
            rows = runner_stats(results, str(run_id))
            if not rows: continue

            fastest_runner = rows[0]["runner"]
            baseline = rows[0]["avg_mean_ms"]
            rows_written = True
            lines.extend(render_run_diff_row(str(run_id), fastest_runner, baseline, row) for row in rows)

    if not rows_written:
        lines.append("No run-level comparison available.")

    return lines


# RENDERS THE BIGGEST CASE GAPS SECTION
def render_biggest_case_gaps(results: List[Dict[str, Any]]) -> List[str]:
    gaps = case_gap_stats(results)
    lines = ["## Biggest Case Gaps", ""]

    if not gaps:
        lines.append("No case gap available.")
        return lines

    lines.extend(
        [
            "| Run | Case | Fastest | Slowest | Gap ms | Gap % |",
            "| --- | --- | --- | --- | ---: | ---: |",
        ]
    )

    for gap in gaps:
        lines.append(
            "| {run_id} | {case_name} | {fastest} ({fastest_ms:.3f}) | "
            "{slowest} ({slowest_ms:.3f}) | {diff_ms:.3f} | {diff_pct:+.1f}% |".format(
                run_id=markdown_cell(gap["run_id"]),
                case_name=markdown_cell(f"{gap['tool']} / {gap['case']}"),
                fastest=markdown_cell(gap["fastest_runner"]),
                fastest_ms=gap["fastest_mean_ms"],
                slowest=markdown_cell(gap["slowest_runner"]),
                slowest_ms=gap["slowest_mean_ms"],
                diff_ms=gap["diff_ms"],
                diff_pct=gap["diff_pct"],
            )
        )

    return lines


# RENDERS FAILED REPORTS WHEN ANY RUNNER HAS FAILURES
def render_failed_runner_reports(reports: List[Dict[str, Any]]) -> List[str]:
    failed_reports = [report for report in reports if report["failed_case_count"]]
    if not failed_reports: return []

    lines = [
        "## Failed Runner Reports",
        "",
        "| Run | Runner | Failed | Report |",
        "| --- | --- | ---: | --- |",
    ]
    for report in failed_reports:
        lines.append(
            "| {run_id} | {runner} | {failed} | {path} |".format(
                run_id=markdown_cell(report["run_id"]),
                runner=markdown_cell(report["runner"]),
                failed=report["failed_case_count"],
                path=markdown_cell(report["report_path"]),
            )
        )

    return lines


# RENDERS SKIPPED REPORTS WHEN SOME REPORTS COULD NOT BE READ
def render_skipped_reports(skipped: List[Dict[str, str]]) -> List[str]:
    if not skipped: return []

    lines = ["## Skipped Reports", ""]
    for report in skipped:
        lines.append(f"- {report['path']}: {report['error']}")
    return lines


# RENDERS THE FINAL MARKDOWN REPORT ACROSS ALL EXISTING RUNNERS
def render_final_markdown_report(final_result: Dict[str, Any]) -> str:
    metadata = final_result["metadata"]
    results = final_result["results"]
    sections = [
        render_final_header(metadata),
        render_global_runner_diff(results),
        render_runner_run_drift(results, metadata.get("runs", [])),
        render_diff_by_run(results, metadata.get("runs", [])),
        render_biggest_case_gaps(results),
        render_failed_runner_reports(final_result["reports"]),
        render_skipped_reports(final_result["skipped_reports"]),
    ]

    lines: List[str] = []
    for section in sections:
        if not section: continue
        if lines: lines.append("")
        lines.extend(section)
    lines.append("")
    return "\n".join(lines)
