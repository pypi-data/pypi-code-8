import argparse
from . import Logical, UserFacts
from .serializer import dump, load
from .targeting import NotFound
from aioutils import Group
from facts.conf import settings


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug',
                        action='store_true',
                        help='activate debug mode')

    cmds = parser.add_subparsers(dest='command')
    cmds.required = True

    all_parser = cmds.add_parser('all', help='get all facts')
    all_parser.set_defaults(handle=all_handler)
    all_parser.add_argument('--human',
                            action='store_true',
                            dest='humanize',
                            help='humanize display')

    match_parser = cmds.add_parser('match', help='match a fact')
    match_parser.set_defaults(handle=match_handler)
    match_parser.add_argument('target')

    read_parser = cmds.add_parser('read', help='get a fact')
    read_parser.set_defaults(handle=read_handler)
    read_parser.add_argument('target')
    read_parser.add_argument('--human',
                             action='store_true',
                             dest='humanize',
                             help='humanize display')

    write_parser = cmds.add_parser('write', help='set a fact')
    write_parser.set_defaults(handle=write_handler)
    write_parser.add_argument('target')
    write_parser.add_argument('value')
    write_parser.add_argument('--format',
                              choices={'plain', 'yaml'},
                              default='plain',
                              help='in which format value must be evaluated')

    group = write_parser.add_mutually_exclusive_group()
    group.add_argument('--replace',
                       action='store_false',
                       dest='merge',
                       default=False)
    group.add_argument('--merge',
                       action='store_true',
                       dest='merge')

    delete_parser = cmds.add_parser('delete', help='delete a fact')
    delete_parser.set_defaults(handle=delete_handler)
    delete_parser.add_argument('target')

    return parser


def all_handler(parser, args):
    g = Group()
    logical = Logical()
    task = g.spawn(logical.as_dict())
    g.join()
    msg = dump(task.result(),
               explicit_start=True,
               default_flow_style=False,
               humanize=args.humanize)
    parser.exit(0, msg)


def read_handler(parser, args):
    g = Group()
    logical = Logical()
    task = g.spawn(logical.read(args.target))
    g.join()
    try:
        resp = task.result()
        code = 0
    except NotFound:
        resp = None
        code = 1
    msg = dump(resp,
               explicit_start=True,
               default_flow_style=False,
               humanize=args.humanize)
    parser.exit(code, msg)


def match_handler(parser, args):
    g = Group()
    logical = Logical()
    task = g.spawn(logical.match(args.target))
    g.join()
    try:
        resp = task.result()
    except NotFound:
        resp = None
    msg = dump(resp, explicit_start=True, default_flow_style=False)
    parser.exit(0, msg)


def write_handler(parser, args):
    user_facts = UserFacts(settings.userfacts)
    if args.format == 'yaml':
        args.value = load(args.value)
    user_facts.write(args.target, args.value, args.merge)


def delete_handler(parser, args):
    user_facts = UserFacts(settings.userfacts)
    user_facts.delete(args.target)


def resolve(*tasks):
    """docstring for resolve"""
    pass


def run():
    parser = get_parser()
    args = parser.parse_args()
    try:
        args.handle(parser, args)
    except Exception as error:
        if args.debug:
            raise
        parser.error(error)


if __name__ == '__main__':
    run()
