import os
import json

from fabric.api import env
from fabric.api import task

from . import log

DEFAULT_ENV = {
    # Do **NOT** allow pypi publishing by default.
    "public_source": False,
}


class NexilesEnv(dict):
    """NexilesEnv

    A dict subclass with attribute access and overwite
    warnings.
    """

    def __init__(self, **kw):
        self.update(**DEFAULT_ENV)
        self.update(**kw)

    def update(self, **kw):
        """update(**kwargs) -> None

        Update key in self and warn when overwriting
        a key."""
        for k, v in kw.items():
            if k in self.__dict__:
                log.warning("Overwriting environment key: {} := '{}', was {}".format(k, v, self[k]))
            self[k] = v

    def __getattr__(self, k):
        return self[k]


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
    log.info("Initializing environment.")
    env.nexiles = NexilesEnv()
    if os.path.exists("fabric.json"):
        log.info("Loading fabric env from fabric.json")
        try:
            read_from_file("fabric.json")
        except ValueError, e:
            log.error("Invalid JSON in fabric.json!")
            raise

# EOF
