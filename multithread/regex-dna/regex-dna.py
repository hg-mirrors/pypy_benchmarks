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
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright notice, this list
#     of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice, this
#     list of conditions and the following disclaimer in the documentation and/or
#     other materials provided with the distribution.
#   * Neither the name of "The Computer Language Benchmarks Game" nor the name of "The
#     Computer Language Shootout Benchmarks" nor the names of its contributors may be
#     used to endorse or promote products derived from this software without specific
#     prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.


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

def main_b(small=False):
    f = 'regexdna-inputYYY.txt' if not small else 'regexdna-input10000.txt'
    with open(f, 'r') as f:
        seq = f.read().lower()
    ilen = len(seq)

    seq = sub('>.*\n|\n', '', seq)
    clen = len(seq)


    variants = [
          'agggtaaa|tttaccct',
          '[cgt]gggtaaa|tttaccc[acg]',
          'a[act]ggtaaa|tttacc[agt]t',
          'ag[act]gtaaa|tttac[agt]ct',
          'agg[act]taaa|ttta[agt]cct',
          'aggg[acg]aaa|ttt[cgt]ccct',
          'agggt[cgt]aa|tt[acg]accct',
          'agggta[cgt]a|t[acg]taccct',
          'agggtaa[cgt]|[acg]ttaccct']
    # instead of increasing input data, just search for the variants
    # multiple times:
    variants = 40 * variants

    t = time.time()
    fs = [Future(var_find, v, seq) for v in variants]
    for f in zip(variants, fs):
        print(f[1]())
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


def run(threads=2, small=False):
    threads = int(threads)

    set_thread_pool(ThreadPool(threads))

    t = main_b(small)

    # shutdown current pool
    set_thread_pool(None)
    return t

def main(argv):
    # warmiters threads args...
    warmiters = int(argv[0])
    threads = int(argv[1])
    small = len(argv) == 3
        

    print "params (iters, threads):", warmiters, threads

    print "do warmup:"
    for i in range(3):
        t = run(threads, small)
        print "iter", i, "time:", t

    print "turn off jitting"
    turn_jitting_off()
    print "do", warmiters, "real iters:"
    times = []
    for i in range(warmiters):
        gc.collect()

        t = run(threads, small)
        times.append(t)
    print "warmiters:", times

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
