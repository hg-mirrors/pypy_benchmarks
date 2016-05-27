# From http://www.reddit.com/r/tinycode/comments/169ri9/ray_tracer_in_140_sloc_of_python_with_picture/
# Date: 14.03.2013

from math import sqrt, pi
from common.abstract_threading import (
    atomic, Future, set_thread_pool, ThreadPool,
    print_abort_info, hint_commit_soon)
import time

#import platform
#if platform.python_implementation() == "Jython":
#    # be fair to jython and don't use a lock where none is required:
#    class fakeatomic:
#        def __enter__(self):
#            pass
#        def __exit__(self,*args):
#            pass
#    atomic = fakeatomic()


AMBIENT = 0.1

class Vector(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, b):
        return self.x*b.x + self.y*b.y + self.z*b.z

    def cross(self, b):
        return (self.y*b.z-self.z*b.y, self.z*b.x-self.x*b.z, self.x*b.y-self.y*b.x)

    def magnitude(self):
        return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)

    def normal(self):
        mag = self.magnitude()
        return Vector(self.x/mag,self.y/mag,self.z/mag)

    def __add__(self, b):
        return Vector(self.x + b.x, self.y+b.y, self.z+b.z)

    def __sub__(self, b):
        return Vector(self.x-b.x, self.y-b.y, self.z-b.z)

    def __mul__(self, b):
        #assert type(b) == float or type(b) == int
        return Vector(self.x*b, self.y*b, self.z*b)


class Sphere(object):
    def __init__(self, center, radius, color):
        self.c = center
        self.r = radius
        self.col = color

    def intersection(self, l):
        q = l.d.dot(l.o - self.c)**2 - (l.o - self.c).dot(l.o - self.c) + self.r**2
        if q < 0:
            return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
        else:
            d = -l.d.dot(l.o - self.c)
            d1 = d - sqrt(q)
            d2 = d + sqrt(q)
            if 0 < d1 and ( d1 < d2 or d2 < 0):
                return Intersection(l.o+l.d*d1, d1, self.normal(l.o+l.d*d1), self)
            elif 0 < d2 and ( d2 < d1 or d1 < 0):
                return Intersection(l.o+l.d*d2, d2, self.normal(l.o+l.d*d2), self)
            else:
                return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)

    def normal(self, b):
        return (b - self.c).normal()


class Plane(object):
    def __init__(self, point, normal, color):
        self.n = normal
        self.p = point
        self.col = color

    def intersection(self, l):
        d = l.d.dot(self.n)
        if d == 0:
            return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
        else:
            d = (self.p - l.o).dot(self.n) / d
            return Intersection(l.o+l.d*d, d, self.n, self)


class Ray(object):
    def __init__(self, origin, direction):
        self.o = origin
        self.d = direction


class Intersection(object):
    def __init__(self, point, distance, normal, obj):
        self.p = point
        self.d = distance
        self.n = normal
        self.obj = obj


def testRay(ray, objects, ignore=None):
    intersect = Intersection( Vector(0,0,0), -1, Vector(0,0,0), None)

    for obj in objects:
        if obj is not ignore:
            currentIntersect = obj.intersection(ray)
            if currentIntersect.d > 0 and intersect.d < 0:
                intersect = currentIntersect
            elif 0 < currentIntersect.d < intersect.d:
                intersect = currentIntersect
    return intersect


def trace(ray, objects, light, maxRecur):
    if maxRecur < 0:
        return (0,0,0)
    intersect = testRay(ray, objects)
    if intersect.d == -1:
        col = Vector(AMBIENT,AMBIENT,AMBIENT)
    elif intersect.n.dot(light - intersect.p) < 0:
        col = intersect.obj.col * AMBIENT
    else:
        lightRay = Ray(intersect.p, (light-intersect.p).normal())
        if testRay(lightRay, objects, intersect.obj).d == -1:
            lightIntensity = 1000.0/(4*pi*(light-intersect.p).magnitude()**2)
            col = intersect.obj.col * max(intersect.n.normal().dot((light - intersect.p).normal()*lightIntensity), AMBIENT)
        else:
            col = intersect.obj.col * AMBIENT
    return col



def task(line, x, h, cameraPos, objs, lightSource):
    for y in range(h):
        with atomic:
            ray = Ray(cameraPos,
                      (Vector(x/50.0-5,y/50.0-5,0)-cameraPos).normal())
            col = trace(ray, objs, lightSource, 10)
            line[y] = (col.x + col.y + col.z) / 3.0
        #print_abort_info(0.00001)
    return x


futures = []
def future_dispatcher(ths, *args):
    futures.append(Future(task, *args))



def run(ths=8, w=1024, h=1024):
    ths = int(ths)
    w = int(w)
    h = int(h)

    set_thread_pool(ThreadPool(ths))
    objs = []
    objs.append(Sphere( Vector(-2,0,-10), 2, Vector(0,255,0)))
    objs.append(Sphere( Vector(2,0,-10), 3.5, Vector(255,0,0)))
    objs.append(Sphere( Vector(0,-4,-10), 3, Vector(0,0,255)))
    objs.append(Plane( Vector(0,0,-12), Vector(0,0,1), Vector(255,255,255)))
    lightSource = Vector(0,10,0)

    cameraPos = Vector(0,0,20)
    img = []
    for x in range(w):
        img.append([0.0] * h)
    parallel_time = time.time()
    for x in range(w):
        future_dispatcher(ths, img[x], x, h, cameraPos, objs, lightSource)

    for f in futures:
        f()
    del futures[:]
    parallel_time = time.time() - parallel_time

    # shutdown current pool
    set_thread_pool(None)
    return parallel_time


def main(argv):
    # warmiters threads args...
    warmiters = int(argv[0])
    threads = int(argv[1])
    w, h = int(argv[2]), int(argv[3])

    print "params (iters, threads, w, h):", warmiters, threads, w, h

    print "do warmup:"
    for i in range(5):
        print "iter", i, "time:", run(threads, w, h)

    print "turn off jit"
    import pypyjit, gc
    pypyjit.set_param("off")
    pypyjit.set_param("threshold=999999999,trace_eagerness=99999999")
    print "do", warmiters, "real iters:"
    times = []
    for i in range(warmiters):
        gc.collect()
        times.append(run(threads, w, h))
    print "warmiters:", times

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
