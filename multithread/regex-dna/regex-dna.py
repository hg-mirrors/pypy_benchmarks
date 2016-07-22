# -*- coding: utf-8 -*-

import gc
import sys
import time
from common.abstract_threading import (
    atomic, Future, set_thread_pool, ThreadPool,
    hint_commit_soon, turn_jitting_off)


# Revised BSD license
# This is a specific instance of the Open Source Initiative (OSI) BSD license template.
# Copyright (c) 2004-2008 Brent Fulgham, 2005-2016 Isaac Gouy
# All rights reserved.
# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
# contributed by Dominique Wahli
# 2to3
# mp by Ahmad Syukri
# modified by Justin Peel

from sys import stdin
from re import sub, findall


def var_find(f, seq):
    return len(findall(f, seq))

def main_b():
    with open('regexdna-inputYYY.txt', 'r') as f:
        seq = f.read()
    ilen = len(seq)

    seq = sub('>.*\n|\n', '', seq)
    clen = len(seq)


    variants = (
          'agggtaaa|tttaccct',
          '[cgt]gggtaaa|tttaccc[acg]',
          'a[act]ggtaaa|tttacc[agt]t',
          'ag[act]gtaaa|tttac[agt]ct',
          'agg[act]taaa|ttta[agt]cct',
          'aggg[acg]aaa|ttt[cgt]ccct',
          'agggt[cgt]aa|tt[acg]accct',
          'agggta[cgt]a|t[acg]taccct',
          'agggtaa[cgt]|[acg]ttaccct')

    t = time.time()
    fs = [Future(var_find, v, seq) for v in variants]
    for f in zip(variants, fs):
        print(f[0], f[1]())
    t = time.time() - t

    subst = {
          'B' : '(c|g|t)', 'D' : '(a|g|t)',   'H' : '(a|c|t)', 'K' : '(g|t)',
          'M' : '(a|c)',   'N' : '(a|c|g|t)', 'R' : '(a|g)',   'S' : '(c|g)',
          'V' : '(a|c|g)', 'W' : '(a|t)',     'Y' : '(c|t)'}
    for f, r in list(subst.items()):
        seq = sub(f, r, seq)

    print()
    print(ilen)
    print(clen)
    print(len(seq))
    return t


def run(threads=2):
    threads = int(threads)

    set_thread_pool(ThreadPool(threads))

    t = main_b()

    # shutdown current pool
    set_thread_pool(None)
    return t

def main(argv):
    # warmiters threads args...
    warmiters = int(argv[0])
    threads = int(argv[1])

    print "params (iters, threads):", warmiters, threads

    print "do warmup:"
    for i in range(4):
        t = run(threads)
        print "iter", i, "time:", t

    print "turn off jitting"
    turn_jitting_off()
    print "do", warmiters, "real iters:"
    times = []
    for i in range(warmiters):
        gc.collect()

        t = run(threads)
        times.append(t)
    print "warmiters:", times

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
