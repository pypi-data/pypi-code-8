# -*- coding: utf-8 -*-
# pylint: disable=E1101, C0330
#   E1101 = Module X has no Y member
"""
GUI Components for TPEdit

Created on Mon Jul 06 14:36:23 2015

Usage:
    gui.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function, division
from __future__ import absolute_import
#from __future__ import unicode_literals

# Allow this package to be run any which way
# See http://stackoverflow.com/a/27876800/1354930
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#        import douglib.core as core
    else:
#        from .. import core as core
        pass

from docopt import docopt

__author__ = "Douglas Thor"
__version__ = "v0.1.0"


def main():
    """ Main Code """
    docopt(__doc__, version=__version__)


if __name__ == "__main__":
    main()
