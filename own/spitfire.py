
import sys
import os
import util
import time
import optparse
if sys.version_info[0] < 3:
    import cStringIO as io
else:
    import io

def relative(*args):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

testdir = relative('..', 'unladen_swallow', 'lib', 'spitfire', 'tests', 'perf')
sys.path.insert(0, testdir)
sys.path.insert(0, relative('..', 'unladen_swallow', 'lib', 'spitfire'))
import bigtable
# bummer, timeit module is stupid
from bigtable import test_python_cstringio, test_spitfire_o3, test_spitfire

def runtest(n, benchmark):
    times = []
    for i in range(n):
        sys.stdout = io.StringIO()
        bigtable.run([benchmark], 100)
        times.append(float(sys.stdout.getvalue().split(" ")[-2]))
        sys.stdout = sys.__stdout__
    return times

if __name__ == '__main__':
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Test the performance of the spitfire benchmark")
    parser.add_option('--benchmark', type="choice",
                      choices=['python_cstringio', 'spitfire_o3'],
                      default="spitfire_o3",
                      help="choose between cstringio and spitfire_o3")
    util.add_standard_options_to(parser)
    options, args = parser.parse_args(sys.argv)
    util.run_benchmark(options, options.num_runs, runtest, options.benchmark)
