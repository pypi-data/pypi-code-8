# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import *
VERSION = (0, 1, 3)

from .base import BaseImporter, ValidationError
from .readers import *
#from . import tests


def get_version():
    "Returns the version as a human-format string."
    return '.'.join([str(i) for i in VERSION])


__version__ = get_version()
