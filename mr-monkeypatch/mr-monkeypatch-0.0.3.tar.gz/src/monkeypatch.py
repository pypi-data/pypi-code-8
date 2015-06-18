#!/usr/bin/python
# Filename: monkeypatch_test.py

import re
import logging
from collections import defaultdict
try:
    import exceptions
except:
    exceptions = type('Exception', (), {'AttributeError': AttributeError})

__resolve__ = defaultdict(dict)
__pending_resolve__ = {}


def _bypass(attr):
    return attr in ['cls', 'path', 'obj'] or attr.startswith('__')


class _ProxyClass(object):

    def __init__(self, cls, obj, path=''):
        self.__mp_obj = obj
        self.__mp_cls = cls
        self.__mp_path = path

    def __call__(self, *args, **kwargs):
        for cls in self.__mp_cls.mro():
            for path, func in __resolve__[cls].items():
                m = re.match(path, self.__mp_path)
                if m:
                    args = (self.__mp_obj,) + m.groups() + args
                    return func(*args, **kwargs)
        # Fail to resolve
        raise exceptions.AttributeError(self.__mp_cls + 'is not callable')

    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except exceptions.AttributeError:
            return _ProxyClass(self.__mp_cls, self.__mp_obj, self.__mp_path + '.' + attr)


def monkeypatch(cls):
    """Class decorator.
    """
    global __resolve__, __pending_resolve__
    __resolve__[cls] = __pending_resolve__
    __pending_resolve__ = {}

    def getattribute(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except exceptions.AttributeError:
            return _ProxyClass(cls, self, attr)

    return type(cls.__name__, (cls,), {
        '__getattribute__': getattribute,
        '__original_getattribute__': cls.__getattribute__,
    })


def route(path):
    """Return a decorator.
    """
    def decorator(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        global __pending_resolve__
        __pending_resolve__[path] = func
        return inner
    return decorator
