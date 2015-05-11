#!/usr/bin/env python3
"""Simple server script for Cyrano apps.

Puts together the major pieces for the user, especially for development
and simple purposes.

If this isn't flexible or robust enough for your specific task, you
probably want to build your own custom serve script using Cyrano's API.
"""
import os
import sys
import argparse
assert sys.version_info >= (3, 3), "this only runs on Python 3.3+"
from ipaddress import ip_address
import logging.config
from cyrano.backends import backend


def port(value):
    """argparse argument validator for integers in network port range.
    """
    try:
        integer = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError('%r is not a port' % value)
    if not(0 < integer < 65536):
        raise argparse.ArgumentTypeError('%d is not a port' % integer)
    return integer


def filename(readable=True, writable=False):
    def filename_validator(value):
        if not isinstance(value, str):
            raise argparse.ArgumentTypeError(
                'non-string %r cannot be a filename' % value)
        if not os.path.exists(value):
            raise argparse.ArgumentTypeError(
                'filename %r does not exist' % value
            )
        return value

    return filename_validator


def argparser():
    """Make an argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Start a server.",
    )
    parser.add_argument(
        '--log-config', type=filename(readable=True),
        metavar='FILENAME',
        help='path to logging config file'
    )
    parser.add_argument(
        '--address', type=ip_address,
        nargs='*',
        metavar="IP",
        default=['127.0.0.1'],
        help="IP address to listen on; can use multiple times"
    )
    parser.add_argument(
        '--port', type=port, metavar='PORTNUMBER', default='4000',
        help='port to listen on',
    )
    parser.add_argument(
        '--debug', action='store_true',
        help="",
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help="",
    )
    parser.add_argument(
        '--backend', action='store', default='asyncio.tcp',
        help="select which networking backend to use"
    )
    return parser


def setup_logging(options):
    if options.log_config:
        logging.config.fileConfig(
            options.log_config, disable_existing_loggers=False)
    elif options.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif options.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    # if not options.debug:
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def serve(app, args):
    """
    """
    parser = argparser()
    options = parser.parse_args(args)
    setup_logging(options)
    logger = logging.getLogger('cyrano.serve.serve')
    logger.debug("command line options: %r", options)
    server = backend(options.backend)
    address = '0.0.0.0'
    port = 7777
    logger.info("Serving from %s port %s", address, port)
    server.run(app.new_handler, address, port)


def main():
    import sys
    args = sys.argv[1:]
    from cyrano.demos import echo_chat
    app = echo_chat.EchoChat()
    serve(app, args)

if __name__ == '__main__':
    main()
