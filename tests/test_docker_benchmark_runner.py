import importlib.util
import json
import sys
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "docker" / "benchmark_runner.py"
SPEC = importlib.util.spec_from_file_location("docker_benchmark_runner", MODULE_PATH)
benchmark_runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = benchmark_runner
SPEC.loader.exec_module(benchmark_runner)


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
    assert benchmark_runner.slugify("") == "unknown"


# TEST FOR INPUT COPYING AND OUTPUT PATH ISOLATION
def test_prepare_case_args_copies_inputs_and_isolates_outputs(tmp_path):
    project_root = tmp_path / "project"
    project_root.mkdir()
    (project_root / "README.md").write_text("# docs\n", encoding="utf-8")

    iteration_dir = tmp_path / "run"
    args = ["README.md", "/tmp/autoconvert-smoke.json", "--format", "json", "plain"]

    prepared = benchmark_runner.prepare_case_args(args, iteration_dir, project_root)

    copied_input = iteration_dir / "inputs" / "README.md"
    isolated_output = iteration_dir / "outputs" / "autoconvert-smoke.json"

    assert copied_input.read_text(encoding="utf-8") == "# docs\n"
    assert prepared == [str(copied_input), str(isolated_output), "--format", "json", "plain"]


# TEST FOR JSON AND MARKDOWN REPORT WRITING
def test_write_reports_creates_json_and_markdown(tmp_path):
    report = {
        "metadata": {
            "started_at": "2026-01-01T00:00:00+00:00",
            "finished_at": "2026-01-01T00:00:01+00:00",
            "platform": "Ubuntu",
            "python_version": "3.12",
            "iterations": 2,
            "warmup": 1,
            "timeout_s": 30,
            "include": ["autocaps"],
            "exclude": [],
            "project_root": "/app",
            "case_count": 1,
            "failed_case_count": 0,
        },
        "results": [
            {
                "category": "Text",
                "tool": "autocaps",
                "case": "basic",
                "status": "OK",
                "stats": {
                    "count": 2,
                    "min_ms": 1.0,
                    "mean_ms": 1.5,
                    "median_ms": 1.5,
                    "p95_ms": 2.0,
                    "max_ms": 2.0,
                },
            }
        ],
    }

    paths = benchmark_runner.write_reports(report, tmp_path)

    json_report = Path(paths["json"])
    markdown_report = Path(paths["markdown"])

    assert json_report.name.startswith("benchmark-ubuntu-")
    assert markdown_report.name.startswith("benchmark-ubuntu-")
    assert json.loads(json_report.read_text(encoding="utf-8"))["metadata"]["case_count"] == 1
    assert "| Text | autocaps | basic | OK | 2 |" in markdown_report.read_text(encoding="utf-8")
