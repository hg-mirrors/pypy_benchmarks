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
# http://benchmarksgame.alioth.debian.org/
#
# contributed by Joerg Baumann
# many thanks to Oleg Mazurov for his helpful description

from sys import argv
from math import factorial
from itertools import islice, starmap

def permutations(n, start, size):
    p = bytearray(range(n))
    count = bytearray(n)

    remainder = start
    for v in range(n - 1, 0, -1):
        count[v], remainder = divmod(remainder, factorial(v))
        for _ in range(count[v]):
            p[:v], p[v] = p[1:v + 1], p[0]

    assert(count[1] == 0)
    assert(size < 2 or (size % 2 == 0))

    if size < 2:
        yield p[:]
    else:
        rotation_swaps = [None] * n
        for i in range(1, n):
            r = list(range(n))
            for v in range(1, i + 1):
                r[:v], r[v] = r[1:v + 1], r[0]
            swaps = []
            for dst, src in enumerate(r):
                if dst != src:
                    swaps.append((dst, src))
            rotation_swaps[i] = tuple(swaps)

        while True:
            yield p[:]
            p[0], p[1] = p[1], p[0]
            yield p[:]
            i = 2
            while count[i] >= i:
                count[i] = 0
                i += 1
            else:
                count[i] += 1
                t = p[:]
                for dst, src in rotation_swaps[i]:
                    p[dst] = t[src]

def alternating_flips_generator(n, start, size):
    maximum_flips = 0
    alternating_factor = 1
    for permutation in islice(permutations(n, start, size), size):
        first = permutation[0]
        if first:
            flips_count = 1
            while True:
                permutation[:first + 1] = permutation[first::-1]
                first = permutation[0]
                if not first: break
                flips_count += 1
            if maximum_flips < flips_count:
                maximum_flips = flips_count
            yield flips_count * alternating_factor
        else:
            yield 0
        alternating_factor = -alternating_factor
    yield maximum_flips

def task(n, start, size):
    alternating_flips = alternating_flips_generator(n, start, size)
    return sum(islice(alternating_flips, size)), next(alternating_flips)

def fannkuch(n):
    assert(n > 0)

    task_count = 16
    total = factorial(n)
    task_size = (total + task_count - 1) // task_count

    if task_size < 20000:
        task_size = total
        task_count = 1

    assert(task_size % 2 == 0)

    task_args = [(n, i * task_size, task_size) for i in range(task_count)]

    t = time.time()
    fs = []
    for args in task_args:
        fs.append(Future(task, *args))
    checksums, maximums = zip(*[f() for f in fs])
    # with Pool() as pool:
    #     checksums, maximums = zip(*pool.starmap(task, task_args))

    checksum, maximum = sum(checksums), max(maximums)
    t = time.time() - t
    print("{0}\nPfannkuchen({1}) = {2}".format(checksum, n, maximum))
    return t


def run(threads=2, n=9):
    threads = int(threads)
    n = int(n)

    set_thread_pool(ThreadPool(threads))

    t = fannkuch(n)

    # shutdown current pool
    set_thread_pool(None)
    return t

def main(argv):
    # warmiters threads args...
    warmiters = int(argv[0])
    threads = int(argv[1])
    n = int(argv[2])

    print "params (iters, threads, n):", warmiters, threads, n

    print "do warmup:"
    for i in range(4):
        t = run(threads, n)
        print "iter", i, "time:", t

    print "turn off jitting"
    turn_jitting_off()
    print "do", warmiters, "real iters:"
    times = []
    for i in range(warmiters):
        gc.collect()

        t = run(threads, n)
        times.append(t)
    print "warmiters:", times

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
