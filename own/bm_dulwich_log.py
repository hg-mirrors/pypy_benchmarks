
import optparse
import util, os

import dulwich.repo

INNER_ITERS = 50

def test_dulwich(n):
    l = []
    r = dulwich.repo.Repo(os.path.join(os.path.dirname(__file__), 'git-demo'))
    import time
    for i in xrange(n):
        t0 = time.time()

        for j in xrange(INNER_ITERS):
            r.revision_history(r.head())

        l.append(time.time() - t0)
    return l

if __name__ == "__main__":
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Test the performance of Dulwich (git replacement)."))
    util.add_standard_options_to(parser)
    (options, args) = parser.parse_args()

    util.run_benchmark(options, options.num_runs, test_dulwich)
