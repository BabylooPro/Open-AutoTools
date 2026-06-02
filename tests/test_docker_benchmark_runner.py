import importlib.util
import json
import sys
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "docker" / "benchmarks" / "benchmark_runner.py"
MODULE_DIR = str(MODULE_PATH.parent)
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

SPEC = importlib.util.spec_from_file_location("docker_benchmark_runner", MODULE_PATH)
benchmark_runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = benchmark_runner
SPEC.loader.exec_module(benchmark_runner)


# BUILDS A MINIMAL BENCHMARK REPORT FOR REPORT WRITING TESTS
def make_benchmark_report(
    run_id,
    platform,
    python_version="3.12",
    status="OK",
    mean_ms=1.5,
    p95_ms=2.0,
    max_ms=2.0,
):
    failed_case_count = 0 if status == "OK" else 1

    return {
        "metadata": {
            "started_at": "2026-01-01T00:00:00+00:00",
            "finished_at": "2026-01-01T00:00:01+00:00",
            "platform": platform,
            "python_version": python_version,
            "iterations": 2,
            "warmup": 1,
            "timeout_s": 30,
            "include": ["autocaps"],
            "exclude": [],
            "project_root": "/app",
            "run_id": run_id,
            "case_count": 1,
            "failed_case_count": failed_case_count,
        },
        "results": [
            {
                "category": "Text",
                "tool": "autocaps",
                "case": "basic",
                "status": status,
                "stats": {
                    "count": 2,
                    "min_ms": 1.0,
                    "mean_ms": mean_ms,
                    "median_ms": mean_ms,
                    "p95_ms": p95_ms,
                    "max_ms": max_ms,
                },
            }
        ],
    }


# TEST FOR BENCHMARK ENVIRONMENT PARSING
def test_load_config_parses_benchmark_env(tmp_path):
    config = benchmark_runner.load_config(
        {
            "BENCHMARK_ITERATIONS": "3",
            "BENCHMARK_WARMUP": "0",
            "BENCHMARK_TIMEOUT": "12",
            "BENCHMARK_INCLUDE": "autocaps, autolower",
            "BENCHMARK_EXCLUDE": "autoip autotest",
            "BENCHMARK_OUTPUT_DIR": str(tmp_path / "reports"),
            "BENCHMARK_WORKDIR": str(tmp_path / "work"),
            "BENCHMARK_PROJECT_ROOT": str(tmp_path / "project"),
            "BENCHMARK_RUN_ID": "run_01",
            "PLATFORM": "Ubuntu",
            "PYTHON_VERSION": "3.12",
        }
    )

    assert config.iterations == 3
    assert config.warmup == 0
    assert config.timeout_s == 12
    assert config.include == {"autocaps", "autolower"}
    assert config.exclude == {"autoip", "autotest"}
    assert config.output_dir == tmp_path / "reports"
    assert config.workdir == tmp_path / "work"
    assert config.project_root == tmp_path / "project"
    assert config.run_id == "run_01"


# TEST FOR SEQUENTIAL RUN ID ASSIGNMENT
def test_next_sequential_run_id_increments_highest(tmp_path):
    assert benchmark_runner.next_sequential_run_id(tmp_path) == "run_01"

    (tmp_path / "run_01").mkdir()
    (tmp_path / "run_02").mkdir()
    (tmp_path / "run_09").mkdir()
    (tmp_path / "final_result.json").write_text("{}", encoding="utf-8")

    assert benchmark_runner.next_sequential_run_id(tmp_path) == "run_10"


# TEST FOR AUTO-ASSIGNED RUN ID WHEN BENCHMARK_RUN_ID IS UNSET
def test_load_config_auto_assigns_sequential_run_id(tmp_path):
    output_dir = tmp_path / "reports"
    output_dir.mkdir()
    (output_dir / "run_01").mkdir()

    config = benchmark_runner.load_config({"BENCHMARK_OUTPUT_DIR": str(output_dir)})

    assert config.run_id == "run_02"


# TEST FOR INVALID INTEGER ENVIRONMENT VALUES
@pytest.mark.parametrize(
    "name,raw_value,minimum",
    [
        ("BENCHMARK_ITERATIONS", "0", 1),
        ("BENCHMARK_TIMEOUT", "fast", 1),
    ],
)
def test_parse_int_env_rejects_invalid_values(name, raw_value, minimum):
    with pytest.raises(ValueError):
        benchmark_runner.parse_int_env({name: raw_value}, name, 5, minimum)


# TEST FOR DURATION SUMMARY STATISTICS
def test_summarize_durations_uses_milliseconds_and_nearest_rank_p95():
    summary = benchmark_runner.summarize_durations([0.001, 0.002, 0.003, 0.004])

    assert summary == {
        "count": 4,
        "min_ms": 1.0,
        "mean_ms": 2.5,
        "median_ms": 2.5,
        "p95_ms": 4.0,
        "max_ms": 4.0,
    }


# TEST FOR PLATFORM SLUG NORMALIZATION
def test_slugify_normalizes_platform_names():
    assert benchmark_runner.slugify("macOS") == "macos"
    assert benchmark_runner.slugify("Windows 11") == "windows-11"
    assert benchmark_runner.slugify("run_01") == "run_01"
    assert benchmark_runner.slugify("") == "unknown"


# TEST FOR INPUT COPYING AND OUTPUT PATH ISOLATION
def test_prepare_case_args_copies_inputs_and_isolates_outputs(tmp_path):
    project_root = tmp_path / "project"
    project_root.mkdir()
    (project_root / "README.md").write_text("# docs\n", encoding="utf-8")

    iteration_dir = tmp_path / "run"
    requested_output = tmp_path / "requested-output" / "autoconvert-smoke.json"
    args = ["README.md", str(requested_output), "--format", "json", "plain"]

    prepared = benchmark_runner.prepare_case_args(args, iteration_dir, project_root)

    copied_input = iteration_dir / "inputs" / "README.md"
    isolated_output = iteration_dir / "outputs" / "autoconvert-smoke.json"

    assert copied_input.read_text(encoding="utf-8") == "# docs\n"
    assert prepared == [str(copied_input), str(isolated_output), "--format", "json", "plain"]


# TEST FOR JSON AND MARKDOWN REPORT WRITING
def test_write_reports_creates_json_and_markdown(tmp_path):
    report = make_benchmark_report("run_01", "Ubuntu")

    paths = benchmark_runner.write_reports(report, tmp_path)

    json_report = Path(paths["json"])
    markdown_report = Path(paths["markdown"])

    assert json_report == tmp_path / "run_01" / "ubuntu" / "benchmark.json"
    assert markdown_report == tmp_path / "run_01" / "ubuntu" / "benchmark.md"
    assert json.loads(json_report.read_text(encoding="utf-8"))["metadata"]["case_count"] == 1
    markdown = markdown_report.read_text(encoding="utf-8")
    assert "- Run: run_01" in markdown
    assert "| Text | autocaps | basic | OK | 2 |" in markdown


# TEST FOR FINAL RESULT WRITING ACROSS EXISTING RUNNER REPORTS
def test_write_reports_updates_final_result_for_all_existing_runners(tmp_path):
    benchmark_runner.write_reports(make_benchmark_report("run_01", "Ubuntu"), tmp_path)
    paths = benchmark_runner.write_reports(
        make_benchmark_report("run_01", "Windows", status="FAIL", mean_ms=3.0, p95_ms=4.0, max_ms=5.0),
        tmp_path,
    )

    final_json = Path(paths["final_json"])
    final_markdown = Path(paths["final_markdown"])
    final_result = json.loads(final_json.read_text(encoding="utf-8"))

    assert final_json == tmp_path / "final_result.json"
    assert final_markdown == tmp_path / "final_result.md"
    assert final_result["metadata"]["report_count"] == 2
    assert final_result["metadata"]["runner_count"] == 2
    assert final_result["metadata"]["case_count"] == 2
    assert final_result["metadata"]["failed_case_count"] == 1
    assert {report["runner"] for report in final_result["reports"]} == {
        "Ubuntu Python 3.12",
        "Windows Python 3.12",
    }
    assert len(final_result["results"]) == 2

    markdown = final_markdown.read_text(encoding="utf-8")
    assert "# Open-AutoTools Benchmark Diff" in markdown
    assert "## Global Runner Diff" in markdown
    assert "## Diff By Run" in markdown
    assert "## Biggest Case Gaps" in markdown
    assert "## Case Results" not in markdown
    assert "| Windows Python 3.12 | 1 | 1 | 1 | 3.000 | 3.000 | 4.000 | 5.000 | +1.500 | +100.0% |" in markdown
    assert "| run_01 | Ubuntu Python 3.12 | Windows Python 3.12 | 3.000 | +1.500 | +100.0% | 1 |" in markdown
    assert "| run_01 | autocaps / basic | Ubuntu Python 3.12 (1.500) | Windows Python 3.12 (3.000) | 1.500 | +100.0% |" in markdown
