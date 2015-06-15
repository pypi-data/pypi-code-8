from mythicals import http


def parsers(commands, parents):
    parser = commands.add_parser(
        'http', parents=parents, description='serve http',
    )
    parser.add_argument(
        '--host', metavar='HOST', default='127.0.0.1',
    )
    parser.add_argument(
        '-p', '--port', metavar='PORT', default=4580, type=int,
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
    )
    parser.set_defaults(command=command)


def command(args):
    http.app.run(host=args.host, port=args.port, debug=args.debug)
