
for i in range(100):
    exec """
def f():
    s = 0
    i = 0
    while i < 10000:
        i += 1
        if i % 2 == 0:
            s += 1
        if i % 3 == 0:
            s += 1
        if i % 5 == 0:
            s += 1
        if i % 7 == 0:
            s += 1
        if i % 11 == 0:
            s += 1
        if i % 13 == 0:
            s += 1
        if i % 17 == 0:
            s += 1
        if i % 19 == 0:
            s += 1
        if i % 23 == 0:
            s += 1

f()
"""
