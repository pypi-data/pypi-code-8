import sys
import threading


__version__ = '1.0.1'


_PY2 = sys.version_info[0] == 2
_PY3 = sys.version_info[0] == 3
if _PY3:
    import queue as _Queue
elif _PY2:
    import Queue as _Queue
else:
    raise RuntimeError('Unsupported python version.')


def done(): pass
def abort(): pass
def clear(): pass


class _Backend(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._queue = _Queue.Queue()
        self._abort_event = threading.Event()
        self.setDaemon(True)
        self.start()

    def stop(self, timeout=None, msg=done):
        self.send(msg)
        self.join(timeout)
        # self._agent = None
        # self._queue = None
        # self._abort_event = None

    def run(self):
        if self._queue is None:
            return

        while True:
            if self._abort_event.is_set():
                break
            msg = self._queue.get()
            if msg is done:
                break
            ret = msg()
            if ret is False:
                break

    def send(self, msg):
        if msg is abort:
            if not self._abort_event.is_set():
                self._abort_event.set()
        elif msg is clear:
            while not self._queue.empty():
                self._queue.get()
        else:
            self._queue.put(msg)


class Agent(object):
    def __init__(self, auto_start_backend=True):
        self._main_thread_id = threading.current_thread().ident
        self._queue = _Queue.Queue()
        self._backend = None
        if auto_start_backend:
            self.start_backend()

    def start_backend(self):
        assert not self.is_backend_started()
        self._backend = _Backend()

    def stop_backend(self, timeout=None, msg=done):
        if not self.is_backend_started():
            return
        self._backend.stop(timeout, msg)
        self._backend = None

    def send_to_frontend(self, msg):
        self._queue.put(msg)

    def send_to_backend(self, msg):
        assert self.is_backend_started()
        self._backend.send(msg)

    def tick(self):
        """Handle all messages received from background

        return
            True: on no message or all message handled
            False: on handle message error
        """

        # thread maybe exit on error, in that case, the related active object will not be auto destroyed, so destroy it
        if self._backend and not self._backend.is_alive():
            self.stop_backend()

        while True:
            try:
                msg = self._queue.get_nowait()
            except _Queue.Empty:
                return True
            ret = msg()
            if ret is False:
                return False

        return True

    def is_backend_started(self):
        return self._backend is not None


class _CallWrapper:
    def __init__(self, agent, func, *args, **kwargs):
        self.agent = agent
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def __call__(self, *args, **kwargs):
        return self.func(self.agent, *self.args, **self.kwargs)


def backend(func):
    def wrapper(self, *args, **kwargs):
        if threading.current_thread().ident == self._main_thread_id:
            self.send_to_backend(_CallWrapper(self, func, *args, **kwargs))
        else:
            return func(self, *args, **kwargs)
    return wrapper


def frontend(func):
    def wrapper(self, *args, **kwargs):
        if threading.current_thread().ident == self._main_thread_id:
            return func(self, *args, **kwargs)
        else:
            self.send_to_frontend(_CallWrapper(self, func, *args, **kwargs))
    return wrapper
