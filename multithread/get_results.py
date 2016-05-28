#!/usr/bin/python

import os
import sys
import json



def main(argv):
    results_file = argv[0]
    assert os.path.exists(results_file)

    with open(results_file, 'r') as f:
        results = json.loads(f.read())

    print "RUNS:", len(results)
    for run_key, run in results.iteritems():
        res_over_run = {}

        print "###", "RUN", run_key, "###"
        print "python:", run['python']
        print "python-version:", run['python-version'].strip()
        print "hg-id:", run['hg-id'].strip()
        run_results = run['results']
        print "RESULTS:", len(run_results)

        print "BENCHMARKS:", run_results.keys()
        for bench_key, bench_res in run_results.items():
            print "BENCHMARK:", bench_key
            if 'fail_reason' in bench_res:
                print "FAILED:", bench_res
            else:
                timings = bench_res['timings']
                failures = bench_res['failures']
                print "timings:", len(timings), "failures:", len(failures)
                res_over_run.setdefault(bench_key, []).extend(timings)
                if failures:
                    print "############# THERE ARE FAILURES! #############"
                    #print "fail reasons:", failures
                    #import pdb;pdb.set_trace()
        print ""
        print "RESULTS OF RUN:"
        for bench_key, timings in res_over_run.items():
            print "BENCH", bench_key
            # group timings by thread (multiple vmstarts)
            threads = results[run_key]['config']['defaults']['threads']
            grouped = [[] for _ in range(max(threads))]
            for t in timings:
                grouped[t['threads'] - 1].extend(t['warmiters'])
            for ts in threads:
                print "TS:", ts, "times:", grouped[ts - 1]
        print ""
        print ""


if __name__ == '__main__':
    main(sys.argv[1:])
