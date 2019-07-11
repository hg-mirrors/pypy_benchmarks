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
# submitted by Ian Osgood
# modified by Sokolov Yura
# modified by bearophile
# modified by jacek2v: few changes in algorytm, added multiprocessing, used str.count (nucleo newer overlapping)

from collections import defaultdict

def gen_freq(seq, frame):
    frequences = defaultdict(int)
    ns = len(seq) + 1 - frame
    for ii in range(ns):
        frequences[seq[ii:ii + frame]] += 1
    return ns, frequences

def sort_seq(seq, length):
    n, frequences = gen_freq(seq, length)
    #l = sorted(frequences.items(), reverse=True, key=lambda (seq,freq): (freq,seq))
    l = sorted(list(frequences.items()), reverse=True, key=lambda seq_freq: (seq_freq[1],seq_freq[0]))
    return [(st, 100.0*fr/n) for st, fr in l]

def find_seq(seq, nucleo):
    count = seq.count(nucleo)
    return nucleo, count

def load():
    with open('knucleotide-inputYYY.txt', 'r') as infile:
        for line in infile:
            if line[0:3] == ">TH":
                break
        seq = []
        for line in infile:
            if line[0] in ">;":
                break
            seq.append( line[:-1] )
        return seq

def main_b():
    # ORIGINAL version looked only for these:
    #     nucleos = "GGT GGTA GGTATT GGTATTTTAATT GGTATTTTAATTTATAGT"
    nucleos = "GGT AGT GGTA AGGA GGTATT TTGAT GGTATTTTAATT GGATTATGAAAT GGTATTTTAATTTATAGT"
    sequence = "".join(load()).upper()
    plres = []

    # to increase benchmark time without changing input size, repeat the nuclei to 
    # look for
    nucleos = nucleos * 10

    t = time.time()
    # ORIGINAL version only looked for 1, 2 sequences
    for nl in range(1, 20):
        plres.append(Future(sort_seq, sequence, nl))

    for se in nucleos.split():
        plres.append(Future(find_seq, sequence, se))

    [p() for p in plres]
    t = time.time() - t

    # for ii in 0, 1, 2, 3, 4, 5, 6, 7:
    #     print('\n'.join("%s %.3f" % (st, fr) for st,fr in plres[ii]()))
    #     print('')
    # for ii in range(8, len(nucleos.split()) + 8):
    #     print("%d\t%s" % (plres[ii]()[1], plres[ii]()[0]))
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
