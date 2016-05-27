
from common.abstract_threading import (
    atomic, Future, set_thread_pool, ThreadPool,
    print_abort_info, hint_commit_soon, turn_jitting_off)
import time

from parsible import Parsible



def run(threads):

    set_thread_pool(ThreadPool(threads))

    p = Parsible(input_file="data/nasa-http-log",
                 parser="parse_nginx",
                 pid_file="/tmp/parsible.pid",
                 debug=False, batch=True, auto_reload=False)
    t = time.time()
    p.main(128)
    parallel_time = time.time() - t

    # shutdown current pool
    set_thread_pool(None)
    return parallel_time




def main(argv):
    # warmiters threads args...
    warmiters = int(argv[0])
    threads = int(argv[1])

    print "params (iters, threads):", warmiters, threads

    print "do warmup:"
    for i in range(4):
        print "iter", i, "time:", run(threads)

    print "turn off jitting"
    import gc
    turn_jitting_off()
    print "do", warmiters, "real iters:"
    times = []
    for i in range(warmiters):
        gc.collect()
        times.append(run(threads))
    print "warmiters:", times

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
