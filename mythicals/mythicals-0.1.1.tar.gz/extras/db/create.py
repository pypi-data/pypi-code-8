#!/usr/bin/env python
"""
Helper used to (re)create db.
"""
import argparse
import logging
import sys

import sqlalchemy as sa
from sqlalchemy import engine as sae

from mythicals import commands


logger = logging.getLogger(__name__)


def setup_logging(args):
    logging.basicConfig(
        level=args.log_level,
        format='%(asctime)s : %(levelname)s : %(name)s : %(message)s',
        stream=sys.stderr,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url', metavar='URL', help='postgresql://user:password@localhost:5432/db',
    )
    parser.add_argument(
        '-O', '--owner', metavar='USER', default=None,
    )
    parser.add_argument(
        '-E', '--encoding', metavar='CHARSET', default='utf8',
    )
    parser.add_argument(
        '-T', '--template', metavar='NAME', default='template0',
    )
    parser.add_argument(
        '-D', '--tablespace', metavar='NAME', default=None,
    )
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

    url = sae.url.make_url(args.url)

    postgres_url = sae.url.make_url(args.url)
    postgres_url.database = 'postgres'
    engine = sa.create_engine(str(postgres_url), echo=True)
    cxn = engine.connect()
    cxn.connection.set_isolation_level(0)  # AUTOCOMMIT

    # drop
    if args.delete:
        cxn.execute('ALTER DATABASE {} OWNER TO {}'.format(url.database, url.username))
        cxn.execute('DROP DATABASE IF EXISTS {}'.format(url.database))

    # create
    cmd = ['CREATE DATABASE {} WITH'.format(url.database)]
    params = {}
    for name, value in [
            ('TEMPLATE', args.template),
            ('TABLESPACE', args.tablespace),
        ]:
        if value is not None:
            cmd.append('    {} = {}'.format(name, value))
    for name, value in [('ENCODING', args.encoding)]:
        if value is not None:
            cmd.append('    {} = :{}'.format(name, name.lower()))
            params[name.lower()] = value
    cmd = sa.text('\n'.join(cmd))
    try:
        cxn.execute(cmd, **params)
    except sa.exc.ProgrammingError as ex:
        if 'database "{0}" already exists'.format(url.database) not in str(ex):
            raise

    # extensions
    engine = sa.create_engine(args.url, echo=True)
    cxn = engine.connect()
    cxn.connection.set_isolation_level(0)  # AUTOCOMMIT
    cxn.execute('CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;')
    cxn.execute('CREATE EXTENSION IF NOT EXISTS hstore WITH SCHEMA public;')
    cxn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;')

    # ownership
    cxn.execute('ALTER DATABASE {} OWNER TO {}'.format(url.database, args.owner))


if __name__ == '__main__':
    main()
