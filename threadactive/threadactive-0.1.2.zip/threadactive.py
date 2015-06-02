import sys
import threading


__version__ = '0.1.2'


_PY2 = sys.version_info[0] == 2
_PY3 = sys.version_info[0] == 3
if _PY3:
    import queue as _Queue
elif _PY2:
    import Queue as _Queue
else:
    raise RuntimeError('Unsupported python version.')


class _Active(threading.Thread):
    def __init__(self, agent):
        threading.Thread.__init__(self)
        self._agent = agent
        self._queue = _Queue.Queue()
        self.start()

    def stop(self, timeout=None):
        self.send(None)
        self.join(timeout)

    def run(self):
        while True:
            msg = self._queue.get()
            if msg is None:
                break
            msg(self._agent)

    def send(self, msg):
        self._queue.put(msg)


class Agent(object):
    def __init__(self):
        self._main_thread_id = threading.current_thread().ident
        self._active = _Active(self)
        self._queue = _Queue.Queue()

    def send_to_frontend(self, msg):
        self._queue.put(msg)

    def send_to_backend(self, msg):
        self._active.send(msg)

    def tick(self):
        """Handle all messages received from background

        return
            True: on no message or all message handled
            False: on handle message error
        """
        while True:
            try:
                msg = self._queue.get_nowait()
            except _Queue.Empty:
                return True
            ret = msg()
            if ret is False:
                return False
        return True

    def stop(self, timeout=None):
        """Wait until timeout(if not None) or all message handled in background"""
        self._active.stop(timeout)


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
            self.send_to_backend(_CallWrapper(self, func, args, kwargs))
        else:
            func(self, *args, **kwargs)
    return wrapper


def frontend(func):
    def wrapper(self, *args, **kwargs):
        if threading.current_thread().ident == self._main_thread_id:
            func(self, *args, **kwargs)
        else:
            self.send_to_frontend(_CallWrapper(self, func, args, kwargs))
    return wrapper
