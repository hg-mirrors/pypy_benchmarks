#!/usr/bin/env python
""" Usage: runner.py <result filename> <path to pypy-c> <revnumber>
"""

import json
import socket
import sys
import os
import time

import benchmarks
from saveresults import save
from unladen_swallow import perf

BENCHMARK_SET = ['richards', 'slowspitfire', 'django', 'spambayes',
                 'rietveld', 'html5lib', 'ai']
BENCHMARK_SET += perf._FindAllBenchmarks(benchmarks.__dict__).keys()

class WrongBenchmark(Exception):
    pass

def convert_results(result_list):
    r = []
    for bench, cls, dict, t0 in result_list:
        runs = []
        cur_time = t0
        for t in dict['times']:
            runs.append({"start_timestamp": cur_time, "duration": t})
            cur_time += t
        r.append({"name": bench, "runs": runs, "events": []})
    return r

def run_and_store(benchmark_set, result_filename, path, revision=0,
                  options='', branch='default', args='', upload=False,
                  fast=False, full_store=False, parser_options=None):
    _funcs = perf.BENCH_FUNCS.copy()
    _funcs.update(perf._FindAllBenchmarks(benchmarks.__dict__))
    bench_data = json.load(open('bench-data.json'))
    funcs = {}
    for key, value in _funcs.iteritems():
        funcs[key] = (value, bench_data[key])
    opts = ['-b', ','.join(benchmark_set),
            '--inherit_env=PATH',
            '--no_charts']
    if fast:
        opts += ['--fast']
    if args:
        opts += ['--args', args]
    if full_store:
        opts += ['--no_statistics']
    opts += [path]
    start_time = time.time()
    results = perf.main(opts, funcs)
    end_time = time.time()
    f = open(str(result_filename), "w")
    results = [(name, result.__class__.__name__, result.__dict__, t0)
           for name, result, t0 in results]
    force_host = parser_options.force_host
    f.write(json.dumps({
        'revision': revision,
        'benchmarks': convert_results(results),
        "interpreter": parser_options.interpreter_name or parser_options.python,
        "machine": force_host if force_host else socket.gethostname(),
        "protocol_version_no": "1",
        "start_timestamp": start_time,
        "end_timestamp": end_time,
        'options': options,
        'branch': branch,
        }, indent=4))
    f.close()
    return results

def main(argv):
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Run benchmarks and dump json")

    # benchmark options
    benchmark_group = optparse.OptionGroup(
        parser, 'Benchmark options',
        ('Options affecting the benchmark runs and the resulting output '
         'json file.'))
    benchmark_group.add_option(
        "-b", "--benchmarks", metavar="BM_LIST",
        help=("Comma-separated list of benchmarks to run"
              " Valid benchmarks are: %s"
              ". (default: Run all listed benchmarks)"
              ) % ", ".join(sorted(BENCHMARK_SET)))
    benchmark_group.add_option(
        '-p', '--python', default=sys.executable, action='store',
        help=('Interpreter. (default: the python used to '
              'run this script)'))
    benchmark_group.add_option(
        "-f", "--benchmarks-file", metavar="BM_FILE",
        help=("Read the list of benchmarks to run from this file (one "
              "benchmark name per line).  Do not specify both this and -b."))
    benchmark_group.add_option(
        '-o', '--output-filename', default="result.json",
        action="store",
        help=('Specify the output filename to store resulting json. '
              '(default: result.json)'))
    benchmark_group.add_option(
        '--options', default='', action='store',
        help='A string describing picked options, no spaces.')
    benchmark_group.add_option(
        '--branch', default='default', action='store',
        dest='upload_branch',
        help=("The branch the 'changed' interpreter was compiled from. This "
              'will be store in the result json and used for the upload. '
              "(default: 'default')"))
    benchmark_group.add_option(
        '--force-interpreter-name', default=None, action='store',
        dest='interpreter_name',
        help=("Force the interpreter name present",)
    )
    benchmark_group.add_option(
        '-r', '--revision', action="store",
        dest='upload_revision',
        help=("Specify the revision of the 'changed' interpreter. "
              'This will be store in the '
              'result json and used for the upload. (default: None)'))
    benchmark_group.add_option(
        "-a", "--args", default="",
        help=("Pass extra arguments to the python binaries."
              " If there is a comma in this option's value, the"
              " arguments before the comma (interpreted as a"
              " space-separated list) are passed to the baseline"
              " python, and the arguments after are passed to"
              " the changed python. If there's no comma, the"
              " same options are passed to both."))
    benchmark_group.add_option(
        "--fast", default=False, action="store_true",
        help="Run shorter benchmark runs.")
    benchmark_group.add_option(
        "--full-store", default=False, action="store_true",
        help="Run the benchmarks with the --no-statistics flag.")
    parser.add_option_group(benchmark_group)

    parser.add_option("--upload-url", action="store", default=None,
                      help="Upload to url or None")
    parser.add_option("--upload-revision", action="store", default=None,
                      help="Upload revision")
    parser.add_option("--upload-branch", action="store", default=None,
                      help="Upload branch")
    parser.add_option("--upload-project", action="store", default="PyPy")
    parser.add_option("--upload-executable", action="store", default="pypy-c")
    parser.add_option(
        "--force-host", default=None, action="store",
        help=("Force the hostname."))
    parser.add_option("--niceness", default=None, type="int",
                      help="Set absolute niceness for process")

    options, args = parser.parse_args(argv)

    if options.benchmarks is not None:
        if options.benchmarks_file is not None:
            parser.error(
                '--benchmarks and --benchmarks-file are mutually exclusive')
        else:
            benchmarks = [benchmark.strip()
                          for benchmark in options.benchmarks.split(',')]
    else:
        if options.benchmarks_file is not None:
            benchmarks = []
            try:
                bm_file = open(options.benchmarks_file, 'rt')
            except IOError as e:
                parser.error('error opening benchmarks file: %s' % e)
            with bm_file:
                for line in bm_file:
                    benchmarks.append(line.strip())
        else:
            benchmarks = list(BENCHMARK_SET)

    for benchmark in benchmarks:
        if benchmark not in BENCHMARK_SET and not benchmark.startswith('-'):
            raise WrongBenchmark(benchmark)

    path = options.python
    fast = options.fast
    args = options.args
    full_store = options.full_store
    output_filename = options.output_filename

    branch = options.upload_branch
    revision = options.upload_revision
    force_host = options.force_host

    if options.niceness is not None:
        os.nice(options.niceness - os.nice(0))

    results = run_and_store(benchmarks, output_filename, path,
                            revision, args=args, fast=fast,
                            full_store=full_store, branch=branch,
                            parser_options=options)

    if options.upload_url:
        branch = options.upload_branch or 'default'
        revision = options.upload_revision

        # prevent to upload results from the nullpython dummy
        host = force_host if force_host else socket.gethostname()
        print save(options.upload_project,
                   revision, results, options.upload_executable, host,
                   options.upload_url,
                   branch=branch)


if __name__ == '__main__':
    main(sys.argv[1:])
