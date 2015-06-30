import asyncio
import functools
import logging
import os.path
from collections import namedtuple
from facts.conf import settings
from pkgutil import extend_path, walk_packages
from pkg_resources import iter_entry_points

__path__ = extend_path(__path__, __name__)
__all__ = ['graft', 'Graft', 'Namespace']

GRAFTS = []

Namespace = namedtuple('Namespace', 'namespace value')


class Graft:

    def __init__(self, func, *, namespace=None):
        self.func = asyncio.coroutine(func)
        self.namespace = namespace

    @asyncio.coroutine
    def __call__(self, *arg, **kwargs):
        response = yield from self.func(*arg, **kwargs)
        return Namespace(self.namespace, response)


def graft(func=None, *, namespace=None):
    """Decorator for marking a function as a graft.

    Parameters:
        namespace (str): namespace of data, same format as targeting.
    Returns:
        Graft

    For example, these grafts::

        @graft
        def foo_data:
            return {'foo', True}

        @graft(namespace='bar')
        def bar_data:
            return False

    will be redered has::

        {
            'foo': True,
            'bar': False
        }
    """

    if not func:
        return functools.partial(graft, namespace=namespace)

    if isinstance(func, Graft):
        return func

    return Graft(func, namespace=namespace)


def is_graft(func):
    """Tells if func is a graft.
    """
    return isinstance(func, Graft)


def load(force=False):
    """Magical loading of all grafted functions.

    Parameters:
        force (bool): force reload
    """

    if GRAFTS and not force:
        return GRAFTS

    # insert missing paths
    # this could be a configurated item
    userpath = settings.userpath
    if os.path.isdir(userpath) and userpath not in __path__:
        __path__.append(userpath)

    def notify_error(name):
        logging.error('unable to load %s package' % name)

    # autoload decorated functions
    walker = walk_packages(__path__, '%s.' % __name__, onerror=notify_error)
    for module_finder, name, ispkg in walker:
        loader = module_finder.find_module(name)
        mod = loader.load_module(name)
        for func in mod.__dict__.values():
            if is_graft(func):
                GRAFTS.append(func)

    # append setuptools modules
    for entry_point in iter_entry_points(group=settings.entry_point):
        try:
            func = entry_point.load()
            if is_graft(func):
                GRAFTS.append(func)
            else:
                notify_error(entry_point.name)
        except Exception as error:
            logging.exception(error)
            notify_error(entry_point.name)

    return GRAFTS
