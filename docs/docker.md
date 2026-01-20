# Docker Support

Open-AutoTools can be tested across multiple platforms using Docker containers.

## Usage

```bash
# Go to docker directory
cd docker

# Run the full matrix locally (DEFAULT)
# (3.10 -> 3.14) x (ubuntu/macos/windows)
docker-compose build
docker-compose up

# Build and run tests with a specific Python version (ex: 3.13, 3.14)
COMPOSE_PROFILES=single PYTHON_VERSION=3.13 docker-compose build
COMPOSE_PROFILES=single PYTHON_VERSION=3.13 docker-compose up

# Run a single matrix service (example: Ubuntu / Python 3.14)
docker-compose up ubuntu-py314

# Test specific platform
COMPOSE_PROFILES=single docker-compose up ubuntu    # For Ubuntu
COMPOSE_PROFILES=single docker-compose up macos     # For macOS
COMPOSE_PROFILES=single docker-compose up windows   # For Windows

# Clean up
docker-compose down --remove-orphans
```

## Notes

-   **macos/windows services**: they run Linux containers (`python:X.Y-slim`) but set `PLATFORM` to exercise platform-specific code paths.
-   **Ubuntu Python patch versions**: Ubuntu images install `pythonX.Y` via deadsnakes on Ubuntu 24.04, so patch versions can differ (example: 3.12.3). Slim images use official `python:X.Y-slim` (example: 3.12.x).
-   **Disk usage**: if Docker Desktop runs out of space, prune build cache and dangling images:

```bash
docker system df
docker builder prune -af
docker image prune -af
```

## Smoke tests (auto-discovery)

Docker runs the CLI smoke runner (`autotools smoke`). It **auto-detects tools**, so you **do not** need to edit `docker/run_tests.sh` when you add a new tool.

### Adding a new tool to smoke

-   **Required**: add a package `autotools/<tool>/` with a `commands.py` that exposes a `@click.command()` (the command name should match the folder name).
-   **Recommended**: define `SMOKE_TESTS` in `autotools/<tool>/commands.py` so the smoke test is deterministic (otherwise it will try a best-effort default invocation).

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

## Platform Support

Each platform-specific container includes:

-   Python environment (matrix: 3.10 -> 3.14, single-profile default: 3.12, configurable with `PYTHON_VERSION`)
-   All required dependencies (FFmpeg, Java, etc.)
-   Automated test suite
-   Volume mapping for persistent data

> **Note:** The Docker setup is primarily for testing and development. For regular use, install via pip as described in [installation.md](installation.md).
