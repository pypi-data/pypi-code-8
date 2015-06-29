import asyncio
import logging
import os.path
from facts.conf import settings
from pkgutil import extend_path, walk_packages
from pkg_resources import iter_entry_points

__path__ = extend_path(__path__, __name__)
__all__ = ['graft']

GRAFTS = []


def graft(func):
    """Decorator for marking a function as a graft.
    """
    func = asyncio.coroutine(func)
    setattr(func, '_is_graft', True)
    return func


def is_graft(func):
    """Tells if func is a fragt.
    """
    return getattr(func, '_is_graft', False)


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
