import asyncio
import logging
import os.path
from pkgutil import extend_path, walk_packages
from facts.conf import settings

__path__ = extend_path(__path__, __name__)
__all__ = ['graft']

GRAFTS = []


def graft(func):
    """Decorator for marking a function as a graft.
    """
    func = asyncio.coroutine(func)
    setattr(func, '_is_graft', True)
    GRAFTS.append(func)
    return func


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

    walker = walk_packages(__path__, '%s.' % __name__, onerror=notify_error)
    for module_finder, name, ispkg in walker:
        loader = module_finder.find_module(name)
        loader.load_module(name)

    return GRAFTS
