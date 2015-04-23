# encoding=utf-8

import functools


class decorator(object):

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, type=None):

        @functools.wraps(self.func)
        def _func(*args, **kwargs):
            method = functools.partial(self.func, obj)
            return self.call(method, *args, **kwargs)

        return _func

    def call(self, method, *args, **kwargs):
        return method(*args, **kwargs)


class single(decorator):
    def call(self, method, cr, uid, ids, *args, **kwargs):
        if _is_iterable(ids):
            ids = ids[0] if ids else None
        return super(single, self).call(method, cr, uid, ids, *args, **kwargs)


class batch(decorator):
    def call(self, method, cr, uid, ids, *args, **kwargs):
        if not _is_iterable(ids):
            ids = [ids]
        return super(batch, self).call(method, cr, uid, ids, *args, **kwargs)


def _is_iterable(val):
    try:
        return iter(val)
    except:
        return False
