# -*- coding: utf-8 -*-
# Based on code from http://code.activestate.com/recipes/576647/
# by Raymond Hettinger
#
# It is a bit problematic because find_solutions spends half
# of the execution time constructing the permutations. Thus
# only half the execution is parallelised.


import sys
import time
from common.abstract_threading import (
    atomic, Future, set_thread_pool, ThreadPool,
    hint_commit_soon, turn_jitting_off)

from itertools import permutations
import itertools


def chunks(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))



def check_solutions(n, cols, perms):
    sols = []
    if 1: #with atomic:
        for vec in perms:
            if n == len(set(vec[i]+i for i in cols)) \
               == len(set(vec[i]-i for i in cols)):
                sols.append(vec)
    return sols


def find_solutions(n):
    solutions = []
    fs = []
    cols = range(n)
    for perms in chunks(permutations(cols), 10000):
        fs.append(Future(check_solutions, n, cols, perms))
    print "Futures:", len(fs)
    for f in fs:
        solutions.extend(f())

    print "found:", len(solutions)


def run(threads=2, n=10):
    threads = int(threads)
    n = int(n)

    set_thread_pool(ThreadPool(threads))

    find_solutions(n)

    # shutdown current pool
    set_thread_pool(None)


def main(argv):
    # warmiters threads args...
    warmiters = int(argv[0])
    threads = int(argv[1])
    n = int(argv[2])

    print "params (iters, threads, n):", warmiters, threads, n

    print "do warmup:"
    for i in range(3):
        t = time.time()
        run(threads, n)
        print "iter", i, "time:", time.time() - t

    print "turn off jitting"
    import gc
    turn_jitting_off()
    print "do", warmiters, "real iters:"
    times = []
    for i in range(warmiters):
        gc.collect()
        t = time.time()
        run(threads, n)
        times.append(time.time() - t)
    print "warmiters:", times

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
