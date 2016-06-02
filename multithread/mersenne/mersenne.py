# -*- coding: utf-8 -*-



import sys
import time, random
from common.abstract_threading import (
    atomic, Future, set_thread_pool, ThreadPool,
    turn_jitting_off)

import itertools
from collections import deque


from sys import stdout
from math import sqrt, log


def chunks(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))


def is_prime ( p ):
    if p == 2: return True # Lucas-Lehmer test only works on odd primes
    elif p <= 1 or p % 2 == 0: return False
    else:
        for i in range(3, int(sqrt(p))+1, 2 ):
            if p % i == 0: return False
    return True

def is_mersenne_prime ( p ):
    if p == 2:
        return True
    else:
        m_p = ( 1 << p ) - 1
        s = 4
        for i in range(3, p+1):
            s = (s ** 2 - 2) % m_p
        return s == 0


def work(ps, counter, upb_count):
    if counter[0] >= upb_count:
        return

    for p in ps:
        if 1: #with atomic:
            if is_prime(p) and is_mersenne_prime(p):
                #print p
                with atomic:
                    counter[0] += 1
        if counter[0] >= upb_count:
            break


def run(threads=2, n=2000):
    threads = int(threads)
    n = int(n)

    set_thread_pool(ThreadPool(threads))


    precision = n   # maximum requested number of decimal places of 2 ** MP-1 #
    long_bits_width = precision * log(10, 2)
    upb_prime = int( long_bits_width - 1 ) / 2    # no unsigned #
    upb_count = 45      # find 45 mprimes if int was given enough bits #

    print " Finding Mersenne primes in M[2..%d]:" % upb_prime

    counter = [0]
    fs = []
    cs = list(chunks(xrange(2, upb_prime+1), 100))
    print len(cs), "futures"
    for ps in cs:
        fs.append(Future(work, ps, counter, upb_count))

    [f() for f in fs]
    print "found", counter[0]

    # shutdown current pool
    set_thread_pool(None)

    return


def main(argv):
    # warmiters threads args...
    warmiters = int(argv[0])
    threads = int(argv[1])
    n = int(argv[2])

    print "params (iters, threads, n):", warmiters, threads, n

    print "do warmup:"
    for i in range(2):
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

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
