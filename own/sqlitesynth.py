import sqlite3
import math

# the goal of the benchmark is to test CFFI performance and going back and
# forth between SQLite and Python a lot. Therefore the queries themselves are
# really simple

class AvgLength(object):
    def __init__(self):
        self.sum = 0
        self.count = 0

    def step(self, x):
        if x is not None:
            self.count += 1
            self.sum += len(x)

    def finalize(self):
        return self.sum / float(self.count)

def _main():
    conn = sqlite3.connect(":memory:")
    conn.execute('create table cos (x, y, z);')
    for i in range(300000):
        conn.execute('insert into cos values (?, ?, ?)', [i, math.cos(i), str(i)])
    conn.create_function("cos", 1, math.cos)
    for x, cosx1, cosx2 in conn.execute("select x, cos(x), y from cos"):
        assert math.cos(x) == cosx1 == cosx2

    conn.create_aggregate("avglength", 1, AvgLength)
    avglen, = conn.execute("select avglength(z) from cos;").next()
    conn.execute("delete from cos;")
    conn.close()



def main(n):
    import time
    times = []
    for i in range(6):
        _main() # warmup
    for i in range(n):
        t1 = time.time()
        _main()
        t2 = time.time()
        times.append(t2 - t1)
    return times

if __name__ == "__main__":
    import util, optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Test the performance of the SqliteSynth benchmark")
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, main)

