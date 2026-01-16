# Docker Support

Open-AutoTools can be tested across multiple platforms using Docker containers.

## Usage

```bash
# Go to docker directory
cd docker

# Build and run tests for all platforms
docker-compose build
docker-compose up

# Test specific platform
docker-compose up ubuntu    # For Ubuntu
docker-compose up macos     # For macOS
docker-compose up windows   # For Windows

# Clean up
docker-compose down --remove-orphans
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

-   Python 3.11/3.12 environment
-   All required dependencies (FFmpeg, Java, etc.)
-   Automated test suite
-   Volume mapping for persistent data

> **Note:** The Docker setup is primarily for testing and development. For regular use, install via pip as described in [installation.md](installation.md).
