import uuid
import functools

from google.appengine.ext import deferred as gae_deferred

__all__ = [
    'task',
    'defer',
]


DEFERRED_URL = '/gaetasks/{}'


def defer(obj, *args, **kwargs):
    reference = '{}.{}'.format(
        obj.__module__,
        obj.__name__,
    )
    _url = DEFERRED_URL.format(reference)
    kwargs.setdefault('_url', _url)

    name = reference.replace('.', '-')
    name = '{}-{}'.format(name, uuid.uuid4().hex)
    kwargs.setdefault('_name', name)
    return gae_deferred.defer(obj, *args, **kwargs)


class Task(object):
    def __call__(self, fn):
        def delay(*args, **kwargs):
            return defer(fn, *args, **kwargs)
        fn.delay = delay
        return fn

task = Task
