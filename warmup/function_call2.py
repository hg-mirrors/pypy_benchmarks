
import time
l = []

for i in range(200):
    if i % 10 == 0:
        print i
    t0 = time.time()
    exec """

def k(a, b, c):
    pass

def g(a, b, c):
    k(a, b + 1, c + 2)
    k(a, b + 1, c + 2)
    k(a, b + 1, c + 2)
    k(a, b + 1, c + 2)
    k(a, b + 1, c + 2)

def f(i):
    g(i, i + 1, i + 2)
    g(i, i + 1, i + 2)
    g(i, i + 1, i + 2)
    g(i, i + 1, i + 2)
    g(i, i + 1, i + 2)
    g(i, i + 1, i + 2)
for i in range(2000):
    f(i)
"""
    l.append(time.time() - t0)
    #l.append(0)

print l
