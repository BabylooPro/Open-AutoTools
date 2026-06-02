# Docker Support

Open-AutoTools can be tested across multiple platforms using Docker containers.

## Usage

```bash
# Go to docker directory
cd docker

# Run full matrix (3.10 -> 3.14) x (ubuntu/macos/windows) concurrently (DEFAULT)
docker-compose build
docker-compose up

# Run single-version services (ubuntu/macos/windows) with default Python (3.12)
COMPOSE_PROFILES=single docker-compose build
COMPOSE_PROFILES=single docker-compose up

# Run single-version services with a specific Python version (example: 3.13, 3.14)
PYTHON_VERSION=3.13 COMPOSE_PROFILES=single docker-compose build
PYTHON_VERSION=3.13 COMPOSE_PROFILES=single docker-compose up

# Run a single matrix service (example: Ubuntu / Python 3.14)
docker-compose up ubuntu-py314

# Run the full matrix sequentially (LOWER DISK USAGE)
./run_matrix.sh

# Run only one platform in single-version mode (enable profile)
COMPOSE_PROFILES=single docker-compose up ubuntu    # For Ubuntu
COMPOSE_PROFILES=single docker-compose up macos     # For macOS
COMPOSE_PROFILES=single docker-compose up windows   # For Windows

# Clean up
docker-compose down --remove-orphans
```

## Notes

- **macos/windows services**: they run Linux containers (`python:X.Y-slim`) but set `PLATFORM` to exercise platform-specific code paths.
- **Ubuntu Python patch versions**: Ubuntu images install `pythonX.Y` via deadsnakes on Ubuntu 24.04, so patch versions can differ (example: 3.12.3). Slim images use official `python:X.Y-slim` (example: 3.12.x).
- **Disk usage**: if Docker Desktop runs out of space (example: `no space left on device` while exporting layers), prune build cache and dangling images:

```bash
docker system df
docker builder prune -af
docker image prune -af
docker volume prune -f
```

## Test suite + smoke tests

By default, each container runs:

- `autotools test` (full pytest suite + coverage)
- then `autotools smoke` (CLI smoke runner, auto-discovery)

You can disable either step:

```bash
# Skip full pytest suite, run smoke only
RUN_AUTOTOOLS_TEST=0 docker-compose up

# Skip smoke, run full pytest suite only
RUN_AUTOTOOLS_SMOKE=0 docker-compose up
```

The smoke runner (`autotools smoke`) **auto-detects tools**, so you **do not** need to edit `docker/run_tests.sh` when you add a new tool.

### Adding a new tool to smoke

- **Required**: add a package `autotools/<tool>/` with a `commands.py` that exposes a `@click.command()` (the command name should match the folder name).
- **Recommended**: define `SMOKE_TESTS` in `autotools/<tool>/commands.py` so the smoke test is deterministic (otherwise it will try a best-effort default invocation).

Example:

```python
# SMOKE TEST CASES (USED BY 'autotools smoke')
SMOKE_TESTS = [
    {"name": "basic", "args": ["hello", "world"]},
    {"name": "flags", "args": ["--some-flag"]},
]
```

To quickly verify:

```bash
# Lists detected tools
autotools list-tools

# Runs smoke only for one tool
autotools smoke --include <tool> --verbose
```

## CLI benchmarks

Open-AutoTools also includes a manual Docker-only benchmark runner. It executes real CLI
commands using the same tool discovery and `SMOKE_TESTS` scenarios as the smoke runner.
It does not run as part of the default Docker matrix or CI workflow.

```bash
# Run all benchmark cases on Ubuntu, macOS, and Windows services concurrently
docker compose -f docker/docker-compose.yml --profile benchmark up --build --abort-on-container-failure benchmark-ubuntu benchmark-macos benchmark-windows

# Quick focused run on all benchmark services
BENCHMARK_INCLUDE=autocaps BENCHMARK_ITERATIONS=2 docker compose -f docker/docker-compose.yml --profile benchmark up --build --abort-on-container-failure benchmark-ubuntu benchmark-macos benchmark-windows

# Run with an explicit folder name
BENCHMARK_RUN_ID=run_01 docker compose -f docker/docker-compose.yml --profile benchmark up --build --abort-on-container-failure benchmark-ubuntu benchmark-macos benchmark-windows

# Remove stopped benchmark containers after a run
docker compose -f docker/docker-compose.yml --profile benchmark down --remove-orphans
```

Reports are written under `docker/benchmarks/data/<run_id>/<platform>/`:

- JSON report for machine-readable results
- Markdown report for quick review

Configuration is environment-only:

- `BENCHMARK_ITERATIONS` (default: `5`)
- `BENCHMARK_WARMUP` (default: `1`)
- `BENCHMARK_TIMEOUT` (default: `30`)
- `BENCHMARK_INCLUDE` (comma- or space-separated tool names)
- `BENCHMARK_EXCLUDE` (comma- or space-separated tool names)
- `BENCHMARK_RUN_ID` (default: next sequential folder such as `run_06`)

The benchmark is informational. It does not enforce performance thresholds.

## Platform Support

Each platform-specific container includes:

- Python environment (default: 3.12, configurable with `PYTHON_VERSION`, matrix: 3.10 -> 3.14)
- All required dependencies (FFmpeg, Java, etc.)
- Automated test suite
- Volume mapping for persistent data

> **Note:** The Docker setup is primarily for testing and development. For regular use, install via pip as described in [installation.md](installation.md).
