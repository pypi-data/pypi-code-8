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
        log.info("Initializing environment.")
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

@task
def dump():
    """dumps nexiles specific fabric environment"""
    for k, v in env.nexiles.items():
        print "{:>30} := {}".format(k, v)

if "nexiles" not in env:
    env.nexiles = NexilesEnv()