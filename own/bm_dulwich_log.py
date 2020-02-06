
import optparse
import util, os

import dulwich.repo

def test_dulwich(n):
    l = []
    r = dulwich.repo.Repo(os.path.join(os.path.dirname(__file__), 'git-demo'))
    import time
    for i in range(20):
        t0 = time.time()
        [e.commit for e in r.get_walker(r.head())]
        l.append(time.time() - t0)
    return l

if __name__ == "__main__":
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Test the performance of Dulwich (git replacement)."))
    util.add_standard_options_to(parser)
    (options, args) = parser.parse_args()

    util.run_benchmark(options, options.num_runs, test_dulwich)
