import sys, os, cStringIO
import time
import util, optparse

pardir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
pypypath = os.path.join(pardir, 'lib', 'pypy')
sys.path.insert(0, pypypath)

from pypy.tool.pytest.objspace import gettestobjspace

def bench(space):
    w_l = space.appexec([], """():
        class A(object):
            def __init__(self, x):
                self.x = x
        glob_a = A(1)
        l = []
        a, b = 1, 1
        for i in range(100):
            l.append((i, a, str(i), float(i), {i: a}, A(b), glob_a.x))
            a, b = b, a + b
        return l
    """)

def main(n):
    l = []
    space = gettestobjspace()
    # warmup
    bench(space)
    bench(space)
    for i in range(n):
        t0 = time.time()
        bench(space)
        time_elapsed = time.time() - t0
        l.append(time_elapsed)
    return l

if __name__ == "__main__":
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Test the performance of the pypy-interp benchmark")
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, main)
