import os
import json

import logging

from fabric.api import env
from fabric.api import task

from . import log
from . import utils

DEFAULT_ENV = {
    # Do **NOT** allow pypi publishing by default.
    "public_source": False,
}


class NexilesEnv(object):
    """NexilesEnv

    A dict subclass with attribute access and overwite
    warnings.
    """

    __defaults__ = {
        "doc_package": "{build_dir}/{package_name}-docs-{version}.zip",
    }

    def __init__(self, **kw):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("__init__: %r", kw)
        self.data = {}
        self.update(**DEFAULT_ENV)
        self.update(**kw)

    def setdefault_expand(self, key, default):
        """setdefault_expand(key, default) -> value

        like setdefault() but also expands {} formats."""
        self.logger.debug("setdefault_expand: %s (%r)", key, default)
        if key not in self.data:
            val = default.format(**self.data)
            self.data[key] = val
            self.logger.debug("setdefault_expand: SET %s <= %r", key, val)
            log.warning("   {} not set, setting default: {}".format(key, val))
            return val
        return self.data[key]

    def setdefault(self, key, default):
        """setdefault(key, default) -> value"""
        self.logger.debug("setdefault: %s (%r)", key, default)
        if key not in self.data:
            self.logger.debug("setdefault: SET %s <= %r", key, default)
            self.data[key] = default
            log.warning("   {} not set, setting default: {}".format(key, default))
            return default
        return self.data[key]

    def update(self, **kw):
        """update(**kwargs) -> None

        Update key in self and warn when overwriting
        a key."""
        for k, v in kw.items():
            if k in self.data:
                log.warning("Overwriting environment key: {} := '{}', was {}".format(k, v, self[k]))
            self.data[k] = v

    def initialize(self, **kw):
        self.logger.debug("initialize: %r", kw)
        log.info("Initializing environment.")
        self.update(**kw)

        self.setdefault("root_dir", os.getcwd())
        self.setdefault("dist_root", os.path.expanduser("~/develop/nexiles/dist"))
        self.setdefault_expand("build_dir", "{root_dir}/build")

        if "version" not in self.data and "setup_py" in self.data:
            self.setdefault("version", utils.get_version_from_setup_py(self.setup_py))

    def __getitem__(self, k):
        self.logger.debug("__getitem__: %s", k)
        if k not in self.data and k in self.__defaults__:
            try:
                val = self.__defaults__[k].format(**self.data)
                log.warning("   {} not set, using default: {}".format(k, val))
                self.data[k] = val
                return val
            except KeyError, e:
                self.logger.error("Exception when trying to set default", exc_info=True)
                raise
        return self.data.__getitem__(k)

    def __setitem__(self, k, v):
        self.logger.debug("__setitem__: %s <= %r", k, v)
        self.data.__setitem__(k, v)

    def __getattr__(self, k):
        self.logger.debug("__getattr__: %s", k)
        return self.__getitem__(k)

    def __contains__(self, k):
        return k in self.data or k in self.__defaults__

    def keys(self):
        return list(set(self.data.keys() + self.__defaults__.keys()))


def read_from_file(fn):
    """read_from_file(filename) -> env

    Reads config from given filename and updates
    the environment.

    Creates a new environmant if none is found.
    """
    with file(fn) as config:
        return read_from_string(config.read())


def read_from_string(s):
    """read_from_string(string) -> env

    Parses JSON from s and updates env.  Returns
    new env if none found.
    """
    e = env.setdefault("nexiles", NexilesEnv())

    e.update(**json.loads(s))

    return e


@task
def dump():
    """dumps nexiles specific fabric environment"""
    for k, v in env.nexiles.items():
        print "{:>30} := {}".format(k, v)

if "nexiles" not in env:
    env.nexiles = NexilesEnv()
    if os.path.exists("fabric.json"):
        log.info("Loading fabric env from fabric.json")
        try:
            read_from_file("fabric.json")
        except ValueError, e:
            log.error("Invalid JSON in fabric.json!")
            raise

# EOF
