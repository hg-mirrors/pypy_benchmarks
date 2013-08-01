#!/usr/bin/env python

"""Tool for comparing the performance of two Python implementations.

Typical usage looks like

./perf.py -b 2to3,django control/python experiment/python

This will run the 2to3 and Django template benchmarks, using `control/python`
as the baseline and `experiment/python` as the experiment. The --fast and
--rigorous options can be used to vary the duration/accuracy of the run. Run
--help to get a full list of options that can be passed to -b.

Omitting the -b option will result in the default group of benchmarks being run
This currently consists of: 2to3, django, nbody, slowspitfire, slowpickle,
slowunpickle, spambayes. Omitting -b is the same as specifying `-b default`.

To run every benchmark perf.py knows about, use `-b all`. To see a full list of
all available benchmarks, use `--help`.

Negative benchmarks specifications are also supported: `-b -2to3` will run every
benchmark in the default group except for 2to3 (this is the same as
`-b default,-2to3`). `-b all,-django` will run all benchmarks except the Django
templates benchmark. Negative groups (e.g., `-b -default`) are not supported.
Positive benchmarks are parsed before the negative benchmarks are subtracted.

If --track_memory is passed, perf.py will continuously sample the benchmark's
memory usage, then give you the maximum usage and a link to a Google Chart of
the benchmark's memory usage over time. This currently only works on Linux
2.6.16 and higher or Windows with PyWin32. Because --track_memory introduces
performance jitter while collecting memory measurements, only memory usage is
reported in the final report.

If --args is passed, it specifies extra arguments to pass to the test
python binaries. For example,
  perf.py --args="-A -B,-C -D" base_python changed_python
will run benchmarks like
  base_python -A -B the_benchmark.py
  changed_python -C -D the_benchmark.py
while
  perf.py --args="-A -B" base_python changed_python
will pass the same arguments to both pythons:
  base_python -A -B the_benchmark.py
  changed_python -A -B the_benchmark.py
"""

from __future__ import division, with_statement

__author__ = "jyasskin@google.com (Jeffrey Yasskin)"

import contextlib
import logging
import math
import optparse
import os
import os.path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import threading
import urllib2
try:
    import multiprocessing
except ImportError:
    multiprocessing = None
try:
    import win32api
    import win32con
    import win32process
    import pywintypes
except ImportError:
    win32api = None


info = logging.info


def avg(seq):
    return sum(seq) / float(len(seq))


def SampleStdDev(seq):
    """Compute the standard deviation of a sample.

    Args:
        seq: the numeric input data sequence.

    Returns:
        The standard deviation as a float.
    """
    mean = avg(seq)
    squares = ((x - mean) ** 2 for x in seq)
    return math.sqrt(sum(squares) / (len(seq) - 1))


# A table of 95% confidence intervals for a two-tailed t distribution, as a
# function of the degrees of freedom. For larger degrees of freedom, we
# approximate. While this may look less elegant than simply calculating the
# critical value, those calculations suck. Look at
# http://www.math.unb.ca/~knight/utility/t-table.htm if you need more values.
T_DIST_95_CONF_LEVELS = [0, 12.706, 4.303, 3.182, 2.776,
                         2.571, 2.447, 2.365, 2.306, 2.262,
                         2.228, 2.201, 2.179, 2.160, 2.145,
                         2.131, 2.120, 2.110, 2.101, 2.093,
                         2.086, 2.080, 2.074, 2.069, 2.064,
                         2.060, 2.056, 2.052, 2.048, 2.045,
                         2.042]


def TDist95ConfLevel(df):
    """Approximate the 95% confidence interval for Student's T distribution.

    Given the degrees of freedom, returns an approximation to the 95%
    confidence interval for the Student's T distribution.

    Args:
        df: An integer, the number of degrees of freedom.

    Returns:
        A float.
    """
    df = int(round(df))
    highest_table_df = len(T_DIST_95_CONF_LEVELS)
    if df >= 200: return 1.960
    if df >= 100: return 1.984
    if df >= 80: return 1.990
    if df >= 60: return 2.000
    if df >= 50: return 2.009
    if df >= 40: return 2.021
    if df >= highest_table_df:
        return T_DIST_95_CONF_LEVELS[highest_table_df - 1]
    return T_DIST_95_CONF_LEVELS[df]


def PooledSampleVariance(sample1, sample2):
    """Find the pooled sample variance for two samples.

    Args:
        sample1: one sample.
        sample2: the other sample.

    Returns:
        Pooled sample variance, as a float.
    """
    deg_freedom = len(sample1) + len(sample2) - 2
    mean1 = avg(sample1)
    squares1 = ((x - mean1) ** 2 for x in sample1)
    mean2 = avg(sample2)
    squares2 = ((x - mean2) ** 2 for x in sample2)

    return (sum(squares1) + sum(squares2)) / float(deg_freedom)


def TScore(sample1, sample2):
    """Calculate a t-test score for the difference between two samples.

    Args:
        sample1: one sample.
        sample2: the other sample.

    Returns:
        The t-test score, as a float.
    """
    assert len(sample1) == len(sample2)
    error = PooledSampleVariance(sample1, sample2) / len(sample1)
    try:
        return (avg(sample1) - avg(sample2)) / math.sqrt(error * 2)
    except ZeroDivisionError:
        return 0.0


def IsSignificant(sample1, sample2):
    """Determine whether two samples differ significantly.

    This uses a Student's two-sample, two-tailed t-test with alpha=0.95.

    Args:
        sample1: one sample.
        sample2: the other sample.

    Returns:
        (significant, t_score) where significant is a bool indicating whether
        the two samples differ significantly; t_score is the score from the
        two-sample T test.
    """
    deg_freedom = len(sample1) + len(sample2) - 2
    critical_value = TDist95ConfLevel(deg_freedom)
    t_score = TScore(sample1, sample2)
    return (abs(t_score) >= critical_value, t_score)


### Code to parse Linux /proc/%d/smaps files.
### See http://bmaurer.blogspot.com/2006/03/memory-usage-with-smaps.html for
### a quick introduction to smaps.

def _ParseSmapsData(smaps_data):
    """Parse the contents of a Linux 2.6 smaps file.

    Args:
        smaps_data: the smaps file contents, as a string.

    Returns:
        The size of the process's private data, in kilobytes.
    """
    total = 0
    for line in smaps_data.splitlines():
        # Include both Private_Clean and Private_Dirty sections.
        if line.startswith("Private_"):
            parts = line.split()
            total += int(parts[1])
    return total


def _ReadSmapsFile(pid):
    """Read the Linux smaps file for a pid.

    Args:
        pid: the process id to retrieve smaps data for.

    Returns:
        The data from the smaps file, as a string.

    Raises:
        IOError if the smaps file for the given pid could not be found.
    """
    with open("/proc/%d/smaps" % pid) as f:
        return f.read()


# Code to sample memory usage on Win32

def _GetWin32MemorySample(process_handle):
    """Gets the amount of memory in use by a process on Win32

    Args:
        process_handle: handle to the process to get the memory usage for

    Returns:
        The size of the process's private data, in kilobytes
    """
    pmi = win32process.GetProcessMemoryInfo(process_handle)
    return pmi["PagefileUsage"] // 1024


@contextlib.contextmanager
def _OpenWin32Process(pid):
    """Open a process on Win32 and close it when done

    Args:
        pid: the process id of the process to open

    Yields:
        A handle to the process

    Raises:
        pywintypes.error if the process does not exist or the user
            does not have sufficient privileges to open it

    Example:
        with _OpenWin32Process(pid) as process_handle:
            ...
    """
    h = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
            0,
            pid)
    try:
        yield h
    finally:
        win32api.CloseHandle(h)


def CanGetMemoryUsage():
    """Returns True if MemoryUsageFuture is supported on this platform."""
    if win32api:
        try:
            with _OpenWin32Process(win32process.GetCurrentProcessId()):
                return True
        except pywintypes.error:
            pass

    try:
        import os
        _ReadSmapsFile(pid=os.getpid())
    except IOError:
        pass
    else:
        return True

    return False


class MemoryUsageFuture(threading.Thread):
    """Continuously sample a process's memory usage for its lifetime.

    Example:
        future = MemoryUsageFuture(some_pid)
        ...
        usage = future.GetMemoryUsage()
        print max(usage)

    Note that calls to GetMemoryUsage() will block until the process exits.
    """

    def __init__(self, pid):
        super(MemoryUsageFuture, self).__init__()
        self._pid = pid
        self._usage = []
        self._done = threading.Event()
        self.start()

    def run(self):
        if win32api:
            with _OpenWin32Process(self._pid) as process_handle:
                while (win32process.GetExitCodeProcess(process_handle) ==
                       win32con.STILL_ACTIVE):
                    sample = _GetWin32MemorySample(process_handle)
                    self._usage.append(sample)
                    time.sleep(0.001)
        else:
            while True:
                try:
                    sample = _ParseSmapsData(_ReadSmapsFile(self._pid))
                    self._usage.append(sample)
                except IOError:
                    # Once the process exits, its smaps file will go away,
                    # leading _ReadSmapsFile() to raise IOError.
                    break
        self._done.set()

    def GetMemoryUsage(self):
        """Get the memory usage over time for the process being sampled.

        This will block until the process has exited.

        Returns:
            A list of all memory usage samples, in kilobytes.
        """
        self._done.wait()
        return self._usage

class Result(object):
    """ An object representing a result of run. Can be converted to
    a string by calling string_representation
    """
    def __init__(self, times, min_time, avg_time, std_time):
        self.times = times
        self.min_time = min_time
        self.avg_time = avg_time
        self.std_time = std_time

    def string_representation(self):
        return "Time: %(min_time)f +- %(std_time)f" % self.__dict__

class ResultError(object):
    def __init__(self, e):
        self.msg = str(e)

    def string_representation(self):
        return self.msg

class MemoryUsageResult(object):
    def __init__(self, max_base, max_changed, delta_max, chart_link):
        self.max_base = max_base
        self.max_changed = max_changed
        self.delta_max = delta_max
        self.chart_link = chart_link

    def get_usage_over_time(self):
        if self.chart_link is None:
            return ""
        return "Usage over time: %(chart_link)s"

    def string_representation(self):
        return (("Mem max: %(max_base).3f -> %(max_changed).3f:" +
                 " %(delta_max)s\n" + self.get_usage_over_time())
                 % self.__dict__)

class SimpleResult(object):
    def __init__(self, time):
        self.time = time

    def string_representation(self):
        return ("%(time)f"
                % self.__dict__)

class RawResult(object):
    def __init__(self, times):
        self.times = times

    def string_representation(self):
        return "Raw results: %s" % (self.times,)

def CompareMemoryUsage(base_usage, changed_usage, options):
    """Like CompareMultipleRuns, but for memory usage."""
    max_base, max_changed = max(base_usage), max(changed_usage)
    delta_max = QuantityDelta(max_base, max_changed)

    return MemoryUsageResult(max_base, max_changed, delta_max, "")

### Utility functions

def SimpleBenchmark(benchmark_function, python, options,
                    *args, **kwargs):
    """Abstract out the body for most simple benchmarks.

    Example usage:
        def BenchmarkSomething(*args, **kwargs):
            return SimpleBenchmark(MeasureSomething, *args, **kwargs)

    The *args, **kwargs style is recommended so as to minimize the number of
    places that have to be changed if we update benchmark arguments.

    Args:
        benchmark_function: callback that takes (python_path, options) and
            returns a (times, memory_usage) 2-tuple.
        options: optparse.Values instance.
        *args, **kwargs: will be passed through to benchmark_function.

    Returns:
        An object representing differences between the two benchmark runs.
        Comes with string_representation method.
    """
    try:
        data = benchmark_function(python, options,
                                  *args, **kwargs)
    except subprocess.CalledProcessError, e:
        return ResultError(e)

    return CompareBenchmarkData(data, options)


def ShortenUrl(url):
    """Shorten a given URL using tinyurl.com.

    Args:
        url: url to shorten.

    Returns:
        Shorter url. If tinyurl.com is not available, returns the original
        url unaltered.
    """
    tinyurl_api = "http://tinyurl.com/api-create.php?url="
    try:
        url = urllib2.urlopen(tinyurl_api + url).read()
    except urllib2.URLError:
        info("failed to call out to tinyurl.com")
    return url


def SummarizeData(data, points=100, summary_func=max):
    """Summarize a large data set using a smaller number of points.

    This will divide up the original data set into `points` windows,
    using `summary_func` to summarize each window into a single point.

    Args:
        data: the original data set, as a list.
        points: optional; how many summary points to take. Default is 100.
        summary_func: optional; function to use when summarizing each window.
            Default is the max() built-in.

    Returns:
        List of summary data points.
    """
    window_size = int(math.ceil(len(data) / points))
    if window_size == 1:
        return data

    summary_points = []
    start = 0
    while start < len(data):
        end = min(start + window_size, len(data))
        summary_points.append(summary_func(data[start:end]))
        start = end
    return summary_points


@contextlib.contextmanager
def ChangeDir(new_cwd):
    former_cwd = os.getcwd()
    os.chdir(new_cwd)
    try:
        yield
    finally:
        os.chdir(former_cwd)


def RemovePycs():
    if sys.platform == "win32":
        for root, dirs, files in os.walk('.'):
            for name in files:
                if name.endswith('.pyc') or name.endswith('.pyo'):
                    os.remove(os.path.join(root, name))
    else:
        subprocess.check_call(["find", ".", "-name", "*.py[co]",
                               "-exec", "rm", "-f", "{}", ";"])


def Relative(path):
    return os.path.join(os.path.dirname(__file__), path)


def LogCall(command):
    command = map(str, command)
    info("Running %s", " ".join(command))
    return command


try:
    import resource
except ImportError:
    # Approximate child time using wall clock time.
    def GetChildUserTime():
        return time.time()
else:
    def GetChildUserTime():
        return resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime


@contextlib.contextmanager
def TemporaryFilename(prefix):
    fd, name = tempfile.mkstemp(prefix=prefix)
    os.close(fd)
    try:
        yield name
    finally:
        os.remove(name)


def TimeDelta(old, new):
    if new > old:
        return "%.4fx slower" % (new / old)
    elif new < old:
        return "%.4fx faster" % (old / new)
    else:
        return "no change"


def QuantityDelta(old, new):
    if old == 0 or new == 0:
        return "uncomparable"
    if new > old:
        return "%.4fx larger" % (new / old)
    elif new < old:
        return "%.4fx smaller" % (old / new)
    else:
        return "no change"


def BuildEnv(env=None, inherit_env=[]):
    """Massage an environment variables dict for the host platform.

    Platforms like Win32 require certain env vars to be set.

    Args:
        env: environment variables dict.
        whitelist: environment variables to inherit from parent environment.

    Returns:
        A copy of `env`, possibly with modifications.
    """
    if env == None:
        env = {}
    fixed_env = env.copy()
    for varname in inherit_env:
        fixed_env[varname] = os.environ[varname]
    if sys.platform == "win32":
        # Win32 requires certain environment variables be present
        for k in ("COMSPEC", "SystemRoot"):
            if k in os.environ and k not in fixed_env:
                fixed_env[k] = os.environ[k]
    return fixed_env


def CompareMultipleRuns(times, options):
    """Compare multiple control vs experiment runs of the same benchmark.

    Args:
        base_times: iterable of float times (control).
        changed_times: iterable of float times (experiment).
        options: optparse.Values instance.

    Returns:
        A string summarizing the difference between the runs, suitable for
        human consumption.
    """
    if options.no_statistics:
        return RawResult(times)
    if len(times) == 1:
        # With only one data point, we can't do any of the interesting stats
        # below.
        return SimpleResult(times[0])

    times = sorted(times)

    min_time = times[0]
    avg_time = avg(times)
    std_time = SampleStdDev(times)

    return Result(times, min_time, avg_time, std_time)

def CompareBenchmarkData(data, options):
    """Compare performance and memory usage.

    Args:
        data: 2-tuple of (times, mem_usage) where times is an iterable
            of floats; mem_usage is a list of memory usage samples.
        options: optparse.Values instance.

    Returns:
        Human-readable summary of the difference between the base and changed
        binaries.
    """
    times, mem = data

    # We suppress performance data when running with --track_memory.
    if options.track_memory:
        if mem is not None:
            XXX # we don't track memory
            return CompareMemoryUsage(base_mem, changed_mem, options)
        return "Benchmark does not report memory usage yet"

    return CompareMultipleRuns(times, options)


def CallAndCaptureOutput(command, env=None, track_memory=False, inherit_env=[]):
    """Run the given command, capturing stdout.

    Args:
        command: the command to run as a list, one argument per element.
        env: optional; environment variables to set.
        track_memory: optional; whether to continuously sample the subprocess's
            memory usage.

    Returns:
        (stdout, mem_usage), where stdout is the captured stdout as a string;
        mem_usage is a list of memory usage samples in kilobytes (if
        track_memory is False, mem_usage is None).

    Raises:
        RuntimeError: if the command failed. The value of the exception will
        be the error message from the command.
    """
    mem_usage = None
    subproc = subprocess.Popen(LogCall(command),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               env=BuildEnv(env, inherit_env))
    if track_memory:
        future = MemoryUsageFuture(subproc.pid)
    result, err = subproc.communicate()
    if subproc.returncode != 0:
        print result
        raise RuntimeError("Benchmark died (returncode: %d): %s" %
                           (subproc.returncode, err))
    if track_memory:
        mem_usage = future.GetMemoryUsage()
    return result, mem_usage


def MeasureGeneric(python, options, bm_path, bm_env=None,
                   extra_args=[], iteration_scaling=1, parser=float):
    """Abstract measurement function for Unladen's bm_* scripts.

    Based on the values of options.fast/rigorous, will pass -n {5,50,100} to
    the benchmark script. MeasureGeneric takes care of parsing out the running
    times from the memory usage data.

    Args:
        python: start of the argv list for running Python.
        options: optparse.Values instance.
        bm_path: path to the benchmark script.
        bm_env: optional environment dict. If this is unspecified or None,
            use an empty enviroment.
        extra_args: optional list of command line args to be given to the
            benchmark script.
        iteration_scaling: optional multiple by which to scale the -n argument
            to the benchmark.

    Returns:
        (times, mem_usage) 2-tuple, where times is a list of floats giving the
        running time of the benchmark iterations; and mem_usage is a list of
        floats giving memory usage samples.
    """
    if bm_env is None:
        bm_env = {}

    trials = 50
    if options.rigorous:
        trials = 100
    elif options.fast:
        trials = 5
    trials = max(1, int(trials * iteration_scaling))

    RemovePycs()
    command = python + [bm_path, "-n", trials] + extra_args
    result, mem_usage = CallAndCaptureOutput(command, bm_env,
                                             track_memory=options.track_memory,
                                             inherit_env=options.inherit_env)
    times = [parser(line) for line in result.splitlines()]
    return times, mem_usage


### Benchmarks

_PY_BENCH_TOTALS_LINE = re.compile("""
    Totals:\s+(?P<min_base>\d+)ms\s+
    (?P<min_changed>\d+)ms\s+
    \S+\s+  # Percent change, which we re-compute
    (?P<avg_base>\d+)ms\s+
    (?P<avg_changed>\d+)ms\s+
    \S+  # Second percent change, also re-computed
    """, re.X)
def MungePyBenchTotals(line):
    m = _PY_BENCH_TOTALS_LINE.search(line)
    if m:
        min_base, min_changed, avg_base, avg_changed = map(float, m.group(
            "min_base", "min_changed", "avg_base", "avg_changed"))
        delta_min = TimeDelta(min_base, min_changed)
        delta_avg = TimeDelta(avg_base, avg_changed)
        return (("Min: %(min_base)d -> %(min_changed)d: %(delta_min)s\n" +
                 "Avg: %(avg_base)d -> %(avg_changed)d: %(delta_avg)s")
                % locals())
    return line


def BM_PyBench(base_python, changed_python, options):
    if options.track_memory:
        return "Benchmark does not report memory usage yet"

    warp = "10"
    if options.rigorous:
        warp = "1"
    if options.fast:
        warp = "100"

    PYBENCH_PATH = Relative("performance/pybench/pybench.py")
    PYBENCH_ENV = BuildEnv({"PYTHONPATH": ""}, inherit_env=options.inherit_env)

    try:
        with contextlib.nested(open(os.devnull, "wb"),
                               TemporaryFilename(prefix="baseline."),
                               TemporaryFilename(prefix="changed.")
                               ) as (dev_null, base_pybench, changed_pybench):
            RemovePycs()
            subprocess.check_call(LogCall(changed_python + [
                                           PYBENCH_PATH,
                                           "-w", warp,
                                           "-f", changed_pybench,
                                           ]), stdout=dev_null,
                                           env=PYBENCH_ENV)
            RemovePycs()
            subprocess.check_call(LogCall(base_python + [
                                           PYBENCH_PATH,
                                           "-w", warp,
                                           "-f", base_pybench,
                                           ]), stdout=dev_null,
                                           env=PYBENCH_ENV)
            comparer = subprocess.Popen(base_python + [
                                         PYBENCH_PATH,
                                         "--debug",
                                         "-s", base_pybench,
                                         "-c", changed_pybench,
                                         ], stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         env=PYBENCH_ENV)
            result, err = comparer.communicate()
            if comparer.returncode != 0:
                return "pybench died: " + err
    except subprocess.CalledProcessError, e:
        return str(e)

    if options.verbose:
        return result
    else:
        for line in result.splitlines():
            if line.startswith("Totals:"):
                return MungePyBenchTotals(line)
        # The format's wrong...
        return result


def Measure2to3(python, options):
    FAST_TARGET = Relative("lib/2to3/lib2to3/refactor.py")
    TWO_TO_THREE_PROG = Relative("lib/2to3/2to3")
    TWO_TO_THREE_DIR = Relative("lib/2to3")
    TWO_TO_THREE_ENV = BuildEnv({"PYTHONPATH": ""}, inherit_env=options.inherit_env)

    if options.fast:
        target = FAST_TARGET
    else:
        target = TWO_TO_THREE_DIR

    with open(os.devnull, "wb") as dev_null:
        RemovePycs()
        # Warm up the cache and .pyc files. Use CallAndCaptureOutput() for its
        # more useful error messages.
        CallAndCaptureOutput(python +
                             [TWO_TO_THREE_PROG, "-f", "all", target],
                             env=TWO_TO_THREE_ENV, inherit_env=options.inherit_env)
        if options.rigorous:
            trials = 5
        else:
            trials = 1
        times = []
        mem_usage = []
        for _ in range(trials):
            start_time = GetChildUserTime()
            subproc = subprocess.Popen(LogCall(python + [
                                                TWO_TO_THREE_PROG,
                                                "-f", "all",
                                                target]),
                                       stdout=dev_null, stderr=subprocess.PIPE,
                                       env=TWO_TO_THREE_ENV)
            if options.track_memory:
                future = MemoryUsageFuture(subproc.pid)
            _, err = subproc.communicate()
            if subproc.returncode != 0:
                raise RuntimeError("Benchmark died: " + err)
            if options.track_memory:
                mem_samples = future.GetMemoryUsage()
            end_time = GetChildUserTime()
            elapsed = end_time - start_time
            assert elapsed != 0
            times.append(elapsed)
            if options.track_memory:
                mem_usage.extend(mem_samples)

    if not options.track_memory:
        mem_usage = None
    return times, mem_usage


def BM_2to3(*args, **kwargs):
    return SimpleBenchmark(Measure2to3, *args, **kwargs)


DJANGO_DIR = Relative("lib/django")


def MeasureDjango(python, options):
    bm_path = Relative("performance/bm_django.py")
    bm_env = {"PYTHONPATH": DJANGO_DIR}
    return MeasureGeneric(python, options, bm_path, bm_env)


def BM_Django(*args, **kwargs):
    return SimpleBenchmark(MeasureDjango, *args, **kwargs)


def MeasureRietveld(python, options):
    PYTHONPATH = ":".join([DJANGO_DIR,
                           # These paths are lifted from
                           # lib/google_appengine.appcfg.py.  Note that we use
                           # our own version of Django instead of Appengine's.
                           Relative("lib/google_appengine"),
                           Relative("lib/google_appengine/lib/antlr3"),
                           Relative("lib/google_appengine/lib/webob"),
                           Relative("lib/google_appengine/lib/yaml/lib"),
                           Relative("lib/rietveld")])
    bm_path = Relative("performance/bm_rietveld.py")
    bm_env = {"PYTHONPATH": PYTHONPATH, "DJANGO_SETTINGS_MODULE": "settings"}

    return MeasureGeneric(python, options, bm_path, bm_env)


def BM_Rietveld(*args, **kwargs):
    return SimpleBenchmark(MeasureRietveld, *args, **kwargs)


def _ComesWithPsyco(python):
    """Determine whether the given Python binary already has Psyco.

    If the answer is no, we should build it (see BuildPsyco()).

    Args:
        python: prefix of a command line for the Python binary.

    Returns:
        True if we can "import psyco" with the given Python, False if not.
    """
    try:
        with open(os.devnull, "wb") as dev_null:
            subprocess.check_call(python + ["-c", "import psyco"],
                                  stdout=dev_null, stderr=dev_null, env=BuildEnv())
        return True
    except subprocess.CalledProcessError:
        return False


def _BuildPsyco(python):
    """Build Psyco against the given Python binary.

    Args:
        python: prefix of a command line for the Python binary.

    Returns:
        Path to Psyco's build directory. Putting this on your PYTHONPATH will
        make "import psyco" work.
    """
    PSYCO_SRC_DIR = Relative("lib/psyco")

    info("Building Psyco for %s", python)
    psyco_build_dir = tempfile.mkdtemp()
    abs_python = os.path.abspath(python[0])
    with ChangeDir(PSYCO_SRC_DIR):
        subprocess.check_call(LogCall([abs_python, "setup.py", "build",
                                       "--build-lib=" + psyco_build_dir]))
    return psyco_build_dir


def MeasureSpitfire(python, options, env=None, extra_args=[]):
    """Use Spitfire to test a Python binary's performance.

    Args:
        python: prefix of a command line for the Python binary to test.
        options: optparse.Values instance.
        env: optional; dict of environment variables to pass to Python.
        extra_args: optional; list of arguments to append to the Python
            command.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run the Spitfire test once; mem_usage is a list of
        memory usage samples in kilobytes.
    """
    bm_path = Relative("performance/bm_spitfire.py")
    return MeasureGeneric(python, options, bm_path, env, extra_args)


def MeasureSpitfireWithPsyco(python, options):
    """Use Spitfire to measure Python's performance.

    Args:
        python: prefix of a command line for the Python binary.
        options: optparse.Values instance.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run the Spitfire test once; mem_usage is a list of
        memory usage samples in kilobytes.
    """
    SPITFIRE_DIR = Relative("lib/spitfire")

    psyco_dir = ""
    if not _ComesWithPsyco(python):
        psyco_dir = _BuildPsyco(python)

    env_dirs = filter(bool, [SPITFIRE_DIR, psyco_dir])
    spitfire_env = {"PYTHONPATH": os.pathsep.join(env_dirs)}

    try:
        return MeasureSpitfire(python, options, spitfire_env)
    finally:
        try:
            shutil.rmtree(psyco_dir)
        except OSError:
            pass


def BM_Spitfire(*args, **kwargs):
    return SimpleBenchmark(MeasureSpitfireWithPsyco, *args, **kwargs)


def BM_SlowSpitfire(python, options):
    extra_args = ["--disable_psyco"]
    spitfire_env = {"PYTHONPATH": Relative("lib/spitfire")}

    try:
        data = MeasureSpitfire(python, options,
                               spitfire_env, extra_args)
    except subprocess.CalledProcessError, e:
        return str(e)

    return CompareBenchmarkData(data, options)


def MeasurePickle(python, options, extra_args):
    """Test the performance of Python's pickle implementations.

    Args:
        python: prefix of a command line for the Python binary.
        options: optparse.Values instance.
        extra_args: list of arguments to append to the command line.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run the pickle test once; mem_usage is a list of
        memory usage samples in kilobytes.
    """
    bm_path = Relative("performance/bm_pickle.py")
    return MeasureGeneric(python, options, bm_path, extra_args=extra_args)


def _PickleBenchmark(base_python, changed_python, options, extra_args):
    """Test the performance of Python's pickle implementations.

    Args:
        base_python: prefix of a command line for the reference
                Python binary.
        changed_python: prefix of a command line for the
                experimental Python binary.
        options: optparse.Values instance.
        extra_args: list of arguments to append to the command line.

    Returns:
        Summary of whether the experiemental Python is better/worse than the
        baseline.
    """
    return SimpleBenchmark(MeasurePickle,
                           base_python, changed_python, options, extra_args)


def BM_Pickle(base_python, changed_python, options):
    args = ["--use_cpickle", "pickle"]
    return _PickleBenchmark(base_python, changed_python, options, args)

def BM_Unpickle(base_python, changed_python, options):
    args = ["--use_cpickle", "unpickle"]
    return _PickleBenchmark(base_python, changed_python, options, args)

def BM_Pickle_List(base_python, changed_python, options):
    args = ["--use_cpickle", "pickle_list"]
    return _PickleBenchmark(base_python, changed_python, options, args)

def BM_Unpickle_List(base_python, changed_python, options):
    args = ["--use_cpickle", "unpickle_list"]
    return _PickleBenchmark(base_python, changed_python, options, args)

def BM_Pickle_Dict(base_python, changed_python, options):
    args = ["--use_cpickle", "pickle_dict"]
    return _PickleBenchmark(base_python, changed_python, options, args)

def BM_SlowPickle(base_python, changed_python, options):
    return _PickleBenchmark(base_python, changed_python, options, ["pickle"])

def BM_SlowUnpickle(base_python, changed_python, options):
    return _PickleBenchmark(base_python, changed_python, options, ["unpickle"])


def MeasureAi(python, options):
    """Test the performance of some small AI problem solvers.

    Args:
        python: prefix of a command line for the Python binary.
        options: optparse.Values instance.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run the ai routine once; mem_usage is a list of
        memory usage samples in kilobytes.
    """
    bm_path = Relative("performance/bm_ai.py")
    return MeasureGeneric(python, options, bm_path)


def BM_Ai(*args, **kwargs):
    return SimpleBenchmark(MeasureAi, *args, **kwargs)


def _StartupPython(command, mem_usage, track_memory, inherit_env):
    startup_env = BuildEnv(inherit_env=inherit_env)
    if not track_memory:
        subprocess.check_call(command, env=startup_env)
    else:
        subproc = subprocess.Popen(command, env=startup_env)
        future = MemoryUsageFuture(subproc.pid)
        if subproc.wait() != 0:
            raise RuntimeError("Startup benchmark died")
        mem_usage.extend(future.GetMemoryUsage())


def MeasureStartup(python, cmd_opts, num_loops, track_memory, inherit_env):
    times = []
    work = ""
    if track_memory:
        # Without this, Python may start and exit before the memory sampler
        # thread has time to work. We can't just do 'time.sleep(x)', because
        # under -S, 'import time' fails.
        work = "for _ in xrange(200000): pass"
    command = python + cmd_opts + ["-c", work]
    mem_usage = []
    info("Running `%s` %d times", command, num_loops * 20)
    for _ in xrange(num_loops):
        t0 = time.time()
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        _StartupPython(command, mem_usage, track_memory, inherit_env)
        t1 = time.time()
        times.append(t1 - t0)
    if not track_memory:
      mem_usage = None
    return times, mem_usage


def BM_normal_startup(base_python, changed_python, options):
    if options.rigorous:
        num_loops = 100
    elif options.fast:
        num_loops = 5
    else:
        num_loops = 50

    opts = []
    changed_data = MeasureStartup(changed_python, opts, num_loops,
                                  options.track_memory, options.inherit_env)
    base_data = MeasureStartup(base_python, opts, num_loops,
                               options.track_memory, options.inherit_env)

    return CompareBenchmarkData(base_data, changed_data, options)


def BM_startup_nosite(base_python, changed_python, options):
    if options.rigorous:
        num_loops = 200
    elif options.fast:
        num_loops = 10
    else:
        num_loops = 100

    opts = ["-S"]
    changed_data = MeasureStartup(changed_python, opts, num_loops,
                                  options.track_memory, options.inherit_env)
    base_data = MeasureStartup(base_python, opts, num_loops,
                               options.track_memory, options.inherit_env)

    return CompareBenchmarkData(base_data, changed_data, options)


def MeasureRegexPerformance(python, options, bm_path):
    """Test the performance of Python's regex engine.

    Args:
        python: prefix of a command line for the Python binary.
        options: optparse.Values instance.
        bm_path: relative path; which benchmark script to run.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run all the regexes routines once; mem_usage is a list
        of memory usage samples in kilobytes.
    """
    return MeasureGeneric(python, options, Relative(bm_path))


def RegexBenchmark(base_python, changed_python, options, bm_path):
    return SimpleBenchmark(MeasureRegexPerformance,
                           base_python, changed_python, options, bm_path)


def BM_regex_v8(base_python, changed_python, options):
    bm_path = "performance/bm_regex_v8.py"
    return RegexBenchmark(base_python, changed_python, options, bm_path)


def BM_regex_effbot(base_python, changed_python, options):
    bm_path = "performance/bm_regex_effbot.py"
    return RegexBenchmark(base_python, changed_python, options, bm_path)


def BM_regex_compile(base_python, changed_python, options):
    bm_path = "performance/bm_regex_compile.py"
    return RegexBenchmark(base_python, changed_python, options, bm_path)


def MeasureThreading(python, options, bm_name):
    """Test the performance of Python's threading support.

    Args:
        python: prefix of a command line for the Python binary.
        options: optparse.Values instance.
        bm_name: name of the threading benchmark to run.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run the threading benchmark once; mem_usage is a list
        of memory usage samples in kilobytes.
    """
    bm_path = Relative("performance/bm_threading.py")
    return MeasureGeneric(python, options, bm_path, extra_args=[bm_name])


def ThreadingBenchmark(base_python, changed_python, options, bm_name):
    return SimpleBenchmark(MeasureThreading,
                           base_python, changed_python, options, bm_name)


def BM_threaded_count(base_python, changed_python, options):
    bm_name = "threaded_count"
    return ThreadingBenchmark(base_python, changed_python, options, bm_name)


def BM_iterative_count(base_python, changed_python, options):
    bm_name = "iterative_count"
    return ThreadingBenchmark(base_python, changed_python, options, bm_name)


def MeasureUnpackSequence(python, options):
    """Test the performance of sequence unpacking.

    Args:
        python: prefix of a command line for the Python binary.
        options: optparse.Values instance.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run the threading benchmark once; mem_usage is a list
        of memory usage samples in kilobytes.
    """
    bm_path = Relative("performance/bm_unpack_sequence.py")
    return MeasureGeneric(python, options, bm_path, iteration_scaling=1000)


def BM_unpack_sequence(*args, **kwargs):
    return SimpleBenchmark(MeasureUnpackSequence, *args, **kwargs)


def MeasureCallSimple(python, options):
    """Test the performance of simple function calls.

    Args:
        python: prefix of a command line for the Python binary.
        options: optparse.Values instance.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run the threading benchmark once; mem_usage is a list
        of memory usage samples in kilobytes.
    """
    bm_path = Relative("performance/bm_call_simple.py")
    return MeasureGeneric(python, options, bm_path)


def BM_call_simple(*args, **kwargs):
    return SimpleBenchmark(MeasureCallSimple, *args, **kwargs)


def MeasureNbody(python, options):
    """Test the performance of math operations using an n-body benchmark.

    Args:
        python: prefix of a command line for the Python binary.
        options: optparse.Values instance.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run the benchmark loop once; mem_usage is a list
        of memory usage samples in kilobytes.
    """
    bm_path = Relative("performance/bm_nbody.py")
    return MeasureGeneric(python, options, bm_path)


def BM_nbody(*args, **kwargs):
    return SimpleBenchmark(MeasureNbody, *args, **kwargs)


def MeasureSpamBayes(python, options):
    """Test the performance of the SpamBayes spam filter and its tokenizer.

    Args:
        python: prefix of a command line for the Python binary.
        options: optparse.Values instance.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run the benchmark loop once; mem_usage is a list
        of memory usage samples in kilobytes.
    """
    pypath = ":".join([Relative("lib/spambayes"), Relative("lib/lockfile")])
    bm_path = Relative("performance/bm_spambayes.py")
    bm_env = {"PYTHONPATH": pypath}
    return MeasureGeneric(python, options, bm_path, bm_env)


def BM_spambayes(*args, **kwargs):
    return SimpleBenchmark(MeasureSpamBayes, *args, **kwargs)


def MeasureHtml5lib(python, options):
    """Test the performance of the html5lib HTML 5 parser.

    Args:
        python: prefix of a command line for the Python binary.
        options: optparse.Values instance.

    Returns:
        (perf_data, mem_usage), where perf_data is a list of floats, each the
        time it took to run the benchmark loop once; mem_usage is a list
        of memory usage samples in kilobytes.
    """
    bm_path = Relative("performance/bm_html5lib.py")
    bm_env = {"PYTHONPATH": Relative("lib/html5lib")}
    return MeasureGeneric(python, options, bm_path, bm_env,
                          iteration_scaling=0.10)


def BM_html5lib(*args, **kwargs):
    return SimpleBenchmark(MeasureHtml5lib, *args, **kwargs)

def MeasureRichards(python, options):
    bm_path = Relative("performance/bm_richards.py")
    return MeasureGeneric(python, options, bm_path)

def BM_richards(*args, **kwargs):
    return SimpleBenchmark(MeasureRichards, *args, **kwargs)

### End benchmarks, begin main entry point support.

def _FindAllBenchmarks(namespace):
    return dict((name[3:].lower(), func)
                for (name, func) in sorted(namespace.iteritems())
                if name.startswith("BM_"))

BENCH_FUNCS = _FindAllBenchmarks(globals())

# Benchmark groups. The "default" group is what's run if no -b option is
# specified.
# If you update the default group, be sure to update the module docstring, too.
# An "all" group which includes every benchmark perf.py knows about is generated
# automatically.
BENCH_GROUPS = {"default": ["2to3", "django", "nbody", "slowspitfire",
                            "slowpickle", "slowunpickle", "spambayes"],
                "startup": ["normal_startup", "startup_nosite"],
                "regex": ["regex_v8", "regex_effbot", "regex_compile"],
                "threading": ["threaded_count", "iterative_count"],
                "cpickle": ["pickle", "unpickle"],
                "micro": ["unpack_sequence", "call_simple"],
                "app": [#"2to3",
    "html5lib", "spambayes"]
               }


def _ExpandBenchmarkName(bm_name, bench_groups):
    """Recursively expand name benchmark names.

    Args:
        bm_name: string naming a benchmark or benchmark group.

    Yields:
        Names of actual benchmarks, with all group names fully expanded.
    """
    expansion = bench_groups.get(bm_name)
    if expansion:
        for name in expansion:
            for name in _ExpandBenchmarkName(name, bench_groups):
                yield name
    else:
        yield bm_name


def ParseBenchmarksOption(benchmarks_opt, bench_groups):
    """Parses and verifies the --benchmarks option.

    Args:
        benchmarks_opt: the string passed to the -b option on the command line.

    Returns:
        A set() of the names of the benchmarks to run.
    """
    legal_benchmarks = bench_groups["all"]
    benchmarks = benchmarks_opt.split(",")
    positive_benchmarks = set(
        bm.lower() for bm in benchmarks if bm and bm[0] != "-")
    negative_benchmarks = set(
        bm[1:].lower() for bm in benchmarks if bm and bm[0] == "-")

    should_run = set()
    if not positive_benchmarks:
        should_run = set(_ExpandBenchmarkName("default", bench_groups))

    for name in positive_benchmarks:
        for bm in _ExpandBenchmarkName(name, bench_groups):
            if bm not in legal_benchmarks:
                logging.warning("No benchmark named %s", bm)
            else:
                should_run.add(bm)
    for bm in negative_benchmarks:
        if bm in bench_groups:
            raise ValueError("Negative groups not supported: -%s" % bm)
        elif bm not in legal_benchmarks:
            logging.warning("No benchmark named %s", bm)
        else:
            should_run.remove(bm)
    return should_run

def ParseEnvVars(option, opt_str, value, parser):
    """Parser callback to --inherit_env var names"""
    parser.values.inherit_env = [v for v in value.split(",") if v]

def main(argv, bench_funcs=BENCH_FUNCS, bench_groups=BENCH_GROUPS):
    bench_groups = bench_groups.copy()
    all_benchmarks = bench_funcs.keys()
    bench_groups["all"] = all_benchmarks

    parser = optparse.OptionParser(
        usage="%prog [options] baseline_python changed_python",
        description=("Compares the performance of baseline_python with" +
                     " changed_python and prints a report."))
    parser.add_option("-r", "--rigorous", action="store_true",
                      help=("Spend longer running tests to get more" +
                            " accurate results"))
    parser.add_option("-f", "--fast", action="store_true",
                      help="Get rough answers quickly")
    parser.add_option("-v", "--verbose", action="store_true",
                      help="Print more output")
    parser.add_option("-m", "--track_memory", action="store_true",
                      help="Track memory usage. This only works on Linux.")
    parser.add_option("-a", "--args", default="",
                      help=("Pass extra arguments to the python binaries."
                            " If there is a comma in this option's value, the"
                            " arguments before the comma (interpreted as a"
                            " space-separated list) are passed to the baseline"
                            " python, and the arguments after are passed to the"
                            " changed python. If there's no comma, the same"
                            " options are passed to both."))
    parser.add_option("-b", "--benchmarks", metavar="BM_LIST", default="",
                      help=("Comma-separated list of benchmarks to run.  Can" +
                            " contain both positive and negative arguments:" +
                            "  --benchmarks=run_this,also_this,-not_this.  If" +
                            " there are no positive arguments, we'll run all" +
                            " benchmarks except the negative arguments. " +
                            " Otherwise we run only the positive arguments. " +
                            " Valid benchmarks are: " +
                            ", ".join(bench_groups.keys() + all_benchmarks)))
    parser.add_option("--inherit_env", metavar="ENVVARS", type="string", action="callback",
                      callback=ParseEnvVars, default=[],
                      help=("Comma-separated list of environment variable names"
                            " that are inherited from the parent environment"
                            " when running benchmarking subprocesses."))
    parser.add_option("--no_charts", default=False, action="store_true",
                      help=("Don't use google charts for displaying the"
                            " graph outcome"))
    parser.add_option("--no_statistics", default=False, action="store_true",
                      help=("Don't perform statistics - return raw data"))

    options, args = parser.parse_args(argv)
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    base, = args
    options.base_binary = base

    base_args = options.args
    if base_args:
        base_cmd_prefix = [base] + base_args.split(" ")
    else:
        base_cmd_prefix = [base]

    logging.basicConfig(level=logging.INFO)

    if options.track_memory:
        if CanGetMemoryUsage():
            info("Suppressing performance data due to --track_memory")
        else:
            # TODO(collinwinter): make this work on other platforms.
            parser.error("--track_memory requires Windows with PyWin32 or " +
                         "Linux 2.6.16 or above")

    should_run = ParseBenchmarksOption(options.benchmarks, bench_groups)

    results = []
    for name in sorted(should_run):
        func = bench_funcs[name]
        print "Running %s..." % name
        # PyPy specific modification: let the func to return a list of results
        # for sub-benchmarks
        bench_result = func(base_cmd_prefix, options)
        name = getattr(func, 'benchmark_name', name)
        if isinstance(bench_result, list):
            for subname, subresult in bench_result:
                fullname = '%s_%s' % (name, subname)
                results.append((fullname, subresult))
        else:
            results.append((name, bench_result))

    print
    print "Report on %s" % " ".join(platform.uname())
    if multiprocessing:
        print "Total CPU cores:", multiprocessing.cpu_count()
    for name, result in results:
        print
        print "###", name, "###"
        print result.string_representation()
    return results

if __name__ == "__main__":
    main(sys.argv[1:])
