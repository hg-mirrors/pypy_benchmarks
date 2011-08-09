#!/usr/bin/env python
""" Usage: runner.py <result filename> <path to pypy-c> <revnumber>
"""

import json
import sys
from unladen_swallow import perf
import benchmarks
import socket

def perform_upload(pypy_c_path, args, force_host, options, res, revision,
                   changed=True, postfix=''):
    from saveresults import save
    project = 'PyPy'
    if "--jit" in args:
        name = "pypy-c" + postfix
    else:
        name = "pypy-c-jit" + postfix
    if "psyco.sh" in pypy_c_path:
        name = "cpython psyco-profile"
        revision = 100
        project = 'cpython'
    if force_host is not None:
        host = force_host
    else:
        host = socket.gethostname()
    print save(project, revision, res, options, name, host, changed=changed)

        
def run_and_store(benchmark_set, result_filename, pypy_c_path, revision=0,
                  options='', branch='default', args='', upload=False,
                  force_host=None, fast=False, baseline=sys.executable,
                  full_store=False, postfix=''):
    funcs = perf.BENCH_FUNCS.copy()
    funcs.update(perf._FindAllBenchmarks(benchmarks.__dict__))
    opts = ['-b', ','.join(benchmark_set), '--inherit_env=PATH',
            '--no_charts']
    if fast:
        opts += ['--fast']
    if args:
        opts += ['--args', args]
    if full_store:
        opts.append('--no_statistics')
    opts += [baseline, pypy_c_path]
    results = perf.main(opts, funcs)
    f = open(str(result_filename), "w")
    res = [(name, result.__class__.__name__, result.__dict__)
           for name, result in results]
    f.write(json.dumps({
        'revision' : revision,
        'results' : res,
        'options' : options,
        'branch'  : branch,
        }))
    f.close()
    if upload:
        if ',' in args:
            argsbase, argschanged = args.split(',')
        else:
            argsbase, argschanged = args, args
        if 'pypy' in baseline:
            perform_upload(pypy_c_path, argsbase, force_host, options, res,
                           revision, changed=False, postfix=postfix)
        perform_upload(pypy_c_path, argschanged, force_host, options, res,
                       revision, changed=True, postfix=postfix)

BENCHMARK_SET = ['richards', 'slowspitfire', 'django', 'spambayes',
                 'rietveld', 'html5lib', 'ai']
BENCHMARK_SET += perf._FindAllBenchmarks(benchmarks.__dict__).keys()

class WrongBenchmark(Exception):
    pass

def main(argv):
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Run benchmarks and dump json")
    parser.add_option("-b", "--benchmarks", metavar="BM_LIST",
                      default=','.join(BENCHMARK_SET),
                      help=("Comma-separated list of benchmarks to run"
                            " Valid benchmarks are: " +
                            ", ".join(BENCHMARK_SET)))
    parser.add_option('-p', '--pypy-c', default=sys.executable,
                      help='pypy-c or other modified python to run against')
    parser.add_option('-r', '--revision', default=0, action="store",
                      help='specify revision of pypy-c')
    parser.add_option('-o', '--output-filename', default="result.json",
                      action="store",
                      help='specify output filename to store resulting json')
    parser.add_option('--options', default='', action='store',
                      help='a string describing picked options, no spaces')
    parser.add_option('--branch', default='default', action='store',
                      help="pypy's branch")
    parser.add_option('--baseline', default=sys.executable, action='store',
                      help='baseline interpreter, defaults to host one')
    parser.add_option("-a", "--args", default="",
                      help=("Pass extra arguments to the python binaries."
                            " If there is a comma in this option's value, the"
                            " arguments before the comma (interpreted as a"
                            " space-separated list) are passed to the baseline"
                            " python, and the arguments after are passed to the"
                            " changed python. If there's no comma, the same"
                            " options are passed to both."))
    parser.add_option("--upload", default=False, action="store_true",
                      help="Upload results to speed.pypy.org")
    parser.add_option("--force-host", default=None, action="store",
                      help="Force the hostname")
    parser.add_option("--fast", default=False, action="store_true",
                      help="Run shorter benchmark runs")
    parser.add_option("--full-store", default=False, action="store_true",
                      help="")
    parser.add_option('--postfix', default='', action='store',
                      help='Append a postfix to uploaded executable')
    options, args = parser.parse_args(argv)
    benchmarks = options.benchmarks.split(',')
    for benchmark in benchmarks:
        if benchmark not in BENCHMARK_SET:
            raise WrongBenchmark(benchmark)
    run_and_store(benchmarks, options.output_filename, options.pypy_c,
                  options.revision, args=options.args, upload=options.upload,
                  force_host=options.force_host, fast=options.fast,
                  baseline=options.baseline, full_store=options.full_store,
                  postfix=options.postfix)

if __name__ == '__main__':
    main(sys.argv[1:])
