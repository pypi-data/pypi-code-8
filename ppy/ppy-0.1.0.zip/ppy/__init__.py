"""
ppy
---

Packaging for Python.

:copyright: (c) 2014 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import, print_function

__version__ = '0.1.0'

from .cli import main
from .hooks import install


__all__ = ['__version__', 'main', 'install']
