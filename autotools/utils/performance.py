import os
import gc
import sys
import time
import click
import tracemalloc
from contextlib import contextmanager
from typing import Dict, List, Tuple, Optional

try:
    import resource
    RESOURCE_AVAILABLE = True
except ImportError:
    resource = None
    RESOURCE_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# GLOBAL FLAG TO ENABLE/DISABLE PERFORMANCE METRICS
ENABLE_PERFORMANCE_METRICS = False
if os.getenv('AUTOTOOLS_DISABLE_PERF', '').lower() in ('1', 'true', 'yes'): ENABLE_PERFORMANCE_METRICS = False

# FLAG TO ENABLE/DISABLE TRACEMALLOC (CAN BE SLOW IN PRODUCTION)
# ONLY ENABLE IF EXPLICITLY REQUESTED VIA ENV VAR OR IF PYTEST IS ACTUALLY RUNNING
# DO NOT ENABLE BASED ON ARGUMENT VALUES TO AVOID FALSE POSITIVES (EXAMPLE: "test" AS COMMAND ARGUMENT)
_ENV_TRACEMALLOC = os.getenv('AUTOTOOLS_ENABLE_TRACEMALLOC', '').lower() in ('1', 'true', 'yes')
_IS_TEST_ENV = 'pytest' in sys.modules or any(arg.endswith('pytest') or arg.endswith('py.test') for arg in sys.argv)
ENABLE_TRACEMALLOC = _ENV_TRACEMALLOC or _IS_TEST_ENV

# PERFORMANCE METRICS COLLECTOR
class PerformanceMetrics:
    def __init__(self):
        self.reset()
        self.steps: List[Tuple[str, float]] = []
        self._step_start: Optional[float] = None
        self._current_step: Optional[str] = None
        
    def reset(self):
        # TIMING METRICS
        self.startup_start = None
        self.startup_end = None
        self.command_start = None
        self.command_end = None
        self.process_start = None
        self.process_end = None
        
        # CPU METRICS
        self.cpu_user_start = None
        self.cpu_sys_start = None
        self.cpu_user_end = None
        self.cpu_sys_end = None
        
        # MEMORY METRICS
        self.rss_start = None
        self.rss_peak = None
        
        # ALLOCATION TRACKING
        self.tracemalloc_started = False
        self.alloc_start = None
        self.alloc_end = None
        
        # GARBAGE COLLECTION METRICS
        self.gc_start_stats = None
        self.gc_end_stats = None
        
        # FILESYSTEM I/O METRICS
        self.fs_read_start = None
        self.fs_write_start = None
        self.fs_read_end = None
        self.fs_write_end = None
        self.fs_ops_start = None
        self.fs_ops_end = None
        
        # STEP TRACKING
        self.steps = []
        self._step_start = None
        self._current_step = None

    # STARTS PROCESS-LEVEL METRICS TRACKING
    def start_process(self):
        self.process_start = time.perf_counter()
        self._record_cpu_start()
        self._record_rss_start()
        self._record_fs_start()
        
    # STARTS STARTUP PHASE TRACKING
    def start_startup(self):
        self.startup_start = time.perf_counter()
        if tracemalloc.is_tracing() and not self.tracemalloc_started:
            self.tracemalloc_started = True
        elif ENABLE_TRACEMALLOC and not self.tracemalloc_started:
            tracemalloc.start(1)
            self.tracemalloc_started = True

        if self.tracemalloc_started and tracemalloc.is_tracing():
            self.alloc_start = tracemalloc.take_snapshot()
        self.gc_start_stats = self._get_gc_stats()
        
    # ENDS STARTUP PHASE TRACKING
    def end_startup(self):
        self.startup_end = time.perf_counter()
        
    # STARTS COMMAND EXECUTION TRACKING
    def start_command(self):
        self.command_start = time.perf_counter()
        
    # ENDS COMMAND EXECUTION TRACKING
    def end_command(self):
        self.command_end = time.perf_counter()
        
    # ENDS PROCESS-LEVEL METRICS TRACKING
    def end_process(self):
        self.process_end = time.perf_counter()
        self._record_cpu_end()
        self._record_rss_end()
        self._record_fs_end()
        if self.tracemalloc_started and tracemalloc.is_tracing():
            self.alloc_end = tracemalloc.take_snapshot()
            tracemalloc.stop()
        self.gc_end_stats = self._get_gc_stats()

    # STARTS TRACKING A NAMED STEP
    def step_start(self, name: str):
        if self._current_step: 
            self.step_end()
        self._current_step = name
        self._step_start = time.perf_counter()
        
    # ENDS TRACKING THE CURRENT STEP
    def step_end(self):
        if self._current_step and self._step_start:
            duration = time.perf_counter() - self._step_start
            self.steps.append((self._current_step, duration))
            self._current_step = None
            self._step_start = None

    # RECORDS CPU USAGE AT START
    def _record_cpu_start(self):
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            cpu_times = process.cpu_times()
            self.cpu_user_start = cpu_times.user
            self.cpu_sys_start = cpu_times.system
        elif RESOURCE_AVAILABLE:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            self.cpu_user_start = usage.ru_utime
            self.cpu_sys_start = usage.ru_stime
        else:
            self.cpu_user_start = time.process_time()
            self.cpu_sys_start = 0.0
        
    # RECORDS CPU USAGE AT END
    def _record_cpu_end(self):
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            cpu_times = process.cpu_times()
            self.cpu_user_end = cpu_times.user
            self.cpu_sys_end = cpu_times.system
        elif RESOURCE_AVAILABLE:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            self.cpu_user_end = usage.ru_utime
            self.cpu_sys_end = usage.ru_stime
        else:
            self.cpu_user_end = time.process_time()
            self.cpu_sys_end = 0.0
        
    # RECORDS MEMORY USAGE AT START
    def _record_rss_start(self):
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            self.rss_start = process.memory_info().rss / (1024 * 1024)  # MB
        elif RESOURCE_AVAILABLE:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            self.rss_start = usage.ru_maxrss / 1024  # MB (LINUX) OR KB (MACOS)
            if sys.platform == 'darwin': 
                self.rss_start = self.rss_start / 1024  # CONVERT KB TO MB ON MACOS
        else:
            self.rss_start = 0.0
                
    # RECORDS MEMORY USAGE AT END
    def _record_rss_end(self):
        if PSUTIL_AVAILABLE: self._record_rss_end_psutil()
        elif RESOURCE_AVAILABLE: self._record_rss_end_resource()
        else: self.rss_peak = self.rss_start if self.rss_start is not None else 0.0

    # RECORDS MEMORY USAGE AT END USING PSUTIL
    def _record_rss_end_psutil(self):
        process = psutil.Process()
        mem_info = process.memory_info()
        self.rss_peak = mem_info.rss / (1024 * 1024) # MB

        try:
            if hasattr(process, 'memory_info_ex'):
                mem_ext = process.memory_info_ex()
                if hasattr(mem_ext, 'peak_wss'): self.rss_peak = max(self.rss_peak, mem_ext.peak_wss / (1024 * 1024))
        except Exception:
            pass

    # RECORDS MEMORY USAGE AT END USING RESOURCE
    def _record_rss_end_resource(self):
        usage = resource.getrusage(resource.RUSAGE_SELF)
        rss_current = usage.ru_maxrss / 1024
        if sys.platform == 'darwin': rss_current = rss_current / 1024
        self.rss_peak = max(self.rss_start, rss_current) if self.rss_start else rss_current
            
    # RECORDS FILESYSTEM I/O AT START
    def _record_fs_start(self):
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process()
                io_counters = process.io_counters()
                self.fs_read_start = io_counters.read_bytes
                self.fs_write_start = io_counters.write_bytes
                self.fs_ops_start = getattr(io_counters, 'read_count', 0) + getattr(io_counters, 'write_count', 0)
            except (AttributeError, psutil.AccessDenied):
                self.fs_read_start = 0
                self.fs_write_start = 0
                self.fs_ops_start = 0
        else:
            self.fs_read_start = 0
            self.fs_write_start = 0
            self.fs_ops_start = 0
            
    # RECORDS FILESYSTEM I/O AT END
    def _record_fs_end(self):
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process()
                io_counters = process.io_counters()
                self.fs_read_end = io_counters.read_bytes
                self.fs_write_end = io_counters.write_bytes
                self.fs_ops_end = getattr(io_counters, 'read_count', 0) + getattr(io_counters, 'write_count', 0)
            except (AttributeError, psutil.AccessDenied):
                self.fs_read_end = self.fs_read_start
                self.fs_write_end = self.fs_write_start
                self.fs_ops_end = self.fs_ops_start
        else:
            self.fs_read_end = self.fs_read_start
            self.fs_write_end = self.fs_write_start
            self.fs_ops_end = self.fs_ops_start
    
    # GETS CURRENT GARBAGE COLLECTION STATISTICS
    def _get_gc_stats(self) -> List[Dict]: 
        return gc.get_stats()
        
    # CALCULATES DURATION METRICS IN MILLISECONDS
    def _calculate_durations(self) -> Tuple[float, float, float]:
        total_duration_ms = (self.process_end - self.process_start) * 1000 if self.process_end is not None and self.process_start is not None else 0
        startup_duration_ms = (self.startup_end - self.startup_start) * 1000 if self.startup_end is not None and self.startup_start is not None else 0
        command_duration_ms = (self.command_end - self.command_start) * 1000 if self.command_end is not None and self.command_start is not None else 0
        return total_duration_ms, startup_duration_ms, command_duration_ms
        
    # CALCULATES CPU TIME METRICS IN MILLISECONDS
    def _calculate_cpu_time(self) -> Tuple[float, float, float]:
        cpu_user_ms = (self.cpu_user_end - self.cpu_user_start) * 1000 if self.cpu_user_end is not None and self.cpu_user_start is not None else 0
        cpu_sys_ms = (self.cpu_sys_end - self.cpu_sys_start) * 1000 if self.cpu_sys_end is not None and self.cpu_sys_start is not None else 0
        cpu_time_total_ms = cpu_user_ms + cpu_sys_ms
        return cpu_time_total_ms, cpu_user_ms, cpu_sys_ms
        
    # CALCULATES TOTAL MEMORY ALLOCATIONS IN MB
    def _calculate_allocations(self) -> float:
        alloc_mb_total = 0
        if self.alloc_start and self.alloc_end:
            diff = self.alloc_end.compare_to(self.alloc_start, 'lineno')
            alloc_bytes = sum(stat.size_diff for stat in diff if stat.size_diff > 0)
            alloc_mb_total = alloc_bytes / (1024 * 1024)
        return alloc_mb_total
        
    # CALCULATES GARBAGE COLLECTION METRICS
    def _calculate_gc_stats(self) -> Tuple[float, int]:
        gc_pause_total_ms = 0
        gc_collections_count = 0
        if self.gc_start_stats and self.gc_end_stats:
            end_stats = gc.get_stats()
            start_stats = self.gc_start_stats
            
            if len(start_stats) == len(end_stats):
                for start_stat, end_stat in zip(start_stats, end_stats):
                    start_collections = start_stat.get('collections', 0)
                    end_collections = end_stat.get('collections', 0)
                    gc_collections_count += max(0, end_collections - start_collections)
                    
                    start_time = start_stat.get('total_time', 0)
                    end_time = end_stat.get('total_time', 0)
                    gc_pause_total_ms += max(0, (end_time - start_time) * 1000)  # CONVERT TO MS

        return gc_pause_total_ms, gc_collections_count
        
    # CALCULATES FILESYSTEM I/O METRICS
    def _calculate_fs_io(self) -> Tuple[int, int, int]:
        fs_bytes_read_total = self.fs_read_end - self.fs_read_start if self.fs_read_end is not None and self.fs_read_start is not None else 0
        fs_bytes_written_total = self.fs_write_end - self.fs_write_start if self.fs_write_end is not None and self.fs_write_start is not None else 0
        fs_ops_count = self.fs_ops_end - self.fs_ops_start if self.fs_ops_end is not None and self.fs_ops_start is not None else 0
        return fs_bytes_read_total, fs_bytes_written_total, fs_ops_count

    # CALCULATES AND RETURNS ALL PERFORMANCE METRICS AS A DICTIONARY
    def get_metrics(self) -> Dict:
        if self._current_step: self.step_end()
            
        # CALCULATE ALL METRICS
        total_duration_ms, startup_duration_ms, command_duration_ms = self._calculate_durations()
        cpu_time_total_ms, cpu_user_ms, cpu_sys_ms = self._calculate_cpu_time()
        alloc_mb_total = self._calculate_allocations()
        gc_pause_total_ms, gc_collections_count = self._calculate_gc_stats()
        fs_bytes_read_total, fs_bytes_written_total, fs_ops_count = self._calculate_fs_io()
        
        # MEMORY
        rss_mb_peak = self.rss_peak if self.rss_peak else 0
        
        # TOP SLOWEST STEPS
        top_slowest_steps = sorted(self.steps, key=lambda x: x[1], reverse=True)[:5]
        top_slowest_steps_formatted = [
            {'step': name, 'duration_ms': duration * 1000} 
            for name, duration in top_slowest_steps
        ]
        
        return {
            'total_duration_ms': round(total_duration_ms, 2),
            'startup_duration_ms': round(startup_duration_ms, 2),
            'command_duration_ms': round(command_duration_ms, 2),
            'top_slowest_steps': top_slowest_steps_formatted,
            'cpu_time_total_ms': round(cpu_time_total_ms, 2),
            'cpu_user_ms': round(cpu_user_ms, 2),
            'cpu_sys_ms': round(cpu_sys_ms, 2),
            'rss_mb_peak': round(rss_mb_peak, 2),
            'alloc_mb_total': round(alloc_mb_total, 2),
            'gc_pause_total_ms': round(gc_pause_total_ms, 2),
            'gc_collections_count': gc_collections_count,
            'fs_bytes_read_total': fs_bytes_read_total,
            'fs_bytes_written_total': fs_bytes_written_total,
            'fs_ops_count': fs_ops_count
        }

# GLOBAL METRICS INSTANCE
_metrics = PerformanceMetrics()

# CONTEXT MANAGER FOR TRACKING NAMED STEPS
@contextmanager
def track_step(name: str):
    _metrics.step_start(name)
    try: 
        yield
    finally: 
        _metrics.step_end()

# CHECKS IF PERFORMANCE METRICS SHOULD BE ENABLED
def should_enable_metrics(ctx) -> bool:
    current = ctx
    while current:
        if current.params.get('perf', False): return True
        current = getattr(current, 'parent', None)

    if not ENABLE_PERFORMANCE_METRICS: return False

    module = sys.modules.get('autotools')
    module_file = getattr(module, '__file__', '') or ''
    is_dev = module and 'site-packages' not in module_file.lower()

    return is_dev

# DISPLAYS PERFORMANCE METRICS IN A FORMATTED WAY
def display_metrics(metrics: Dict):
    click.echo(click.style("\n" + "="*60, fg='cyan'))
    click.echo(click.style("PERFORMANCE METRICS", fg='cyan', bold=True))
    click.echo(click.style("="*60, fg='cyan'))
    
    # DURATION METRICS
    click.echo(click.style("\nDURATION METRICS:", fg='yellow', bold=True))
    click.echo(f"  Total Duration:        {metrics['total_duration_ms']:.2f} ms")
    click.echo(f"  Startup Duration:      {metrics['startup_duration_ms']:.2f} ms")
    click.echo(f"  Command Duration:      {metrics['command_duration_ms']:.2f} ms")
    
    # CPU METRICS
    click.echo(click.style("\nCPU METRICS:", fg='yellow', bold=True))
    click.echo(f"  CPU Time Total:        {metrics['cpu_time_total_ms']:.2f} ms")
    click.echo(f"  CPU User Time:         {metrics['cpu_user_ms']:.2f} ms")
    click.echo(f"  CPU System Time:       {metrics['cpu_sys_ms']:.2f} ms")
    cpu_ratio = (metrics['cpu_time_total_ms'] / metrics['total_duration_ms'] * 100) if metrics['total_duration_ms'] > 0 else 0
    click.echo(f"  CPU Usage Ratio:       {cpu_ratio:.1f}%")
    
    # MEMORY METRICS
    click.echo(click.style("\nMEMORY METRICS:", fg='yellow', bold=True))
    click.echo(f"  RSS Peak:              {metrics['rss_mb_peak']:.2f} MB")
    click.echo(f"  Allocations Total:     {metrics['alloc_mb_total']:.2f} MB")
    
    # GC METRICS
    if metrics['gc_collections_count'] > 0 or metrics['gc_pause_total_ms'] > 0:
        click.echo(click.style("\nGARBAGE COLLECTION METRICS:", fg='yellow', bold=True))
        click.echo(f"  GC Pause Total:        {metrics['gc_pause_total_ms']:.2f} ms")
        click.echo(f"  GC Collections:        {metrics['gc_collections_count']}")
    
    # FS I/O METRICS
    if metrics['fs_bytes_read_total'] > 0 or metrics['fs_bytes_written_total'] > 0:
        click.echo(click.style("\nFILESYSTEM I/O METRICS:", fg='yellow', bold=True))
        click.echo(f"  Bytes Read:            {metrics['fs_bytes_read_total']:,} bytes ({metrics['fs_bytes_read_total'] / 1024 / 1024:.2f} MB)")
        click.echo(f"  Bytes Written:         {metrics['fs_bytes_written_total']:,} bytes ({metrics['fs_bytes_written_total'] / 1024 / 1024:.2f} MB)")
        click.echo(f"  FS Operations:         {metrics['fs_ops_count']:,}")
    
    # TOP SLOWEST STEPS
    if metrics['top_slowest_steps']:
        click.echo(click.style("\nTOP SLOWEST STEPS:", fg='yellow', bold=True))
        for i, step in enumerate(metrics['top_slowest_steps'], 1): click.echo(f"  {i}. {step['step']}: {step['duration_ms']:.2f} ms")
    
    click.echo(click.style("\n" + "="*60 + "\n", fg='cyan'))

# INITIALIZES METRICS TRACKING
def init_metrics():
    _metrics.reset()
    _metrics.start_process()
    _metrics.start_startup()

# FINALIZES AND DISPLAYS METRICS IF ENABLED
def finalize_metrics(ctx):
    if should_enable_metrics(ctx):
        _metrics.end_process()
        metrics = _metrics.get_metrics()
        display_metrics(metrics)

# GETS THE GLOBAL METRICS INSTANCE
def get_metrics() -> PerformanceMetrics: return _metrics
