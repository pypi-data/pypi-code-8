"""
ppy.installer
~~~~~~~~~~~~~

Exposes the import hook install function.
"""

from __future__ import absolute_import, print_function

import sys
import os
import imp
from .resolver import site_packages_dirname


class InstallationFinder(object):
    """
    Import hook that searches the for a site-packages directory. If
    found, this directory gets added to the import search path.
    """

    def __init__(self, path_entry):
        # TODO: Handle accessing parent site-packages from inside a package
        #       by searching up the directory tree

        # Handle any path that contains a local site packages
        local_site_packages = os.path.join(path_entry, site_packages_dirname)
        if not os.path.isdir(local_site_packages):
            # Indicate this import hook is not to be used for this module
            raise ImportError()

        self.path_entry = path_entry
        self.local_site_packages = local_site_packages

    def find_module(self, fullname, path=None):
        return self

    def load_module(self, fullname):
        # Handle packages
        fullname = fullname.split('.')[-1]

        # Load from the local site packages
        path = list(sys.path)
        path.insert(1, self.local_site_packages)

        # Load the entry module from installed package
        f = None
        try:
            f, pathname, desc = imp.find_module(fullname, path)
            module = imp.load_module(fullname, f, pathname, desc)
        except ImportError:
            # TODO: Remove hooks.py from ImportError tracebacks
            #exc_info = sys.exc_info()
            #raise exc_info[0], exc_info[1], exc_info[2].tb_next
            raise
        finally:
            if f:
                f.close()

        # Set the loader and return the module
        module.__loader__ = self
        return module


class EntryPointFinder(object):
    """
    Import hook that allows importing a directory that contains
    a requirements.json, which has one or more modules and packages.

    This allows all dependencies to be wrapped in a directory.

    This is important so you can still install modules.
    """

    # TODO: How to handle projects that contain multiple packages?
    # TODO: Actually need this hook?
    # TODO: Just use site-packages like normal?

    def __init__(self, path_entry):
        # Handle site-packages
        path_base = os.path.basename(os.path.dirname(path_entry))
        if path_base != site_packages_dirname:
            raise ImportError()

        req_path = os.path.join(path_entry, 'requirements.json')
        if not os.path.exists(req_path) or os.path.isdir(req_path):
            raise ImportError()

        self.path_entry = path_entry

    def find_module(self, fullname, path=None):
        return self

    def load_module(self, fullname):
        # Handle packages
        fullname = fullname.split('.')[-1]

        # TODO: Read requirements.json (?)

        print('Found ', fullname)

        path = list(sys.path)
        # TODO: path.insert a path from requirements.json

        # Load the entry module from installed package
        f, pathname, desc = imp.find_module(fullname, path)
        try:
            module = imp.load_module(fullname, f, pathname, desc)
        finally:
            if f:
                f.close()

        # Set the loader and return the module
        module.__loader__ = self
        return module


def monkey_patch_pip():
    try:
        from .pip_patch import patch
    except ImportError:
        return

    patch()


def install():
    """Installs an import hook to import local site packages."""
    sys.path_hooks.append(InstallationFinder)
    # TODO: sys.path_hooks.append(EntryPointFinder)
    monkey_patch_pip()
