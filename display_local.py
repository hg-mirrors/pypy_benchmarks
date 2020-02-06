#!/usr/bin/env python
"""Usage:

    display_local.py  first-filename  [second-filename]

Displays the content of the file resulting from 'run_local.py'.  With
two arguments, computes statistics and displays the differences.

(Details: each file must result from a '--full-store' execution of
'runner.py'.  The "base_times" keys are used and the "changed_times"
keys are discarded.  The option '--changed1' and/or '--changed2' can be
used to pick the "changed_times" instead in the first/second file.
These options are not useful if the files are produced by 'run_local.py'
because it uses nullpython as the changed interpreter.)
"""

import sys
import json
import math
from unladen_swallow import perf


def load_times(filename, base_times=False):
    with open(filename) as f:
        d = json.load(f)

    if base_times:
        key_times = "base_times"
    else:
        key_times = "changed_times"

    result = {}
    for lst2 in d['results']:
        name = str(lst2[0])
        if lst2[1] != 'RawResult':
            print ("ERROR: entry for %r is not a RawResult "
                   "(missing --full-store?)" % (name,))
            continue
        result[name] = lst2[2][key_times]
    if not result:
        print "No valid result in %r." % (filename,)
        sys.exit(1)
    return result


def _report(row, raw1):
    if raw1 is None:
        row.append('')
        row.append('')
        row.append('')
        row.append('')
        row.append('')
    elif len(raw1) == 1:
        # A single result.  Report it.
        row.append('')
        row.append('')
        row.append(str(round(raw1[0], 3)))
        row.append('')
        row.append('')
    elif len(raw1) == 0:
        # Should not occur
        row.append('???')
        row.append('')
        row.append('empty')
        row.append('')
        row.append('???')
    else:
        # Multiple results.
        t_min = min(raw1)
        t_avg = perf.avg(raw1)
        t_std = perf.SampleStdDev(raw1)
        row.append(str(round(t_min, 3)))
        row.append('')
        row.append(str(round(t_avg, 3)))
        row.append('')
        row.append(str(round(t_std, 5)))
    row.append('')
    return raw1

def geometric_average(lst):
    return math.exp(sum(math.log(t) for t in lst) / len(lst))

def display(times1, times2=None):
    if times2 is None:
        times2 = {}
    all_names = sorted(set(times1) | set(times2))
    table = [[],
             ['BENCHMARK', '   ', 'min', ' ', 'avg', ' ', 'stddev', '  ',
              'min', ' ', 'avg', ' ', 'stddev', '  ',
              'diff']]
    RIGHT_ALIGN = '\x00'

    l_avg1 = []
    l_avg2 = []
    l_diff = []
    for name in all_names:
        row = [name, '']
        table.append(row)
        raw1 = _report(row, times1.get(name))
        raw2 = _report(row, times2.get(name))
        if raw1 and raw2:
            t_avg1 = perf.avg(raw1)
            t_avg2 = perf.avg(raw2)
            row.append(perf.TimeDelta(t_avg1, t_avg2))
            l_avg1.append(t_avg1)
            l_avg2.append(t_avg2)
            l_diff.append(t_avg1 / t_avg2)

    table.append([])
    if len(l_avg1) == len(all_names):
        g_avg1 = geometric_average(l_avg1)
        g_avg2 = geometric_average(l_avg2)
        row = ['GEOM AVG', '',
               '', '', str(round(g_avg1, 3)), '', '', '',
               '', '', str(round(g_avg2, 3)), '', '', '',
               perf.TimeDelta(g_avg1, g_avg2)]
        table.append(row)
        if len(l_avg1) > 3:
            l_avg = zip(l_diff, l_avg1, l_avg2)
            l_avg.sort()
            del l_avg[0]
            del l_avg[-1]
            g_avg1 = geometric_average([y for x,y,z in l_avg])
            g_avg2 = geometric_average([z for x,y,z in l_avg])
            row = ['without 1st/last', '',
                   '', '', str(round(g_avg1, 3)), '', '', '',
                   '', '', str(round(g_avg2, 3)), '', '', '',
                   perf.TimeDelta(g_avg1, g_avg2)]
        table.append(row)
        table.append([])

    lengths = []
    for row in table:
        while len(lengths) < len(row):
            lengths.append(0)
        for i, cell in enumerate(row):
            if len(cell) > lengths[i]:
                lengths[i] = len(cell)
    for row in table:
        s = ''
        for cell, l1 in zip(row, lengths):
            if cell.startswith(RIGHT_ALIGN):
                cell = ' '*(l1 - len(cell) - 1) + cell[1:]
            s += cell + ' '*(l1 - len(cell))
        print s


def main(argv):
    import optparse
    parser = optparse.OptionParser(
        usage="%prog first-filename [second-filename]",
        description=__doc__)

    parser.add_option("--changed1", default=False, action="store_true",
        help='Pick the "changed_times" keys instead of the "base_times"'
             ' keys in the first file')
    parser.add_option("--changed2", default=False, action="store_true",
        help='Pick the "changed_times" keys instead of the "base_times"'
             ' keys in the second file')
    options, args = parser.parse_args(argv)

    if len(args) == 0:
        parser.error("no filenames given; try --help")
    elif len(args) > 2:
        parser.error("too many filenames")

    times1 = load_times(args[0], base_times=not options.changed1)
    if len(args) > 1:
        times2 = load_times(args[1], base_times=not options.changed2)
    else:
        times2 = None
    display(times1, times2)


if __name__ == '__main__':
    main(sys.argv[1:])
