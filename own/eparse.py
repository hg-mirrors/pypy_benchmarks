import time
import os
import ometa
ometa.FAST = True
from monte.eparser import EParser

INNER_ITERS = 24

def main(n):
    l = []
    data = open(os.path.join(os.path.dirname(__file__), 'test.e')).read()
    for _ in range(n):
        t0 = time.time()

        for i in xrange(INNER_ITERS):
            p = EParser(data)
            v, e = p.apply('start')

        l.append(time.time() - t0)
    return l

if __name__ == '__main__':
    import util, optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Test the performance of the eparse benchmark")
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, main)
