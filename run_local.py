#!/usr/bin/env python
"""Usage:

    run_local.py path/to/pypy-c -o output-filename <more options for runner.py>

This is a wrapper script around runner.py that makes it easier to run
locally all benchmarks on a single given pypy-c.  It stores the result
in a JSON file given as 'output-filename'.  You can then run
'display_local.py' to display the output or the differences between two
such output files.

More options can be given on the command line and are passed to runner.py.
Common ones are:

    -b BENCHMARK_LIST
    --fast
    --args=ARGS         arguments to give to pypy-c, must not contain a comma!
"""
from __future__ import print_function
import sys, os
import subprocess

if len(sys.argv) < 2 or sys.argv[1].startswith('-'):
    print(__doc__)
    sys.exit(2)

pypy_c = sys.argv[1]

localdir = os.path.dirname(sys.argv[0]) or '.'

# note: we use nullpython.py as the "changed" interpreter, not the
# "baseline" one, because BM_translate() happens to run only with the
# baseline interpreter and not the changed one.  Messy.
cmdline = [sys.executable, os.path.join(localdir, 'runner.py'),
           '--baseline', pypy_c,
           '--changed', os.path.join(localdir, 'nullpython.py'),
           '--full-store',
           ] + sys.argv[1:]
print('')
print('Executing', cmdline)
print('')

r = subprocess.call(cmdline)
if r:
    print('*** exit code %r ***' % (r,), file=sys.stderr)
    sys.exit(r)
