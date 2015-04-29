# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
import sys
from io import open
try:
    import simplejson as json
except ImportError:
    import json
import requests
from distutils.version import StrictVersion

PY3 = sys.version_info[0] == 3


if PY3:
    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value

else:
    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')


def touch(fname, times=None):
    dirname = '/'.join(fname.split('/')[:-1])
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with file(fname, 'a'):
        os.utime(fname, times)


def get_from_api(uri, config):
    """
        Get an object from the api
    """
    api_uri = config.get('oarapi', 'uri')
    api_limit = config.get('oarapi', 'limit')
    headers = {'Accept': 'application/json'}
    r = requests.get(api_uri + uri + "?limit=" + api_limit, headers=headers)
    if r.status_code != 200:
        print("Could not get " + api_uri + uri)
        r.raise_for_status()
    if StrictVersion(requests.__version__) >= StrictVersion("2.0.0"):
        return r.json()
    else:
        return r.json


def get(uri, config, reload_cache=False):
    """
        Get from the cache or from the api
    """
    view = uri.split("/")[1]
    if (config.cache['enabled'] and not reload_cache):
        cache_time = time.time() - os.path.getmtime(config.cache[view]['file'])
        if (os.path.isfile(config.cache[view]['file'])
                and cache_time < config.cache[view]['delay']):
            with open(config.cache[view]['file']) as fd:
                return json.load(fd)
    else:
        data = get_from_api(uri, config)
    if config.cache['enabled']:
        touch(config.cache[view]['file'])
        with open(config.cache[view]['file'], 'w') as fd:
            json.dump(data, fd)
    return data


def cprint(str, *args):
    """
        Custom print function to get rid of trailing newline and space
    """
    sys.stdout.write(str % args)


def init_colorama():
    from colorama import init
    init()


class CachedProperty(object):

    """ A property that is only computed once per instance and then replaces
    itself with an ordinary attribute. Deleting the attribute resets the
    property """

    def __init__(self, func):
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__.setdefault("_cache", {})
        cached_value = obj._cache.get(self.__name__, None)
        if cached_value is None:
            # don't cache None value
            obj._cache[self.__name__] = self.func(obj)
        return obj._cache.get(self.__name__)


cached_property = CachedProperty


def unset_proxy_from_env():
    for var in ('http_proxy', 'https_proxy'):
        try:
            del os.environ[var]
        except:
            pass
