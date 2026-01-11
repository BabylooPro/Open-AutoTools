# Performance Metrics

Open-AutoTools includes comprehensive performance metrics to help developers understand execution characteristics and identify bottlenecks.

## Overview

Performance metrics are automatically collected during command execution and provide detailed insights into:

-   Execution timing
-   CPU usage
-   Memory consumption
-   Garbage collection activity
-   Filesystem I/O operations
-   Step-by-step breakdown

## Metrics Collected

### Duration Metrics

-   **total_duration_ms**: Total execution time from process start to exit
-   **startup_duration_ms**: Time until command execution begins (runtime initialization, config loading)
-   **command_duration_ms**: Actual command execution time (excluding startup/shutdown)

### CPU Metrics

-   **cpu_time_total_ms**: Total CPU time (user + system)
-   **cpu_user_ms**: User CPU time
-   **cpu_sys_ms**: System CPU time
-   **cpu_usage_ratio**: CPU usage percentage (CPU time / total duration)

### Memory Metrics

-   **rss_mb_peak**: Peak resident set size (RSS) in megabytes
-   **alloc_mb_total**: Total memory allocations tracked via tracemalloc

### Garbage Collection Metrics

-   **gc_pause_total_ms**: Total time spent in garbage collection pauses
-   **gc_collections_count**: Number of GC collections performed

### Filesystem I/O Metrics

-   **fs_bytes_read_total**: Total bytes read from disk
-   **fs_bytes_written_total**: Total bytes written to disk
-   **fs_ops_count**: Total filesystem operations (reads + writes)

### Step Breakdown

-   **top_slowest_steps**: List of the slowest execution steps with their durations

## Enabling Performance Metrics

### Development Mode

Performance metrics are **automatically enabled** when running in development mode (when the package is installed with `pip install -e .` or when running from source).

### Production Mode

In production installations, metrics are disabled by default. Enable them using the `--perf` flag:

```bash
# Using the flag on the main command
autotools --perf autocaps "hello world"

# Or directly on the subcommand
autocaps --perf "hello world"
```

The `--perf` flag works on both the main `autotools` command and directly on subcommands.

### Disabling Metrics

To disable metrics even in development mode, set the environment variable:

```bash
# Disable via environment variable
export AUTOTOOLS_DISABLE_PERF=1
autotools autocaps "hello world"

# Or inline
AUTOTOOLS_DISABLE_PERF=1 autotools autocaps "hello world"
```

Accepted values: `1`, `true`, `yes` (case-insensitive)

## Example Output

```
============================================================
PERFORMANCE METRICS
============================================================

DURATION METRICS:
  Total Duration:        1234.56 ms
  Startup Duration:      12.34 ms
  Command Duration:      1200.00 ms

CPU METRICS:
  CPU Time Total:        500.00 ms
  CPU User Time:         450.00 ms
  CPU System Time:       50.00 ms
  CPU Usage Ratio:       40.5%

MEMORY METRICS:
  RSS Peak:              64.52 MB
  Allocations Total:     6.20 MB

GARBAGE COLLECTION METRICS:
  GC Pause Total:        5.23 ms
  GC Collections:        22

FILESYSTEM I/O METRICS:
  Bytes Read:            1.5 MB
  Bytes Written:         0.2 MB
  Operations:            150

TOP SLOWEST STEPS:
  1. command_autocaps: 1200.00 ms
  2. startup: 12.34 ms
============================================================
```

## Implementation Details

### Dependencies

-   **psutil** (optional): Provides enhanced system metrics. Falls back to Python's `resource` module if unavailable.
-   **tracemalloc**: Built-in Python module for tracking memory allocations.

### Platform Compatibility

-   **Linux**: Uses `ru_maxrss` from `resource.getrusage()` (in KB)
-   **macOS**: Uses `ru_maxrss` from `resource.getrusage()` (in bytes)
-   **Windows**: Uses psutil when available

### Performance Impact

Metrics collection has minimal overhead:

-   Memory tracking: ~1-2% overhead
-   CPU tracking: Negligible (<0.1%)
-   I/O tracking: Only when psutil is available

## Use Cases

1. **Performance Debugging**: Identify slow operations and bottlenecks
2. **Resource Monitoring**: Track memory and CPU usage patterns
3. **Optimization**: Measure improvements after code changes
4. **CI/CD Integration**: Monitor performance regressions in automated tests

## Best Practices

1. Enable metrics during development to catch performance issues early
2. Use `--perf` flag in production only when investigating specific issues
3. Monitor `cpu_usage_ratio` to identify CPU-bound vs I/O-bound operations
4. Check `top_slowest_steps` to focus optimization efforts
5. Compare metrics across different runs to track improvements
