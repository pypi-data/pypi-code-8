from . import down, status, up

def parse_args(argv):
    parser = argparse.ArgumentParser(description='Migrations. Down. Up.')
    parser.add_argument(
        '--directory', dest='directory', default='./migrations',
        help='The directory of the migrations.'
    )
    parser.add_argument(
        '--database', dest='database',
        help='The database to perform the migrations on.'
    )

    subparsers = parser.add_subparsers(help='sub-command help')

    status_cmd = subparsers.add_parser(
        'status', help='Current migration status.'
    )
    status_cmd.set_defaults(func=status)

    up_cmd = subparsers.add_parser('up', help='Migrate up.')
    up_cmd.set_defaults(func=up)
    up_cmd.add_argument(
        'count', type=int, help='How many migrations to go up.'
    )
    up_cmd.add_argument(
        '--fake', dest='fake', type=bool, default=False,
        help='Fake the migration.'
    )

    down_cmd = subparsers.add_parser('down', help='Migrate down.')
    down_cmd.set_defaults(func=down)
    down_cmd.add_argument(
        'count', type=int, help='How many migrations to go down.'
    )

    return parser.parse_args(argv)


def main():
    sys.argv.pop(0)
    argv = parse_args(sys.argv)
    argv.func(argv)
