"""
ppy.imports
~~~~~~~~~~~

Import helpers, including a backport of importlib.import_module from 3.x.
"""

from __future__ import absolute_import, print_function

import sys


def try_import_module(module_name, quiet=False):
    """
    Imports the specified object and shows a descriptive error if it
    does not exist.
    """
    try:
        return import_module(module_name)
    except ImportError:
        if not quiet:
            print(('ppy error: {!r} exists but could not import {!r}. '
                   'ppy will not be used.').format('pip', module_name))
        raise


def try_import_name(name, quiet=False):
    """
    Imports the specified object and shows a descriptive error if it
    does not exist.
    """
    names = name.split('.')
    module_name, object_name = '.'.join(names[:-1]), names[-1]
    module = try_import_module(module_name, quiet=quiet)
    try:
        return getattr(module, object_name)
    except AttributeError:
        return try_import_module(name, quiet=quiet)


def try_import(*names):
    # Optimize when no fallbacks present
    if len(names) == 1:
        return try_import_name(names[0])

    # Try import names and fallbacks
    for name in names:
        try:
            return try_import_name(name, quiet=True)
        except ImportError:
            pass

    # Show error
    return try_import_name(names[0])


# --- Backport of importlib.import_module from 3.x ---

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                             "package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]
