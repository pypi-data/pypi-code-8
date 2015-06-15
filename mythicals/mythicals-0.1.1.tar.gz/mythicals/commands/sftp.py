import logging
import paramiko

import mythicals


logger = logging.getLogger(__name__)


def parsers(commands, parents):
    parser = commands.add_parser(
        'sftp', parents=parents, description='serve sftp',
    )
    parser.add_argument(
        '--host', metavar='HOST', default='127.0.0.1',
    )
    parser.add_argument(
        '-p', '--port', metavar='PORT', default=4522, type=int,
    )
    parser.add_argument(
        '--poll', metavar='SECONDS', default=1.0, type=float,
    )
    parser.add_argument(
        '-k', '--host-key', metavar='FILE', default='/etc/mythical/rsa',
    )
    parser.add_argument(
        '-f', '--forking', action='store_true', default=False,
    )
    parser.add_argument(
        '-t', '--threading', action='store_true', default=False,
    )
    parser.set_defaults(command=command)


def command(args):
    logger.debug('loading host-key @ %s', args.host_key)
    host_key = paramiko.RSAKey.from_private_key_file(args.host_key)
    if args.forking:
        server_cls = mythicals.sftp.ForkingSFTPServer
    elif args.threading:
        server_cls = mythicals.sftp.ThreadingSFTPServer
    else:
        server_cls = mythicals.sftp.SFTPServer
    server = server_cls(address=(args.host, args.port), host_key=host_key)
    logger.info('serving on sftp://%s:%s/ (poll=%s)', args.host, args.port, args.poll)
    server.serve_forever(args.poll)
