#!/usr/bin/python

import os
import sys
import json
import numpy as np

def collect_warmiters(all_res, run_key):
    # group timings by thread (multiple vmstarts)
    res_over_run = all_res[run_key]
    grouped = {}
    for bench_key, timings in res_over_run.items():
        for t in timings:
            per_bench = grouped.setdefault(bench_key, {})
            per_bench.setdefault(t['threads'], []).extend(t['warmiters'])

    return grouped

def retrieve_data(results):
    print "RUNS:", len(results)
    all_res = {}
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
        # print ""
        # print "RESULTS OF RUN:"
        all_res[run_key] = res_over_run
        # grouped = collect_warmiters(all_res, run_key)
        # for b, per_bench in grouped.items():
        #     print "BENCH", b
        #     for ts in sorted(per_bench.keys()):
        #         if per_bench[ts]:
        #             print "TS:", ts, "times:", per_bench[ts]
        print ""
        print ""
    return all_res


def print_csv(all_res, run_key):
    import numpy as np

    grouped = collect_warmiters(all_res, run_key)
    cols = len(grouped) * 2 + 1 # "threads" + avg, stddev for each benchmark
    rows = len(grouped.values()[0]) + 1 # name + threads
    table = [["" for _ in range(cols)] for _ in range(rows)] # t[row][col]

    table[0][0] = "Threads"
    for bench_num, (b, per_bench) in enumerate(grouped.items()):
        print "BENCH", b
        table[0][1 + bench_num * 2] = b
        ts_index = 0
        for ts in sorted(per_bench.keys()):
            if per_bench[ts]:
                row = 1 + ts_index
                if table[row][0] == "":
                    table[row][0] = ts
                else:
                    assert table[row][0] == ts

                print "TS:", ts, "times:", per_bench[ts]
                col = 1 + bench_num * 2
                table[row][col] = np.mean(per_bench[ts])
                table[row][col+1] = np.std(per_bench[ts])
                ts_index += 1

    # print table:
    for r in range(rows):
        line = ",\t".join(map(str, table[r]))
        print line

def print_latex_table(all_res, gil_run_key, stm_run_key):
    print ""
    print r"\footnotesize"
    print r"\begin{tabularx}{\textwidth}{l|r@{\hspace{5pt}}r@{\hspace{5pt}}r@{\hspace{5pt}}r|r@{\hspace{5pt}}r@{\hspace{5pt}}r@{\hspace{5pt}}r|r}"
    #print r"\hline"
    print r"\textbf{Python VM} & \multicolumn{4}{c|}{\textbf{PyPy-GIL}} & \multicolumn{4}{c}{\textbf{PyPy-STM}} & \multicolumn{1}{|p{2cm}}{\textbf{Max. speedup}} \\ \hline"
    print r"\textbf{Threads} & \multicolumn{1}{c}{\textbf{1}} & \multicolumn{1}{c}{\textbf{2}} & \multicolumn{1}{c}{\textbf{4}} & \multicolumn{1}{c|}{\textbf{8}} & \multicolumn{1}{c}{\textbf{1}} & \multicolumn{1}{c}{\textbf{2}} & \multicolumn{1}{c}{\textbf{4}} & \multicolumn{1}{c}{\textbf{8}} & \multicolumn{1}{|c}{*} \\ \hline"

    gil_grouped = collect_warmiters(all_res, gil_run_key)
    stm_grouped = collect_warmiters(all_res, stm_run_key)

    assert stm_grouped.keys() == gil_grouped.keys()
    warnings = ""
    lines = 1
    for bench_key in stm_grouped.keys():
        elems = []
        gil_bench = gil_grouped[bench_key]
        stm_bench = stm_grouped[bench_key]
        threads = [1, 2, 4, 8]
        min_gil, min_stm = 9999999., 9999999.
        for vm_bench in [gil_bench, stm_bench]:
            for ts in threads:
                samples = vm_bench[ts]
                if len(samples) < 30:
                    warnings += "WARNING, %s had only %s samples\n" % (bench_key, len(samples))
                mean, std = np.mean(samples), np.std(samples)
                if vm_bench is gil_bench:
                    if mean < min_gil:
                        min_gil = mean
                else:
                    if mean < min_stm:
                        min_stm = mean
                elems.append((mean, std))

        cells = []
        min_mean = min(min_gil, min_stm)
        for e in elems:
            if e[0] == min_gil or e[0] == min_stm:
                s = r"$\mathbf{%.2f}$ \tiny $\pm %.1f$ \footnotesize" % e
            else:
                s = r"$%.2f$ \tiny $\pm %.1f$ \footnotesize" % e
            cells.append(s)
        #
        speedup = min_gil / min_stm
        cells.append(r"\multicolumn{1}{c}{$%.2f\times$}" % speedup)
        print r"%s & " % bench_key + " & ".join(cells) + r" \\" + (
            r" \hdashline[0.5pt/5pt]{}" if lines % 3 == 0 else "")
        lines += 1
    print r"\hline"
    print r"\end{tabularx}"
    print r"\normalsize"
    print ""
    print warnings

def main(argv):
    results_file = argv[0]
    assert os.path.exists(results_file)

    with open(results_file, 'r') as f:
        results = json.loads(f.read())

    all_res = retrieve_data(results)
    while True:
        print "select gil and stm run (e.g., 0,1):"
        runs = all_res.keys()
        choices = ["%s: %s (%s)" % (i, r, results[r]['python'])
                   for i, r in enumerate(runs)]
        print "\n".join(choices)
        choice = raw_input()

        gil_run_key, stm_run_key = [runs[int(c)] for c in choice.split(',')]
        print_csv(all_res, gil_run_key)
        print_latex_table(all_res, gil_run_key, stm_run_key)


if __name__ == '__main__':
    main(sys.argv[1:])
