from Queue import Queue, Empty, Full
from threading import Thread, Condition, RLock, local
import thread, atexit, sys, time

try:
    from pypystm import atomic, getsegmentlimit, hint_commit_soon
except ImportError:
    raise
    atomic = RLock()
    def getsegmentlimit():
        return 1
    def hint_commit_soon():
        pass

def print_abort_info(tm=0.0):
    "backward compatibility: no-op"


class TLQueue_concurrent(object):
    def __init__(self):
        my_id = thread.get_ident()
        self._tl_items = {my_id : []}
        self._new_items = Condition()
        self._c = 0

    def put(self, v):
        # conflicts with any put() and get()s from
        # the chosen queue:
        c = (id(v) // 5) % len(self._tl_items)
        items = self._tl_items.values()[c]

        with self._new_items:
            items.append(v)
            self._new_items.notify_all()

    def _get_my_items(self):
        my_id = thread.get_ident()
        try:
            items = self._tl_items[my_id]
        except KeyError:
            items = []
            self._tl_items[my_id] = items
        return items

    def get(self):
        # tries first to get item from its
        # own thread-local queue
        items = self._get_my_items()
        with atomic:
            if items:
                return items.pop()

        while True:
            with self._new_items:
                # steal from other queues
                for its in self._tl_items.values():
                    with atomic:
                        if its:
                            return its.pop()
                self._new_items.wait()

class TLQueue(object):
    def __init__(self):
        self.items = []
        self._new_items = Condition()

    def put(self, v):
        self.items.append(v)
        with self._new_items:
            self._new_items.notify_all()

    def get(self):
        items = self.items
        with atomic:
            if items:
                return items.pop()

        while True:
            with self._new_items:
                with atomic:
                    if items:
                        return items.pop()

                self._new_items.wait()


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, queue):
        Thread.__init__(self)
        self.daemon = True
        self.queue = queue
        self.start()

    def run(self):
        while True:
            func, args, kwds = self.queue.get()
            try:
                func(*args, **kwds)
            except Exception as e:
                print e


class ThreadPool(object):
    def __init__(self, n_workers=None):
        self.input_queue = TLQueue()
        if n_workers is None:
            n_workers = getsegmentlimit()
        self.workers = [Worker(self.input_queue) for i in range(n_workers)]

    def add_task(self, func, *args, **kwds):
        self.input_queue.put((func, args, kwds))

    def shutdown(self):
        for w in self.workers:
            #self.input_queue.put((print_abort_info, (), {}))
            self.input_queue.put((sys.exit, (), {}))
        for w in self.workers:
            w.join()


_thread_pool = ThreadPool()
atexit.register(_thread_pool.shutdown)

def set_thread_pool(th):
    global _thread_pool
    if _thread_pool:
        _thread_pool.shutdown()
    _thread_pool = th


class Future(object):
    def __init__(self, func, *args, **kwargs):
        self._done = False
        self._result = None
        self._exception = None
        self._cond = Condition()

        assert hasattr(func, "__call__")

        _thread_pool.add_task(self._task, func, *args, **kwargs)


    def _task(self, func, *args, **kwargs):
        with self._cond:
            try:
                hint_commit_soon()
                self._result = func(*args, **kwargs)
                hint_commit_soon()
            except Exception as e:
                self._exception = e
            finally:
                self._done = True
                # several points/threads in the program
                # may wait for the result (notify_all):
                self._cond.notify_all()


    def __call__(self):
        if not self._done:
            with self._cond:
                while not self._done:
                    self._cond.wait()

        if self._exception:
            raise self._exception

        return self._result



class AtomicFuture(Future):
    def _task(self, func, *args, **kwargs):
        with self._cond:
            try:
                hint_commit_soon()
                with atomic:
                    self._result = func(*args, **kwargs)
                hint_commit_soon()
            except Exception as e:
                self._exception = e
            finally:
                self._done = True
                # several points/threads in the program
                # may wait for the result (notify_all):
                self._cond.notify_all()
