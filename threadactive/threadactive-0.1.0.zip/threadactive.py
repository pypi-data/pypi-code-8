import sys
import threading


__version__ = '0.1.0'


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
        self._active = _Active(self)
        self._queue = _Queue.Queue()

    def send_to_fore(self, msg):
        self._queue.put(msg)

    def send_to_back(self, msg):
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
