import re

from fabric.api import env

import functools

from . import log


class Requires(object):
    """Decorator to document environment usage.

    This decorator is used in task definitions to indicate that
    the task requires some nexiles specific environment.

    Usage::

        @task
        @utils.Require(foo=str, bar=bool)
        def something():
            pass

    .. versionadded: 0.1.2
    """

    def __init__(self, **kw):
        # log.info("Requires.__init__: {}".format(repr(self)))
        self.kw = kw
        self.docs = " Requires: {}".format(",".join(kw.keys()))

    def __call__(self, func):
        # log.info("Requires.__call__: {} {}".format(repr(self), self.docs))
        func.__doc__ += self.docs

        @functools.wraps(func)
        def wrapper(*args, **kw):
            for k, v in self.kw.items():
                if not k in env.nexiles:
                    log.error("{} needs environment {}!".format(func.__name__, k))
                    raise RuntimeError("Missing environment {}.".format(k))

            return func(*args, **kw)

        return wrapper


def get_version_from_setup_py(filename=None):
    """get_version_from_setup_py() -> string

    Extract and return the version form the setup.py file."""
    if filename is None:
        filename = "setup.py"
    with file(filename) as f:
        for line in f:
            if line.startswith("version"):
                return re.split("version = '(.*)'", line)[1]

# EOF
