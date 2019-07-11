#!/usr/bin/env python
""" Usage: runner.py <path to pypy-c> <config file> <result file>
"""

import json
import time
import os, sys
import psutil
import copy
import pprint
from subprocess import Popen, PIPE
import select

STM_LOG = False
WITH_NUMACTL = True
MAX_RETRY = 100  # per bench

def extract_iter_times(stdout):
    for line in stdout.split('\n'):
        if "warmiters" in line:
            # warmiters: [1.2,3.1,]
            times = line.split(':')[1].strip()[1:-1]
            return [float(t) for t in times.split(',')]
    return None

def read_all_so_far(stream, res=''):
    while select.select([stream], [], [], 0.0)[0] != []:
        c = stream.read(1)
        if c == "":  # EOF
            break
        res += c
    return res

def run_benchmark(bench_name, python_exec, bench_config):
    vmstarts = bench_config['vmstarts']
    threads = bench_config['threads']
    print "## run_benchmark", bench_config
    if bench_config['skipvm'] and bench_config['skipvm'] in python_exec:
        print "skip benchmark on VM: skipvm =", bench_config['skipvm']
        return [{'cmd': 'none', 'exception': 'skipvm'}], []

    failures = []
    timings = []
    for ts in threads:
        timeout = False
        vm = 0
        retries = 0
        while vm < vmstarts:
            print "threads: %s, vm: %s" % (ts, vm)
            if timeout:
                print "stop", bench_name, "because of timeout"
                break

            bench_file = os.path.abspath(bench_config['file'])
            cmd = ([python_exec,
                    bench_file,
                    str(bench_config['warmiters']),
                    str(ts)]
                   + bench_config['args'])
            if WITH_NUMACTL:
                # run on node 2, allocate preferrably on node 2
                cmd = ["numactl", "-N1", "--preferred=1"] + cmd
            cmd_str = " ".join(cmd)

            cwd, _ = os.path.split(bench_file)
            cwd = os.path.join(cwd, bench_config['cwd'])
            env = os.environ.copy()
            env['PYTHONPATH'] = bench_config['PYTHONPATH']
            env['JYTHONPATH'] = bench_config['PYTHONPATH']
            env['IRONPYTHONPATH'] = bench_config['PYTHONPATH']
            if STM_LOG:
                env['PYPYSTM'] = "log-%s-%s-%s.pypystm" % (
                    bench_name, ts, vm)
            print "running:", cmd_str

            try:
                p = Popen(cmd, stdout=PIPE, stderr=PIPE, env=env, cwd=cwd)
                start_time = time.time()
                stdout, stderr = "", ""
                mems = []
                while p.poll() is None:
                    time.sleep(0.5)
                    stdout += read_all_so_far(p.stdout)
                    stderr += read_all_so_far(p.stderr)
                    
                    try:
                        process = psutil.Process(p.pid)
                        mem = process.memory_info().rss
                        for child in process.children(recursive=True):
                            mem += child.memory_info().rss
                        mems.append(mem)
                    except psutil.NoSuchProcess as e:
                        print "psutil didn't find the process"
                   
                    if time.time() - start_time > 60 * 60:
                        # kill after 30min
                        print "KILLED AFTER 30min!"
                        timeout = True
                        p.kill()
                        raise Exception("Timeout30min")

                stdout += read_all_so_far(p.stdout)
                stderr += read_all_so_far(p.stderr)

                if p.wait() != 0:
                    # error
                    print stdout
                    print stderr
                    failure = {
                        'cmd': cmd_str,
                        'exitcode': p.returncode,
                        'mems': mems,
                        'stdout': stdout,
                        'stderr': stderr,
                    }
                    failures.append(failure)
                    print "failure:", failure
                    if retries < MAX_RETRY:
                        print "####### FAILURE! RETRYING #######"
                        time.sleep(5)
                        retries += 1
                        continue  # w/o incrementing 'vm'
                else:
                    print stdout
                    iter_times = extract_iter_times(stdout)
                    times = {
                        'cmd': " ".join(cmd),
                        'threads': ts,
                        'vmstarts': vm,
                        'mems': mems,
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
            vm += 1
    return failures, timings


def run_benchmarks(results):
    all_results = results['results'] = {}
    all_config = results['config']
    for bench_key, temp_config in all_config['benchs'].items():
        # load global defaults and overwrite with bench-specific config:
        bench_config = copy.deepcopy(all_config['defaults'])
        bench_config.update(temp_config)

        try:
            failures, timings = run_benchmark(bench_key,
                results['python'], bench_config)
        except Exception as e:
            all_results[bench_key] = {
                'fail_reason': str(e)}
        except KeyboardInterrupt as e:
            all_results[bench_key] = {
                'fail_reason': str(e)}
        else:
            all_results[bench_key] = {
                'failures': failures,
                'timings': timings}

        print bench_key, bench_config
        print "cooldown..."
        time.sleep(20)  # cooldown



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

    p = Popen([python_exec, "-V"],
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
