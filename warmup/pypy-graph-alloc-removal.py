import sys
sys.path.insert(1, '/home/sik/Work/freeSoftware/pypysrc')

from rpython.translator.interactive import Translation
from rpython.translator.translator import graphof
from rpython.translator.backendopt.malloc import LLTypeMallocRemover
from rpython.flowspace.model import copygraph

import time

class X(object):
    pass

def f(n):
    x = X()
    x.attr = n
    y = X()
    y.attr = 6 if n > 100 else 5
    return x.attr + y.attr


t = Translation(f, [int])
t.annotate()
t.rtype()

graph = graphof(t.context, f)

def main(graph, repeat):
    start = time.time()
    l = []
    for i in range(repeat):
        print i
        l.append(f(graph))
    print l
    end = time.time()
    print end - start

def f(graph):
    start = time.time()
    for k in range(10):
        g = copygraph(graph)
        remover = LLTypeMallocRemover()
        remover.remove_mallocs_once(g)
    return time.time() - start

if len(sys.argv) >= 2:
    count = int(sys.argv[1])
else:
    count = 100
main(graph, count)
