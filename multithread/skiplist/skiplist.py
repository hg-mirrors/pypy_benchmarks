
# https://github.com/kunigami/blog-examples/tree/master/2012-09-23-skip-list

from common.abstract_threading import (atomic, Future,
                                       set_thread_pool, ThreadPool,
                                       hint_commit_soon, turn_jitting_off)
import time, threading

import random

thread_local = threading.local()

class SkipNode:
    """A node from a skip list"""
    def __init__(self, height = 0, elem = None):
        self.elem = elem
        self.next = [None]*height

class SkipList:
    def __init__(self):
        self.head = SkipNode()
        self.len = 0
        self.maxHeight = 0

    def __len__(self):
        return self.len

    def find(self, elem, update = None):
        if update == None:
            update = self.updateList(elem)
        if len(update) > 0:
            candidate = update[0].next[0]
            if candidate != None and candidate.elem == elem:
                return candidate
        return None

    def contains(self, elem, update = None):
        return self.find(elem, update) != None

    def randomHeight(self):
        height = 1
        while thread_local.rnd.randint(1, 2) != 1:
            height += 1
        return height

    def updateList(self, elem):
        update = [None] * self.maxHeight
        x = self.head
        for i in reversed(xrange(self.maxHeight)):
            while x.next[i] != None and x.next[i].elem < elem:
                x = x.next[i]
            update[i] = x
        return update

    def insert(self, elem):
        node = SkipNode(self.randomHeight(), elem)

        # conflicts with everything else:
        self.maxHeight = max(self.maxHeight, len(node.next))

        while len(self.head.next) < len(node.next):
            self.head.next.append(None)

        update = self.updateList(elem)
        if self.find(elem, update) == None:
            for i in xrange(len(node.next)):
                node.next[i] = update[i].next[i]
                update[i].next[i] = node
            self.len += 1
        #hint_commit_soon()

    def remove(self, elem):
        update = self.updateList(elem)
        x = self.find(elem, update)
        if x != None:
            # conflicts with everything else:
            for i in reversed(range(len(x.next))):
                update[i].next[i] = x.next[i]
                if self.head.next[i] == None:
                    self.maxHeight -= 1
            self.len -= 1
            #hint_commit_soon()

    def printList(self):
        for i in range(len(self.head.next)-1, -1, -1):
            x = self.head
            while x.next[i] != None:
                print x.next[i].elem,
                x = x.next[i]
            print ''


CONFLICTING = [SkipList.insert, SkipList.remove]
OPS = [SkipList.find] * 1998 + CONFLICTING
ITEM_RANGE = 1000000

def task(id, slist, ops):
    print "start task with %s ops" % ops
    r = random.Random()
    r.seed(id)
    thread_local.rnd = r

    for _ in xrange(ops):
        op = r.choice(OPS)
        elem = r.randint(1, ITEM_RANGE)
        # if op in CONFLICTING:
        #     hint_commit_soon()
        with atomic:
            op(slist, elem)

        #print_abort_info(0.0001)

    print "task ended"


def chunks(l, n):
    """ Yield successive n-sized chunks from l. """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]



def run(threads=2, concurrency=8, operations=2000000):
    threads = int(threads)
    operations = int(operations)

    set_thread_pool(ThreadPool(threads))
    thread_local.rnd = random

    slist = SkipList()
    for _ in xrange(1000):
        slist.insert(random.randint(1, ITEM_RANGE))

    c_len = operations // concurrency
    fs = []
    parallel_time = time.time()
    for i in xrange(concurrency):
        fs.append(Future(task, i, slist, c_len))
    for f in fs:
        f()
    parallel_time = time.time() - parallel_time

    # print "list:"
    # slist.printList()

    # shutdown current pool
    set_thread_pool(None)
    return parallel_time




def main(argv):
    # warmiters threads args...
    warmiters = int(argv[0])
    threads = int(argv[1])
    cs, ops = int(argv[2]), int(argv[3])

    print "params (iters, threads, concs, ops):", warmiters, threads, cs, ops

    print "do warmup:"
    for i in range(3):
        print "iter", i, "time:", run(threads, cs, ops)

    print "turn off jitting"
    import gc
    turn_jitting_off()
    print "do", warmiters, "real iters:"
    times = []
    for i in range(warmiters):
        gc.collect()
        times.append(run(threads, cs, ops))
    print "warmiters:", times

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
