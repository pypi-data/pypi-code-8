import argparse
import os
import subprocess
import sys

from sqlalchemy import engine as sae

from mythicals import config


def parsers(commands, parents):
    root = argparse.ArgumentParser(add_help=False)
    root.add_argument(
        '--data',
        metavar='PATH',
        default=os.path.join(config.DATA_PREFIX, 'db'),
    )
    parents = parents + [root]

    parser = commands.add_parser('db', parents=parents)
    commands = parser.add_subparsers()
    role_parser(commands, parents)
    create_parser(commands, parents)
    schema_parser(commands, parents)


# role

def role_parser(commands, parents):
    parser = commands.add_parser(
        'role', parents=parents, description='role.py wrapper',
    )
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')
    parser.add_argument('remainder', nargs=argparse.REMAINDER)
    parser.set_defaults(command=role_command)


def role_command(args):
    url = sae.url.make_url(config.DB['url'])
    username, password = url.username, url.password
    url.username, url.password = args.username, args.password or ''
    url.database = ''
    cmd = [os.path.join(args.data, 'role.py'), str(url), username, password]
    if args.remainder:
        cmd.extend(args.remainder[1:])
    subprocess.check_call(
        cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
    )


# create

def create_parser(commands, parents):
    parser = commands.add_parser(
        'create', parents=parents, description='create.py wrapper',
    )
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')
    parser.add_argument('remainder', nargs=argparse.REMAINDER)
    parser.set_defaults(command=create_command)


def create_command(args):
    url = sae.url.make_url(config.DB['url'])
    ownername = url.username
    url.username = args.username or url.username
    url.password = args.password or url.password
    cmd = [os.path.join(args.data, 'create.py'), str(url), '-O', ownername]
    if args.remainder:
        remainder = args.remainder[1:]
        cmd.extend(remainder)
    subprocess.check_call(
        cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
    )


# schema

def schema_parser(commands, parents):
    parser = commands.add_parser(
        'schema', parents=parents, description='alembic wrapper',
    )
    parser.add_argument(
        'remainder', nargs=argparse.REMAINDER
    )
    parser.set_defaults(command=schema_command)


def schema_command(args):
    cmd = ['alembic', '-x', 'url=' + config.DB['url']]
    if args.remainder:
        remainder = args.remainder[1:]
        cmd.extend(remainder)
    subprocess.check_call(
        cmd, cwd=args.data, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
    )
