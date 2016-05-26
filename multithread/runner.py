#!/usr/bin/env python
""" Usage: runner.py <result file> <path to pypy-c>
"""

config = {
    "defaults": {
        # global defaults:
        "file": None,
        "threads": [1, 2, 4, 8,],
        "vmstarts": 3,
        "warmiters": 5,
        "args": [],
        "cwd": ".", # relative to file
        "PYTHONPATH": ".",
    },

    "benchs": {
        # list of benchmarks:
        "raytrace": {
            "file": "raytrace/raytrace.py",
            "PYTHONPATH": "..",
            "vmstarts": 5,
            "warmiters": 5,
            "args": ["1024", "1024"] # w, h
        },
    },
}


import json
import time
import os, sys
import copy
import pprint
from subprocess import Popen, PIPE


def run_benchmark(python_exec, bench_config):
    vmstarts = bench_config['vmstarts']
    threads = bench_config['threads']
    print "## run_benchmark", bench_config['file']

    failures = []
    timings = []
    for ts in threads:
        for vm in range(vmstarts):
            print "threads: %s, vm: %s" % (ts, vm)

            bench_file = os.path.abspath(bench_config['file'])
            cmd = ([python_exec,
                    bench_file,
                    str(bench_config['warmiters']),
                    str(ts)]
                   + bench_config['args'])
            cmd_str = " ".join(cmd)

            cwd, _ = os.path.split(bench_file)
            cwd = os.path.join(cwd, bench_config['cwd'])
            env = os.environ.copy()
            env['PYTHONPATH'] = bench_config['PYTHONPATH']
            print "running:", cmd_str, "in", cwd, "with PYTHONPATH=", env['PYTHONPATH']

            try:
                print env['PYTHONPATH']
                p = Popen(cmd, stdout=PIPE, stderr=PIPE, env=env, cwd=cwd)
                if p.wait() != 0:
                    # error
                    stdout, stderr = p.stdout.read(), p.stderr.read()
                    failure = {
                        'cmd': cmd_str,
                        'stdout': stdout,
                        'stderr': stderr,
                    }
                    failures.append(failure)
                    print "failure:", failure
                else:
                    stdout, stderr = p.stdout.read(), p.stderr.read()
                    iter_times = extract_iter_times(stdout)
                    times = {
                        'cmd': " ".join(cmd),
                        'threads': ts,
                        'vmstarts': vm,
                        'stdout': stdout,
                        'stderr': stderr,
                        'warmiters': iter_times,
                    }
                    timings.append(times)
                    print "timing:", times
            finally:
                pass
    return failures, timings


def run_benchmarks(results):
    all_results = results['results'] = {}
    all_config = results['config']
    for bench_key, temp_config in all_config['benchs'].items():
        # load global defaults and overwrite with bench-specific config:
        bench_config = copy.deepcopy(all_config['defaults'])
        bench_config.update(temp_config)

        try:
            failures, timings = run_benchmark(
                results['python'], bench_config)
        except Exception as e:
            all_results[bench_key] = {
                'fail_reason': str(e)}
        else:
            all_results[bench_key] = {
                'failures': failures,
                'timings': timings}

        print bench_key, bench_config




def main(argv):
    result_file = argv[0]
    python_exec = argv[1]

    if os.path.exists(result_file):
        with open(result_file, 'r+') as f:
            results = json.loads(f.read())
    else:
        results = {}

    run_key = time.ctime()
    results[run_key] = {'config': config,
                        'python': python_exec}
    try:
        run_benchmarks(results[run_key])
        print results[run_key]['results']
    finally:
        with open(result_file, 'w') as f:
            f.write(json.dumps(
                results, sort_keys=True,
                indent=4, separators=(',', ': ')))


if __name__ != '__main__': #FIXME: emacs bug?
    main(sys.argv[1:])
else:
    main(["results.json", "/usr/bin/python"])
