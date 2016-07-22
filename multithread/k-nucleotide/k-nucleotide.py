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

    t = time.time()
    # ORIGINAL version only looked for 1, 2 sequences
    for nl in 1, 2, 3, 4, 5, 6, 7, 8:
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
