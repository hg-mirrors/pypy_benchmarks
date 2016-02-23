
for k in range(100):
    d = locals().copy()
    exec """

class A(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

class B(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

def f(count):
    s = 0
    l_glob = [None]
    for i in range(count):
        a = A(1, 2, 3)
        if i > 1041:
            s += 1
        #if i % 15 == 0:
        #    s += 1
        #if i % 21 == 0:
        #    s += 1
        l = [a, B(2, 3), a]
        l_glob[0] = l[-1]
        s += i
    return s

# 1243 = tracing + blackholing + tracing
# 1241 = tracing + blackholing
# 1041 = tracing
# 1039 = just interpreter
f(1243)
""" in d
