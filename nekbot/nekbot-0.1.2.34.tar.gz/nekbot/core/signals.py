# coding=utf-8
from collections import defaultdict
import threading

__author__ = 'nekmo'

class Events(defaultdict):
    def __init__(self):
        super(Events, self).__init__(list)

    def propagate(self, event, *args, **kwargs):
        if not event in self: return
        for function in self[event]:
            # TODO: Es necesario limitar el tiempo, hacer workers...
            l = threading.Thread(target=function, args=args, kwargs=kwargs)
            l.start()

events = Events()

def event(event_name):
    """Decorador para que se ejecute una función con un determinado evento.

    Uso:
        @event('mievento')
        def function():
            pass
    """
    def decorator(f):
        events[event_name].append(f)
        return f
    return decorator