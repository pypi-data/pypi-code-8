# -*- coding: utf-8 -*-
"""
<Short Summary>

Created on Fri Jul 10 15:37:15 2015

<Long Description>

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""
### Imports
# Standard Library
from __future__ import print_function, division
from __future__ import absolute_import
#from __future__ import unicode_literals
import logging
import sys
import decimal
import os.path as osp
import unittest

# Third Party
from docopt import docopt

# Package / Application
try:
    # Imports used for unittests
    from .. import main as tpedit
#    from . import pbsql
    logging.debug("Imports for UnitTests")
except (SystemError, ValueError):
    if __name__ == "__main__":
        # Allow module to be run as script
        print("Running module as script")
        sys.path.append(osp.dirname(osp.dirname(osp.abspath(__file__))))
        import main
    else:
        raise

    try:
#        # Imports used by Spyder
        import main as tpedit
#        import pbsql
        logging.debug("Imports for Spyder IDE")
    except ImportError:
#         # Imports used by cx_freeze
        from tpedit import main as tpedit
#        from pybank import pbsql
        logging.debug("imports for Executable")


class TestCase(unittest.TestCase):
    """
    """
    def test_test(self):
        self.assertTrue(True)


def main():
    """ Main Code """
#    docopt(__doc__, version=__version__)
    unittest.main(exit=False, verbosity=1)


if __name__ == "__main__":
    main()
