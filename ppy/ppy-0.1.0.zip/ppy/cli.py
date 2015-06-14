"""
ppy.cli
~~~~~~~

Implements the command-line interface to ppy.


Usage:
  ppy -h | --help
  ppy --version

Where:
  <path> is a file to render or a directory containing README.md (- for stdin)
  <address> is what to listen on, of the form <host>[:<port>], or just <port>

Options:
  --save, -S        Package will appear in your dependencies
"""

from __future__ import absolute_import, print_function


def main(argv=None):
    """The entry point of the application."""

    # Defer imports until Python has fully loaded
    import sys
    from docopt import docopt
    from . import __version__

    if argv is None:
        argv = sys.argv[1:]
    version = 'ppy ' + __version__

    usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
    args = docopt(usage, argv=argv, version=version)

    # TODO: implement
    print('ppy')

    # TODO: Package checker to verify setup.py, setup.cfg, etc. look good

    # TODO: Add --save option to pip?
