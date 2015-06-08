import sys
import threading
import inspect
import ctypes


__version__ = '0.1.4'


_PY2 = sys.version_info[0] == 2
_PY3 = sys.version_info[0] == 3
if _PY3:
    import queue as _Queue
elif _PY2:
    import Queue as _Queue
else:
    raise RuntimeError('Unsupported python version.')


def _async_raise(tid, exception_type):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exception_type):
        exception_type = type(exception_type)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exception_type))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class _Active(threading.Thread):
    def __init__(self, agent):
        threading.Thread.__init__(self)
        self._agent = agent
        self._queue = _Queue.Queue()
        self.start()

    def stop(self, timeout=None):
        """Stop the thread within timeout

        if timeout is None then terminate the thread immediately
        if timeout happens then force terminate the thread
        """
        if timeout is None:
            _async_raise(self.ident, SystemExit)
        else:
            self.send(None)
            self.join(timeout)
            if self.is_alive():
                _async_raise(self.ident, SystemExit)

        self._agent = None
        self._queue = None

    def run(self):
        if self._queue is None:
            return

        while True:
            msg = self._queue.get()
            if msg is None:
                break
            msg(self._agent)

    def send(self, msg):
        self._queue.put(msg)


class Agent(object):
    def __init__(self, auto_start=True):
        self._main_thread_id = threading.current_thread().ident
        self._active = None
        self._queue = None
        if auto_start:
            self.start()

    def start(self):
        assert not self.is_started()
        self._active = _Active(self)
        self._queue = _Queue.Queue()

    def stop(self, timeout=None):
        """Wait until timeout(if not None) or terminate immediately"""
        if not self.is_started():
            return
        self._active.stop(timeout)
        self._active = None
        self._queue = None

    def send_to_frontend(self, msg):
        assert self.is_started()
        self._queue.put(msg)

    def send_to_backend(self, msg):
        assert self.is_started()
        self._active.send(msg)

    def tick(self):
        """Handle all messages received from background

        return
            True: on no message or all message handled
            False: on handle message error
        """
        assert self.is_started()

        while True:
            try:
                msg = self._queue.get_nowait()
            except _Queue.Empty:
                return True
            ret = msg()
            if ret is False:
                return False
        return True

    def is_started(self):
        return self._active is not None


class _CallWrapper:
    def __init__(self, agent, func, *args, **kwargs):
        self.agent = agent
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def __call__(self, *args, **kwargs):
        self.func(self.agent, *self.args, **self.kwargs)


def backend(func):
    def wrapper(self, *args, **kwargs):
        if threading.current_thread().ident == self._main_thread_id:
            self.send_to_backend(_CallWrapper(self, func, *args, **kwargs))
        else:
            func(self, *args, **kwargs)
    return wrapper


def frontend(func):
    def wrapper(self, *args, **kwargs):
        if threading.current_thread().ident == self._main_thread_id:
            func(self, *args, **kwargs)
        else:
            self.send_to_frontend(_CallWrapper(self, func, *args, **kwargs))
    return wrapper
