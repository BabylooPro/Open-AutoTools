# Development

Open-AutoTools is developed using Python 3.10+.

## Setup Development Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows

# Install project dependencies
pip install -r requirements-dev.txt

# For development, install in editable mode
pip install -e .

# Or install dev extras (includes test/build tooling)
pip install -e ".[dev]"

# Build the package locally
python -m build  # Creates dist/Open_AutoTools-X.X.X-py3-none-any.whl

# Install from local wheel file
pip install dist/Open_AutoTools-X.X.X-py3-none-any.whl

# Check installation and development mode
autotools --version  # Should show "Development mode: enabled" when using pip install -e .
```

## Performance Metrics

Open-AutoTools includes built-in performance metrics that are automatically enabled in development mode. These metrics track:

-   **Duration Metrics**: Total, startup, and command execution times
-   **CPU Metrics**: User time, system time, and CPU usage ratio
-   **Memory Metrics**: RSS peak and total allocations
-   **Garbage Collection**: GC pause time and collection count
-   **Filesystem I/O**: Bytes read/written and operation count
-   **Top Slowest Steps**: Breakdown of the slowest execution steps

### Enabling/Disabling Performance Metrics

Performance metrics are **enabled by default in development mode** (when not installed via pip). In production, use the `--perf` flag to enable them:

```bash
# Enable metrics in production (on main command)
autotools --perf autocaps "hello world"

# Or directly on the subcommand
autocaps --perf "hello world"

# Disable metrics via environment variable
AUTOTOOLS_DISABLE_PERF=1 autotools autocaps "hello world"
```

The `--perf` flag works on both the main `autotools` command and directly on subcommands.

The metrics are displayed automatically at the end of command execution when enabled.

## Running Tests

See [testing.md](testing.md) and [tools/autotest.md](tools/autotest.md) for detailed information about running the test suite.

## Docker

If you want to run the cross-platform smoke suite without touching your local env:

-   More details: [docker.md](docker.md)
