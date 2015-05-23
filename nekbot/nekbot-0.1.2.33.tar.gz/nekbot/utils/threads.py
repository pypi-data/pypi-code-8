import threading

__author__ = 'nekmo'

class TimeLimitExpired(Exception):
    pass

def timelimit(timeout, func, args=(), kwargs=None):
    """ Run func with the given timeout. If func didn't finish running
        within the timeout, raise TimeLimitExpired
    """
    if kwargs is None:
        kwargs = {}
    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            self.result = func(*args, **kwargs)

        def _stop(self):
            if self.isAlive():
                threading.Thread._Thread__stop(self)

    it = FuncThread()
    it.start()
    it.join(timeout)
    if it.isAlive():
        it._stop()
        raise TimeLimitExpired()
    else:
        return it.result