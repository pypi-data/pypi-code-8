#!/usr/bin/env python
"""
Helper used to create role.
"""
import argparse
import logging
import sys

import sqlalchemy as sa

from mythicals import __version__, commands


logger = logging.getLogger(__name__)


def setup_logging(args):
    logging.basicConfig(
        level=args.log_level,
        format='%(asctime)s : %(levelname)s : %(name)s : %(message)s',
        stream=sys.stderr,
    )


def main():
    parser = argparse.ArgumentParser(
        version=__version__,
        description='Helper used to create role.',
    )
    parser.add_argument(
        'url', metavar='CONNECTION', help='postgresql://user:password@localhost:5432/',
    )
    parser.add_argument('name')
    parser.add_argument('password')

    parser.add_argument(
        '-l', '--log-level',
        choices=commands.LogLevelAction.choices,
        default=logging.WARNING,
        metavar='LEVEL',
        action=commands.LogLevelAction,
    )
    parser.add_argument(
        '--delete', action='store_true', default=False
    )

    args = parser.parse_args()

    setup_logging(args)

    engine = sa.create_engine(args.url + 'postgres', echo=True)
    cxn = engine.connect()
    cxn.connection.set_isolation_level(0)  # AUTOCOMMIT

    # drop
    if args.delete:
        cxn.execute('DROP ROLE IF EXISTS {}'.format(args.name))

    # create
    cmd = [
        'CREATE ROLE {} WITH'.format(args.name),
        '    CREATEDB',
        '    LOGIN',
        "    ENCRYPTED PASSWORD '{}'".format(args.password)
    ]
    params = {}
    cmd = sa.text('\n'.join(cmd))
    try:
        cxn.execute(cmd, **params)
    except sa.exc.ProgrammingError as ex:
        if 'role "{0}" already exists'.format(args.name) not in str(ex):
            raise


if __name__ == '__main__':
    main()
