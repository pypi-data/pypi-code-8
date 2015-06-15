"""
Commands for interacting w/ a mythicals installation. These are typically accessed
via ``mythicals`` from your terminal:

.. code:: bash

    $ vaults --help

"""
__all__ = [
    'parser',
    'LogLevelAction',
]

import argparse
import logging
import os

from mythicals import __version__, tracer


def parser():

    root = argparse.ArgumentParser(add_help=False)
    root.add_argument(
        '-l', '--log-level',
        choices=LogLevelAction.choices,
        default=None,
        metavar='LEVEL',
        action=LogLevelAction,
    )
    root.add_argument(
        '--log-conf', metavar='FILE', default=None,
    )
    root.add_argument(
        '-c', '--conf-file', metavar='FILE', default=None,
    )

    parser = argparse.ArgumentParser(version=__version__, parents=[root])

    commands = parser.add_subparsers(title='commands')
    shell.parsers(commands, [root])
    db.parsers(commands, [root])
    user.parsers(commands, [root])
    http.parsers(commands, [root])
    sftp.parsers(commands, [root])

    return parser


class LogLevelAction(argparse.Action):

    mapping = {
        'd': logging.DEBUG, 'debug': logging.DEBUG,
        'i': logging.INFO, 'info': logging.INFO,
        'w': logging.WARNING, 'warn': logging.WARNING,
        'e': logging.ERROR, 'err': logging.ERROR, 'error': logging.ERROR,
    }

    choices = [
        'd', 'debug',
        'i', 'info',
        'w', 'warn',
        'e', 'err', 'error'
    ]

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            values = [self.mapping[v] for v in values]
        else:
            values = self.mapping[values]
        setattr(namespace, self.dest, values)


from . import shell
from . import db
from . import user
from . import http
from . import sftp
