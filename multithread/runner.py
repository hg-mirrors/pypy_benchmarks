#!/usr/bin/env python
""" Usage: runner.py <path to pypy-c> <config file> <result file>
"""

import json
import time
import os, sys
import copy
import pprint
from subprocess import Popen, PIPE


def extract_iter_times(stdout):
    for line in stdout.split('\n'):
        if "warmiters" in line:
            # warmiters: [1.2,3.1,]
            times = line.split(':')[1].strip()[1:-1]
            return [float(t) for t in times.split(',')]
    return None

def run_benchmark(python_exec, bench_config):
    vmstarts = bench_config['vmstarts']
    threads = bench_config['threads']
    print "## run_benchmark", bench_config

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
            print "running:", cmd_str

            try:
                p = Popen(cmd, stdout=PIPE, stderr=PIPE, env=env, cwd=cwd)
                # XXX: process could deadlock if stdout pipe is full -> never terminate -> timeout
                start_time = time.time()
                while p.poll() is None:
                    time.sleep(0.5)
                    if time.time() - start_time > 30 * 60:
                        # kill after 30min
                        p.kill()

                if p.wait() != 0:
                    # error
                    stdout, stderr = p.stdout.read(), p.stderr.read()
                    failure = {
                        'cmd': cmd_str,
                        'exitcode': p.returncode,
                        'stdout': stdout,
                        'stderr': stderr,
                    }
                    failures.append(failure)
                    print "failure:", failure
                else:
                    stdout, stderr = p.stdout.read(), p.stderr.read()
                    print stdout
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
                    print "warmiters:", times['warmiters']
            except Exception as e:
                failures.append({
                    'cmd': cmd_str, 'exception': str(e)})
            except KeyboardInterrupt:
                failures.append({
                    'cmd': cmd_str, 'exception': 'KeyboardInterrupt'})
                return failures, timings
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
    """ Usage: runner.py <path to pypy-c> <config file> <result file> """
    python_exec = argv[0]
    config_file = argv[1]
    result_file = argv[2]

    assert os.path.exists(config_file)
    with open(config_file, 'r') as f:
        config = json.loads(f.read())

    if os.path.exists(result_file):
        with open(result_file, 'r+') as f:
            results = json.loads(f.read())
    else:
        results = {}

    p = Popen([python_exec, "--version"],
              stdout=PIPE, stderr=PIPE)
    _, python_version = p.communicate()
    assert p.returncode == 0
    print python_version

    p = Popen(["hg", "id"], stdout=PIPE, stderr=PIPE)
    hg_id, _ = p.communicate()
    assert p.returncode == 0
    print "id", hg_id

    run_key = time.ctime()
    results[run_key] = {
        'config': config,
        'python': python_exec,
        'python-version': python_version,
        'hg-id': hg_id}

    try:
        run_benchmarks(results[run_key])
        print results[run_key]['results']
    finally:
        with open(result_file, 'w') as f:
            f.write(json.dumps(
                results, sort_keys=True,
                indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main(sys.argv[1:])
    # main(["pypy-c", "config-mersenne.json", "results.json",])
