import os
import sys
import pytest
import gc
import time
import tracemalloc
import importlib
from unittest.mock import patch, MagicMock, Mock
from click import Context
from click.testing import CliRunner

from autotools.utils.performance import (
    PerformanceMetrics, track_step, should_enable_metrics,
    display_metrics, init_metrics, finalize_metrics, get_metrics,
    ENABLE_PERFORMANCE_METRICS, _metrics
)

# CREATES A MOCK CLICK CONTEXT FOR TESTING
@pytest.fixture
def mock_ctx():
    ctx = MagicMock()
    ctx.params = {}
    ctx.parent = None
    return ctx

# CREATES A SAMPLE METRICS DICTIONARY FOR TESTING
@pytest.fixture
def sample_metrics_dict():
    return {
        'total_duration_ms': 100.0,
        'startup_duration_ms': 10.0,
        'command_duration_ms': 90.0,
        'cpu_time_total_ms': 50.0,
        'cpu_user_ms': 30.0,
        'cpu_sys_ms': 20.0,
        'rss_mb_peak': 100.0,
        'alloc_mb_total': 5.0,
        'gc_pause_total_ms': 2.0,
        'gc_collections_count': 5,
        'fs_bytes_read_total': 1000,
        'fs_bytes_written_total': 2000,
        'fs_ops_count': 10,
        'top_slowest_steps': [{'step': 'test', 'duration_ms': 50.0}]
    }

# HELPER TO CAPTURE DISPLAY_METRICS OUTPUT
def get_display_output(metrics_dict):
    runner = CliRunner()
    with runner.isolation() as isolation:
        out = isolation[0] if isinstance(isolation, tuple) else isolation
        display_metrics(metrics_dict)
        output = out.getvalue()
        output = output.decode('utf-8') if isinstance(output, bytes) else output
        return output

# HELPER TO CREATE A MOCK PSUTIL PROCESS
def create_mock_process(memory_rss=None, memory_peak_wss=None, io_counters=None, io_exception=None):
    mock_process = MagicMock()
    if memory_rss is not None: mock_process.memory_info.return_value = MagicMock(rss=memory_rss)
    if memory_peak_wss is not None: mock_process.memory_info_ex.return_value = MagicMock(peak_wss=memory_peak_wss)
    elif memory_rss is not None: mock_process.memory_info_ex.return_value = MagicMock()
    if io_exception: mock_process.io_counters.side_effect = io_exception
    elif io_counters is not None: mock_process.io_counters.return_value = io_counters
    return mock_process

# TEST FOR PERFORMANCE METRICS INITIALIZATION
def test_performance_metrics_init():
    metrics = PerformanceMetrics()
    assert metrics.process_start is None
    assert metrics.steps == []
    assert metrics._current_step is None

# TEST FOR PERFORMANCE METRICS RESET
def test_performance_metrics_reset():
    metrics = PerformanceMetrics()
    metrics.start_process()
    metrics.reset()
    assert metrics.process_start is None
    assert metrics.steps == []

# TEST FOR START PROCESS
def test_start_process():
    metrics = PerformanceMetrics()
    metrics.start_process()
    assert metrics.process_start is not None
    assert metrics.cpu_user_start is not None
    assert metrics.cpu_sys_start is not None

# TEST FOR END PROCESS
def test_end_process():
    metrics = PerformanceMetrics()
    metrics.start_process()
    metrics.start_startup()
    metrics.end_startup()
    metrics.end_process()
    assert metrics.process_end is not None
    assert metrics.cpu_user_end is not None
    assert metrics.cpu_sys_end is not None

# TEST FOR START STARTUP
def test_start_startup():
    metrics = PerformanceMetrics()
    metrics.start_startup()
    assert metrics.startup_start is not None
    assert metrics.tracemalloc_started is True
    assert metrics.alloc_start is not None
    assert metrics.gc_start_stats is not None

# TEST FOR END STARTUP
def test_end_startup():
    metrics = PerformanceMetrics()
    metrics.start_startup()
    metrics.end_startup()
    assert metrics.startup_end is not None

# TEST FOR START COMMAND
def test_start_command():
    metrics = PerformanceMetrics()
    metrics.start_command()
    assert metrics.command_start is not None

# TEST FOR END COMMAND
def test_end_command():
    metrics = PerformanceMetrics()
    metrics.start_command()
    metrics.end_command()
    assert metrics.command_end is not None

# TEST FOR STEP START
def test_step_start():
    metrics = PerformanceMetrics()
    metrics.step_start('test_step')
    assert metrics._current_step == 'test_step'
    assert metrics._step_start is not None

# TEST FOR STEP END
def test_step_end():
    metrics = PerformanceMetrics()
    metrics.step_start('test_step')
    time.sleep(0.001)
    metrics.step_end()
    assert metrics._current_step is None
    assert metrics._step_start is None
    assert len(metrics.steps) == 1
    assert metrics.steps[0][0] == 'test_step'

# TEST FOR STEP END WITHOUT START
def test_step_end_without_start():
    metrics = PerformanceMetrics()
    metrics.step_end()
    assert len(metrics.steps) == 0

# TEST FOR STEP START WITH EXISTING STEP
def test_step_start_with_existing_step():
    metrics = PerformanceMetrics()
    metrics.step_start('step1')
    time.sleep(0.001)
    metrics.step_start('step2')
    assert metrics._current_step == 'step2'
    assert len(metrics.steps) == 1
    assert metrics.steps[0][0] == 'step1'

# TEST FOR RECORD CPU START
def test_record_cpu_start():
    metrics = PerformanceMetrics()
    metrics._record_cpu_start()
    assert metrics.cpu_user_start is not None
    assert metrics.cpu_sys_start is not None

# TEST FOR RECORD CPU START WITH RESOURCE (NO PSUTIL)
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', False)
def test_record_cpu_start_with_resource():
    mock_resource = MagicMock()
    mock_resource.RUSAGE_SELF = 0
    mock_usage = MagicMock()
    mock_usage.ru_utime = 1.5
    mock_usage.ru_stime = 0.5
    mock_resource.getrusage.return_value = mock_usage
    
    metrics = PerformanceMetrics()
    with patch('autotools.utils.performance.RESOURCE_AVAILABLE', True), patch('autotools.utils.performance.resource', mock_resource):
        metrics._record_cpu_start()
        assert metrics.cpu_user_start == pytest.approx(1.5)
        assert metrics.cpu_sys_start == pytest.approx(0.5)

# TEST FOR RECORD CPU START WITHOUT PSUTIL OR RESOURCE
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', False)
@patch('autotools.utils.performance.RESOURCE_AVAILABLE', False)
def test_record_cpu_start_fallback():
    metrics = PerformanceMetrics()
    metrics._record_cpu_start()
    assert metrics.cpu_user_start is not None
    assert metrics.cpu_sys_start == pytest.approx(0.0)

# TEST FOR RECORD CPU END
def test_record_cpu_end():
    metrics = PerformanceMetrics()
    metrics._record_cpu_start()
    metrics._record_cpu_end()
    assert metrics.cpu_user_end is not None
    assert metrics.cpu_sys_end is not None

# TEST FOR RECORD CPU END WITH RESOURCE (NO PSUTIL)
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', False)
def test_record_cpu_end_with_resource():
    mock_resource = MagicMock()
    mock_resource.RUSAGE_SELF = 0
    mock_usage = MagicMock()
    mock_usage.ru_utime = 2.5
    mock_usage.ru_stime = 1.0
    mock_resource.getrusage.return_value = mock_usage
    
    metrics = PerformanceMetrics()
    metrics._record_cpu_start()
    with patch('autotools.utils.performance.RESOURCE_AVAILABLE', True), patch('autotools.utils.performance.resource', mock_resource):
        metrics._record_cpu_end()
        assert metrics.cpu_user_end == pytest.approx(2.5)
        assert metrics.cpu_sys_end == pytest.approx(1.0)

# TEST FOR RECORD CPU END WITHOUT PSUTIL OR RESOURCE
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', False)
@patch('autotools.utils.performance.RESOURCE_AVAILABLE', False)
def test_record_cpu_end_fallback():
    metrics = PerformanceMetrics()
    metrics._record_cpu_start()
    metrics._record_cpu_end()
    assert metrics.cpu_user_end is not None
    assert metrics.cpu_sys_end == pytest.approx(0.0)

# TEST FOR RECORD RSS START WITH PSUTIL
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', True)
@patch('autotools.utils.performance.psutil.Process')
def test_record_rss_start_with_psutil(mock_process_class):
    mock_process = create_mock_process(memory_rss=1024 * 1024 * 100)
    mock_process_class.return_value = mock_process
    metrics = PerformanceMetrics()
    metrics._record_rss_start()
    assert abs(metrics.rss_start - 100.0) < 1e-9

# TEST FOR RECORD RSS START WITHOUT PSUTIL
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', False)
def test_record_rss_start_without_psutil():
    mock_resource = MagicMock()
    mock_resource.RUSAGE_SELF = 0
    mock_usage = MagicMock()
    mock_resource.getrusage.return_value = mock_usage
    
    metrics = PerformanceMetrics()
    with patch('autotools.utils.performance.RESOURCE_AVAILABLE', True), patch('autotools.utils.performance.resource', mock_resource):
        with patch('sys.platform', 'linux'):
            mock_usage.ru_maxrss = 100 * 1024
            metrics._record_rss_start()
            assert abs(metrics.rss_start - 100.0) < 0.01

        metrics2 = PerformanceMetrics()
        with patch('sys.platform', 'darwin'):
            mock_usage.ru_maxrss = 100 * 1024 * 1024
            metrics2._record_rss_start()
            assert abs(metrics2.rss_start - 100.0) < 0.01

# TEST FOR RECORD RSS START WITHOUT PSUTIL OR RESOURCE
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', False)
@patch('autotools.utils.performance.RESOURCE_AVAILABLE', False)
def test_record_rss_start_without_psutil_or_resource():
    metrics = PerformanceMetrics()
    metrics._record_rss_start()
    assert abs(metrics.rss_start - 0.0) < 1e-9

# TEST FOR RECORD RSS END WITH PSUTIL
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', True)
@patch('autotools.utils.performance.psutil.Process')
def test_record_rss_end_with_psutil(mock_process_class):
    mock_process = create_mock_process(memory_rss=1024 * 1024 * 150, memory_peak_wss=1024 * 1024 * 200)
    mock_process_class.return_value = mock_process
    
    metrics = PerformanceMetrics()
    metrics.rss_start = 100.0
    metrics._record_rss_end()
    assert abs(metrics.rss_peak - 200.0) < 1e-9

# TEST FOR RECORD RSS END WITH PSUTIL NO PEAK WSS
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', True)
@patch('autotools.utils.performance.psutil.Process')
def test_record_rss_end_with_psutil_no_peak_wss(mock_process_class):
    mock_process = create_mock_process(memory_rss=1024 * 1024 * 150)
    class MemExtNoPeak: pass
    mem_ext_no_peak = MemExtNoPeak()
    mock_process.memory_info_ex.return_value = mem_ext_no_peak
    mock_process_class.return_value = mock_process
    
    metrics = PerformanceMetrics()
    metrics.rss_start = 100.0
    metrics._record_rss_end()
    assert abs(metrics.rss_peak - 150.0) < 1e-9

# TEST FOR RECORD RSS END WITH PSUTIL EXCEPTION
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', True)
@patch('autotools.utils.performance.psutil.Process')
def test_record_rss_end_with_psutil_exception(mock_process_class):
    mock_process = create_mock_process(memory_rss=1024 * 1024 * 150)
    mock_process.memory_info_ex.side_effect = Exception("ERROR")
    mock_process_class.return_value = mock_process
    
    metrics = PerformanceMetrics()
    metrics.rss_start = 100.0
    metrics._record_rss_end()
    assert abs(metrics.rss_peak - 150.0) < 1e-9

# TEST FOR RECORD RSS END WITHOUT PSUTIL
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', False)
def test_record_rss_end_without_psutil():
    mock_resource = MagicMock()
    mock_resource.RUSAGE_SELF = 0
    mock_usage = MagicMock()
    mock_usage.ru_maxrss = 1024 * 150
    mock_resource.getrusage.return_value = mock_usage
    
    metrics = PerformanceMetrics()
    metrics.rss_start = 100.0 / 1024
    
    with patch('autotools.utils.performance.RESOURCE_AVAILABLE', True), patch('autotools.utils.performance.resource', mock_resource):
        with patch('sys.platform', 'linux'):
            metrics._record_rss_end()
            assert metrics.rss_peak > 0
        
        with patch('sys.platform', 'darwin'):
            metrics.rss_start = 100.0 / (1024 * 1024)
            metrics._record_rss_end()
            assert metrics.rss_peak > 0

# TEST FOR RECORD RSS END WITHOUT PSUTIL OR RESOURCE
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', False)
@patch('autotools.utils.performance.RESOURCE_AVAILABLE', False)
def test_record_rss_end_fallback():
    metrics = PerformanceMetrics()
    metrics.rss_start = 50.0
    metrics._record_rss_end()
    assert metrics.rss_peak == pytest.approx(50.0)
    
    metrics2 = PerformanceMetrics()
    metrics2.rss_start = None
    metrics2._record_rss_end()
    assert metrics2.rss_peak == pytest.approx(0.0)

# TEST FOR RECORD FS START WITH PSUTIL
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', True)
@patch('autotools.utils.performance.psutil.Process')
def test_record_fs_start_with_psutil(mock_process_class):
    mock_io = MagicMock(read_bytes=1000, write_bytes=2000, read_count=10, write_count=20)
    mock_process = create_mock_process(io_counters=mock_io)
    mock_process_class.return_value = mock_process
    
    metrics = PerformanceMetrics()
    metrics._record_fs_start()
    assert metrics.fs_read_start == 1000
    assert metrics.fs_write_start == 2000
    assert metrics.fs_ops_start == 30

# TEST FOR RECORD FS START WITH PSUTIL EXCEPTION
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', True)
@patch('autotools.utils.performance.psutil.Process')
def test_record_fs_start_with_psutil_exception(mock_process_class):
    import psutil
    mock_process = create_mock_process(io_exception=psutil.AccessDenied())
    mock_process_class.return_value = mock_process
    
    metrics = PerformanceMetrics()
    metrics._record_fs_start()
    assert metrics.fs_read_start == 0
    assert metrics.fs_write_start == 0
    assert metrics.fs_ops_start == 0

# TEST FOR RECORD FS START WITH PSUTIL ACCESS DENIED
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', True)
@patch('autotools.utils.performance.psutil.Process')
def test_record_fs_start_with_psutil_access_denied(mock_process_class):
    import psutil
    mock_process = create_mock_process(io_exception=psutil.AccessDenied())
    mock_process_class.return_value = mock_process
    
    metrics = PerformanceMetrics()
    metrics._record_fs_start()
    assert metrics.fs_read_start == 0
    assert metrics.fs_write_start == 0
    assert metrics.fs_ops_start == 0

# TEST FOR RECORD FS START WITHOUT PSUTIL
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', False)
def test_record_fs_start_without_psutil():
    metrics = PerformanceMetrics()
    metrics._record_fs_start()
    assert metrics.fs_read_start == 0
    assert metrics.fs_write_start == 0
    assert metrics.fs_ops_start == 0

# TEST FOR RECORD FS END WITH PSUTIL
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', True)
@patch('autotools.utils.performance.psutil.Process')
def test_record_fs_end_with_psutil(mock_process_class):
    mock_io = MagicMock(read_bytes=2000, write_bytes=3000, read_count=20, write_count=30)
    mock_process = create_mock_process(io_counters=mock_io)
    mock_process_class.return_value = mock_process
    
    metrics = PerformanceMetrics()
    metrics.fs_read_start = 1000
    metrics.fs_write_start = 2000
    metrics.fs_ops_start = 10
    metrics._record_fs_end()
    assert metrics.fs_read_end == 2000
    assert metrics.fs_write_end == 3000
    assert metrics.fs_ops_end == 50

# TEST FOR RECORD FS END WITH PSUTIL EXCEPTION
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', True)
@patch('autotools.utils.performance.psutil.Process')
def test_record_fs_end_with_psutil_exception(mock_process_class):
    import psutil
    mock_process = create_mock_process(io_exception=psutil.AccessDenied())
    mock_process_class.return_value = mock_process
    
    metrics = PerformanceMetrics()
    metrics.fs_read_start = 1000
    metrics.fs_write_start = 2000
    metrics.fs_ops_start = 10
    metrics._record_fs_end()
    assert metrics.fs_read_end == 1000
    assert metrics.fs_write_end == 2000
    assert metrics.fs_ops_end == 10

# TEST FOR RECORD FS END WITHOUT PSUTIL
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', False)
def test_record_fs_end_without_psutil():
    metrics = PerformanceMetrics()
    metrics.fs_read_start = 1000
    metrics.fs_write_start = 2000
    metrics.fs_ops_start = 10
    metrics._record_fs_end()
    assert metrics.fs_read_end == 1000
    assert metrics.fs_write_end == 2000
    assert metrics.fs_ops_end == 10

# TEST FOR GET GC STATS
def test_get_gc_stats():
    metrics = PerformanceMetrics()
    stats = metrics._get_gc_stats()
    assert isinstance(stats, list)
    assert len(stats) > 0

# TEST FOR CALCULATE DURATIONS
def test_calculate_durations():
    metrics = PerformanceMetrics()
    metrics.process_start = 1.0
    metrics.process_end = 2.0
    metrics.startup_start = 1.0
    metrics.startup_end = 1.1
    metrics.command_start = 1.1
    metrics.command_end = 1.9
    
    total, startup, command = metrics._calculate_durations()
    assert abs(total - 1000.0) < 0.01
    assert abs(startup - 100.0) < 0.01
    assert abs(command - 800.0) < 0.01

# TEST FOR CALCULATE DURATIONS WITH NONE VALUES
def test_calculate_durations_with_none():
    metrics = PerformanceMetrics()
    total, startup, command = metrics._calculate_durations()
    assert abs(total - 0.0) < 1e-9
    assert abs(startup - 0.0) < 1e-9
    assert abs(command - 0.0) < 1e-9

# TEST FOR CALCULATE CPU TIME
def test_calculate_cpu_time():
    metrics = PerformanceMetrics()
    metrics.cpu_user_start = 1.0
    metrics.cpu_user_end = 1.1
    metrics.cpu_sys_start = 1.0
    metrics.cpu_sys_end = 1.05
    
    total, user, sys = metrics._calculate_cpu_time()
    assert abs(total - 150.0) < 0.01
    assert abs(user - 100.0) < 0.01
    assert abs(sys - 50.0) < 0.01

# TEST FOR CALCULATE CPU TIME WITH NONE VALUES
def test_calculate_cpu_time_with_none():
    metrics = PerformanceMetrics()
    total, user, sys = metrics._calculate_cpu_time()
    assert abs(total - 0.0) < 1e-9
    assert abs(user - 0.0) < 1e-9
    assert abs(sys - 0.0) < 1e-9

# TEST FOR CALCULATE ALLOCATIONS
def test_calculate_allocations():
    metrics = PerformanceMetrics()
    metrics.start_startup()
    _ = list(range(1000))
    metrics.alloc_end = tracemalloc.take_snapshot()
    
    alloc_mb = metrics._calculate_allocations()
    assert alloc_mb >= 0

# TEST FOR CALCULATE ALLOCATIONS WITH NONE
def test_calculate_allocations_with_none():
    metrics = PerformanceMetrics()
    alloc_mb = metrics._calculate_allocations()
    assert abs(alloc_mb - 0.0) < 1e-9

# TEST FOR CALCULATE GC STATS
def test_calculate_gc_stats():
    metrics = PerformanceMetrics()
    metrics.gc_start_stats = gc.get_stats()
    _ = list(range(10000))
    del _
    gc.collect()
    metrics.gc_end_stats = gc.get_stats()
    
    pause_ms, collections = metrics._calculate_gc_stats()
    assert pause_ms >= 0
    assert collections >= 0

# TEST FOR CALCULATE GC STATS WITH NONE
def test_calculate_gc_stats_with_none():
    metrics = PerformanceMetrics()
    pause_ms, collections = metrics._calculate_gc_stats()
    assert abs(pause_ms - 0.0) < 1e-9
    assert collections == 0

# TEST FOR CALCULATE FS IO
def test_calculate_fs_io():
    metrics = PerformanceMetrics()
    metrics.fs_read_start = 1000
    metrics.fs_read_end = 2000
    metrics.fs_write_start = 500
    metrics.fs_write_end = 1500
    metrics.fs_ops_start = 10
    metrics.fs_ops_end = 25
    
    read, write, ops = metrics._calculate_fs_io()
    assert read == 1000
    assert write == 1000
    assert ops == 15

# TEST FOR CALCULATE FS IO WITH NONE
def test_calculate_fs_io_with_none():
    metrics = PerformanceMetrics()
    read, write, ops = metrics._calculate_fs_io()
    assert read == 0
    assert write == 0
    assert ops == 0

# TEST FOR GET METRICS
def test_get_metrics():
    metrics = PerformanceMetrics()
    metrics.start_process()
    metrics.start_startup()
    metrics.end_startup()
    metrics.start_command()
    time.sleep(0.001)
    metrics.end_command()
    metrics.end_process()
    
    result = metrics.get_metrics()
    assert 'total_duration_ms' in result
    assert 'startup_duration_ms' in result
    assert 'command_duration_ms' in result
    assert 'cpu_time_total_ms' in result
    assert 'rss_mb_peak' in result
    assert 'alloc_mb_total' in result
    assert 'gc_pause_total_ms' in result
    assert 'gc_collections_count' in result
    assert 'fs_bytes_read_total' in result
    assert 'fs_bytes_written_total' in result
    assert 'fs_ops_count' in result
    assert 'top_slowest_steps' in result

# TEST FOR GET METRICS WITH CURRENT STEP
def test_get_metrics_with_current_step():
    metrics = PerformanceMetrics()
    metrics.step_start('test_step')
    metrics.get_metrics()
    assert metrics._current_step is None

# TEST FOR TRACK STEP CONTEXT MANAGER
def test_track_step():
    initial_steps = len(_metrics.steps)
    with track_step('test_step'): time.sleep(0.001)
    assert len(_metrics.steps) == initial_steps + 1

# TEST FOR TRACK STEP WITH EXCEPTION
def test_track_step_with_exception():
    initial_steps = len(_metrics.steps)
    try:
        with track_step('test_step'): raise ValueError("TEST EXCEPTION")
    except ValueError:
        pass
    assert len(_metrics.steps) == initial_steps + 1

# TEST FOR SHOULD ENABLE METRICS WITH FLAG DISABLED
@patch('autotools.utils.performance.ENABLE_PERFORMANCE_METRICS', False)
def test_should_enable_metrics_flag_disabled(mock_ctx):
    assert should_enable_metrics(mock_ctx) is False

# TEST FOR SHOULD ENABLE METRICS WITH PERF FLAG
def test_should_enable_metrics_with_perf_flag(mock_ctx):
    mock_ctx.params = {'perf': True}
    with patch('autotools.utils.performance.ENABLE_PERFORMANCE_METRICS', True):
        assert should_enable_metrics(mock_ctx) is True

# TEST FOR SHOULD ENABLE METRICS WITH PERF FLAG EVEN WHEN ENABLE_PERFORMANCE_METRICS IS False
def test_should_enable_metrics_with_perf_flag_override_disabled(mock_ctx):
    mock_ctx.params = {'perf': True}
    with patch('autotools.utils.performance.ENABLE_PERFORMANCE_METRICS', False):
        assert should_enable_metrics(mock_ctx) is True

# TEST FOR SHOULD ENABLE METRICS WITH PERF FLAG IN PARENT
def test_should_enable_metrics_with_perf_flag_in_parent(mock_ctx):
    mock_parent = MagicMock(params={'perf': True})
    mock_ctx.params = {}
    mock_ctx.parent = mock_parent
    with patch('autotools.utils.performance.ENABLE_PERFORMANCE_METRICS', True):
        assert should_enable_metrics(mock_ctx) is True

# TEST FOR SHOULD ENABLE METRICS WITH PERF FLAG IN PARENT EVEN WHEN ENABLE_PERFORMANCE_METRICS IS False
def test_should_enable_metrics_with_perf_flag_in_parent_override_disabled(mock_ctx):
    mock_parent = MagicMock(params={'perf': True})
    mock_ctx.params = {}
    mock_ctx.parent = mock_parent
    with patch('autotools.utils.performance.ENABLE_PERFORMANCE_METRICS', False):
        assert should_enable_metrics(mock_ctx) is True

# TEST FOR SHOULD ENABLE METRICS IN DEVELOPMENT MODE
def test_should_enable_metrics_dev_mode(mock_ctx):
    with patch('autotools.utils.performance.ENABLE_PERFORMANCE_METRICS', True):
        with patch('sys.modules', {'autotools': MagicMock(__file__='/dev/test/autotools/__init__.py')}):
            assert should_enable_metrics(mock_ctx) is True

# TEST FOR SHOULD ENABLE METRICS NOT IN DEVELOPMENT MODE
def test_should_enable_metrics_not_dev_mode(mock_ctx):
    with patch('autotools.utils.performance.ENABLE_PERFORMANCE_METRICS', True):
        with patch('sys.modules', {'autotools': MagicMock(__file__='/usr/lib/python3/site-packages/autotools/__init__.py')}):
            assert should_enable_metrics(mock_ctx) is False

# TEST FOR SHOULD ENABLE METRICS NO MODULE
def test_should_enable_metrics_no_module(mock_ctx):
    with patch('autotools.utils.performance.ENABLE_PERFORMANCE_METRICS', True):
        with patch('sys.modules', {}):
            result = should_enable_metrics(mock_ctx)
            assert not result

# TEST FOR DISPLAY METRICS
def test_display_metrics(sample_metrics_dict):
    output = get_display_output(sample_metrics_dict)
    assert "PERFORMANCE METRICS" in output
    assert "100.00 ms" in output
    assert "test" in output

# TEST FOR DISPLAY METRICS WITHOUT GC
def test_display_metrics_without_gc(sample_metrics_dict):
    metrics = {
        **sample_metrics_dict, 'gc_pause_total_ms': 0.0, 'gc_collections_count': 0,
        'fs_bytes_read_total': 0, 'fs_bytes_written_total': 0, 'fs_ops_count': 0,
        'top_slowest_steps': []
    }
    output = get_display_output(metrics)
    assert "PERFORMANCE METRICS" in output
    assert "GARBAGE COLLECTION" not in output
    assert "FILESYSTEM I/O" not in output

# TEST FOR DISPLAY METRICS WITH ZERO DURATION
def test_display_metrics_zero_duration(sample_metrics_dict):
    metrics = {
        k: 0.0 if isinstance(v, float) else (0 if isinstance(v, int) else [])
        for k, v in sample_metrics_dict.items()
    }
    output = get_display_output(metrics)
    assert "PERFORMANCE METRICS" in output
    assert "CPU Usage Ratio:       0.0%" in output

# TEST FOR INIT METRICS
def test_init_metrics():
    init_metrics()
    metrics = get_metrics()
    assert metrics.process_start is not None
    assert metrics.startup_start is not None
    assert metrics.tracemalloc_started is True

# TEST FOR FINALIZE METRICS
def test_finalize_metrics(mock_ctx):
    with patch('autotools.utils.performance.should_enable_metrics', return_value=True):
        init_metrics()
        get_metrics().end_startup()
        get_metrics().start_command()
        get_metrics().end_command()
        
        runner = CliRunner()
        with runner.isolation() as isolation:
            out = isolation[0] if isinstance(isolation, tuple) else isolation
            finalize_metrics(mock_ctx)
            output = out.getvalue()
            output = output.decode('utf-8') if isinstance(output, bytes) else output
            assert "PERFORMANCE METRICS" in output

# TEST FOR FINALIZE METRICS DISABLED
def test_finalize_metrics_disabled(mock_ctx):
    with patch('autotools.utils.performance.should_enable_metrics', return_value=False):
        runner = CliRunner()
        with runner.isolation() as isolation:
            out = isolation[0] if isinstance(isolation, tuple) else isolation
            finalize_metrics(mock_ctx)
            output = out.getvalue()
            output = output.decode('utf-8') if isinstance(output, bytes) else output
            assert "PERFORMANCE METRICS" not in output

# TEST FOR GET METRICS FUNCTION
def test_get_metrics_function():
    metrics = get_metrics()
    assert isinstance(metrics, PerformanceMetrics)

# TEST FOR ENVIRONMENT VARIABLE DISABLE
@patch('autotools.utils.performance.os.getenv')
def test_environment_variable_disable(mock_getenv):
    mock_getenv.return_value = '1'
    result = mock_getenv('AUTOTOOLS_DISABLE_PERF', '').lower() in ('1', 'true', 'yes')
    assert result is True

# TEST FOR ENVIRONMENT VARIABLE DISABLE WITH TRUE
@patch('autotools.utils.performance.os.getenv')
def test_environment_variable_disable_with_true(mock_getenv):
    mock_getenv.return_value = 'true'
    result = mock_getenv('AUTOTOOLS_DISABLE_PERF', '').lower() in ('1', 'true', 'yes')
    assert result is True

# TEST FOR ENVIRONMENT VARIABLE DISABLE WITH YES
@patch('autotools.utils.performance.os.getenv')
def test_environment_variable_disable_with_yes(mock_getenv):
    mock_getenv.return_value = 'yes'
    result = mock_getenv('AUTOTOOLS_DISABLE_PERF', '').lower() in ('1', 'true', 'yes')
    assert result is True

# TEST FOR ENVIRONMENT VARIABLE NOT SET
@patch('autotools.utils.performance.os.getenv')
def test_environment_variable_not_set(mock_getenv):
    mock_getenv.return_value = ''
    result = mock_getenv('AUTOTOOLS_DISABLE_PERF', '').lower() in ('1', 'true', 'yes')
    assert result is False

# TEST FOR RECORD RSS END WITH PSUTIL NO MEMORY INFO EX
@patch('autotools.utils.performance.PSUTIL_AVAILABLE', True)
@patch('autotools.utils.performance.psutil.Process')
def test_record_rss_end_with_psutil_no_memory_info_ex(mock_process_class):
    mock_process = create_mock_process(memory_rss=1024 * 1024 * 150)
    mock_process.memory_info_ex = None
    mock_process_class.return_value = mock_process
    
    metrics = PerformanceMetrics()
    metrics.rss_start = 100.0
    metrics._record_rss_end()
    assert abs(metrics.rss_peak - 150.0) < 1e-9

# TEST FOR CALCULATE GC STATS WITH DIFFERENT LENGTHS
def test_calculate_gc_stats_different_lengths():
    metrics = PerformanceMetrics()
    metrics.gc_start_stats = [{'collections': 1, 'total_time': 0.1}]
    metrics.gc_end_stats = [{'collections': 2, 'total_time': 0.2}, {'collections': 1, 'total_time': 0.1}]
    
    pause_ms, collections = metrics._calculate_gc_stats()
    assert abs(pause_ms - 0.0) < 1e-9
    assert collections == 0

# TEST FOR CALCULATE ALLOCATIONS WITH NEGATIVE SIZE DIFF
def test_calculate_allocations_negative_size_diff():
    metrics = PerformanceMetrics()
    metrics.start_startup()

    _ = list(range(100))
    metrics.alloc_end = tracemalloc.take_snapshot()

    alloc_mb = metrics._calculate_allocations()
    assert alloc_mb >= 0

# TEST FOR DISPLAY METRICS WITH EMPTY TOP SLOWEST STEPS
def test_display_metrics_empty_top_slowest_steps(sample_metrics_dict):
    metrics = {
        **sample_metrics_dict, 'gc_pause_total_ms': 0.0, 'gc_collections_count': 0,
        'fs_bytes_read_total': 0, 'fs_bytes_written_total': 0, 'fs_ops_count': 0,
        'top_slowest_steps': []
    }
    output = get_display_output(metrics)
    assert "PERFORMANCE METRICS" in output
    assert "TOP SLOWEST STEPS" not in output

# TEST FOR DISPLAY METRICS WITH MULTIPLE SLOWEST STEPS
def test_display_metrics_multiple_slowest_steps(sample_metrics_dict):
    metrics = {
        **sample_metrics_dict, 'gc_pause_total_ms': 0.0, 'gc_collections_count': 0,
        'fs_bytes_read_total': 0, 'fs_bytes_written_total': 0, 'fs_ops_count': 0,
        'top_slowest_steps': [
            {'step': 'step1', 'duration_ms': 50.0},
            {'step': 'step2', 'duration_ms': 30.0},
            {'step': 'step3', 'duration_ms': 20.0}
        ]
    }
    output = get_display_output(metrics)
    assert "PERFORMANCE METRICS" in output
    assert "step1" in output
    assert "step2" in output
    assert "step3" in output

# TEST FOR END PROCESS WITHOUT TRACEMALLOC
def test_end_process_without_tracemalloc():
    metrics = PerformanceMetrics()
    metrics.start_process()
    metrics.tracemalloc_started = False
    metrics.end_process()
    assert metrics.process_end is not None
    assert metrics.alloc_end is None

# TEST FOR START STARTUP WITH TRACEMALLOC ALREADY STARTED
def test_start_startup_tracemalloc_already_started():
    metrics = PerformanceMetrics()
    metrics.tracemalloc_started = True
    metrics.start_startup()
    assert metrics.startup_start is not None
    assert metrics.alloc_start is not None

# TEST FOR START STARTUP WITH TRACEMALLOC STARTED BUT NOT TRACING
def test_start_startup_tracemalloc_started_but_not_tracing():
    metrics = PerformanceMetrics()
    if tracemalloc.is_tracing(): tracemalloc.stop()
    metrics.tracemalloc_started = True
    metrics.start_startup()
    assert metrics.startup_start is not None
    assert metrics.alloc_start is None

# TEST FOR CALCULATE GC STATS WITH NEGATIVE VALUES
def test_calculate_gc_stats_negative_values():
    metrics = PerformanceMetrics()
    metrics.gc_start_stats = [{'collections': 5, 'total_time': 0.2}]
    metrics.gc_end_stats = [{'collections': 3, 'total_time': 0.1}]
    
    pause_ms, collections = metrics._calculate_gc_stats()
    assert abs(pause_ms - 0.0) < 1e-9
    assert collections == 0

# TEST FOR GET METRICS WITH RSS PEAK NONE
def test_get_metrics_rss_peak_none():
    metrics = PerformanceMetrics()
    metrics.start_process()
    metrics.start_startup()
    metrics.end_startup()
    metrics.start_command()
    metrics.end_command()
    metrics.end_process()
    metrics.rss_peak = None
    
    result = metrics.get_metrics()
    assert abs(result['rss_mb_peak'] - 0.0) < 1e-9

# TEST FOR RESOURCE AVAILABLE WHEN RESOURCE IS IMPORTED
def test_resource_available_when_imported():
    import autotools.utils.performance as perf_module
    assert hasattr(perf_module, 'RESOURCE_AVAILABLE')
    assert isinstance(perf_module.RESOURCE_AVAILABLE, bool)

# TEST FOR RESOURCE AVAILABLE = True PATH
def test_resource_available_true_path():
    import sys
    import importlib

    mock_resource = MagicMock()
    mock_resource.RUSAGE_SELF = 0

    perf_module_name = 'autotools.utils.performance'
    original_resource = sys.modules.get('resource')
    
    fake_resource = MagicMock()
    fake_resource.RUSAGE_SELF = 0
    sys.modules['resource'] = fake_resource
    
    try:
        if perf_module_name in sys.modules: importlib.reload(sys.modules[perf_module_name])
        else: importlib.import_module(perf_module_name)

        perf_module = sys.modules[perf_module_name]
        assert hasattr(perf_module, 'RESOURCE_AVAILABLE')
    finally:
        if original_resource: sys.modules['resource'] = original_resource
        elif 'resource' in sys.modules: del sys.modules['resource']
        if perf_module_name in sys.modules: importlib.reload(sys.modules[perf_module_name])

# TEST FOR PSUTIL IMPORT ERROR TO COVER EXCEPT BLOCK
def test_psutil_import_error_coverage():
    import builtins
    original_psutil = sys.modules.get('psutil')
    perf_module_name = 'autotools.utils.performance'
    original_perf_module = sys.modules.get(perf_module_name)
    
    modules_to_remove = []
    for key in sys.modules.keys():
        if key == 'psutil' or key == perf_module_name or key.startswith(perf_module_name + '.'):
            modules_to_remove.append(key)

    for key in modules_to_remove: del sys.modules[key]

    original_import = builtins.__import__
    def import_side_effect(name, *args, **kwargs):
        if name == 'psutil': raise ImportError("No module named 'psutil'")
        return original_import(name, *args, **kwargs)
    
    with patch('builtins.__import__', side_effect=import_side_effect):
        perf_module = importlib.import_module(perf_module_name)
        assert perf_module.PSUTIL_AVAILABLE is False
        metrics = perf_module.PerformanceMetrics()
        metrics._record_rss_start()
        assert metrics.rss_start is not None
    
    if original_psutil: sys.modules['psutil'] = original_psutil
    if original_perf_module:
        sys.modules[perf_module_name] = original_perf_module
        importlib.reload(original_perf_module)

# TEST FOR RESOURCE IMPORT ERROR TO COVER EXCEPT BLOCK
def test_resource_import_error_coverage():
    import builtins
    original_resource = sys.modules.get('resource')
    perf_module_name = 'autotools.utils.performance'
    original_perf_module = sys.modules.get(perf_module_name)
    
    modules_to_remove = []
    for key in sys.modules.keys():
        if key == 'resource' or key == perf_module_name or key.startswith(perf_module_name + '.'):
            modules_to_remove.append(key)

    for key in modules_to_remove: del sys.modules[key]

    original_import = builtins.__import__
    def import_side_effect(name, *args, **kwargs):
        if name == 'resource': raise ImportError("No module named 'resource'")
        return original_import(name, *args, **kwargs)
    
    with patch('builtins.__import__', side_effect=import_side_effect):
        perf_module = importlib.import_module(perf_module_name)
        assert perf_module.RESOURCE_AVAILABLE is False
        assert perf_module.resource is None
        original_psutil_available = perf_module.PSUTIL_AVAILABLE
        perf_module.PSUTIL_AVAILABLE = False

        try:
            metrics = perf_module.PerformanceMetrics()
            metrics._record_rss_start()
            assert abs(metrics.rss_start - 0.0) < 1e-9
        finally:
            perf_module.PSUTIL_AVAILABLE = original_psutil_available

    if original_resource: sys.modules['resource'] = original_resource
    if original_perf_module:
        sys.modules[perf_module_name] = original_perf_module
        importlib.reload(original_perf_module)
