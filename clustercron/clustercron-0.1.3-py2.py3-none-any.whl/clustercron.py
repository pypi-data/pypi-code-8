#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai

'''
Cluster Cron ============
'''

import logging
import sys


# general libary logging
logger = logging.getLogger(__name__)


class Clustercron(object):
    '''
    Main program class.
    Set properties from arguments.
    Runs sub commands in scopes.
    '''

    logger = logging.getLogger('clustercron')

    def __init__(self, args):
        self.args = args
        self.exitcode = 0
        print(self.args)
        # Run sub command in scope
        # getattr(self, self.args.cluster_type)()

    def run_command(self):
        pass


class Optarg(object):
    '''
    Parse command arguments
    Set properties from arguments.
    Runs sub commands in scopes.
    '''
    def __init__(self, arg_list):
        self.arg_list = arg_list
        # Set exitcode 3 for invalid arguments
        self.exitcode = 3
        self.args = {
            'version': False,
            'help': False,
            'verbose': False,
            'dry_run': False,
            'lb_type': None,
            'lb_name': None,
            'command': [],
        }
        self.usage = \
            'usage:  clustercron [options] elb <loadbalancer_name>' \
            ' <cron_command>\n' \
            '        clustercron [options] haproxy <loadbalancer_name>' \
            ' <cron_command>\n\n' \
            'Options:\n' \
            '(-n|--dry-run)   Dry-run, do not run <cron_command>\n' \
            '                 shows where <cron_command> would have ran.\n' \
            '(-v|--verbose)   Verbose output.\n\n' \
            '        clustercron --version\n' \
            '        clustercron (-h|--help)\n'

    def parse(self):
        arg_list = list(self.arg_list)
        arg_list.reverse()
        while arg_list:
            arg = arg_list.pop()
            if arg == '-h' or arg == '--help':
                self.args['help'] = True
                break
            if arg == '--version':
                self.args['version'] = True
                break
            elif arg == '-v' or arg == '--verbose':
                self.args['verbose'] = True
            elif arg == '-n' or arg == '--dry-run':
                self.args['dry_run'] = True
            elif arg in ['haproxy', 'elb']:
                self.args['lb_type'] = arg
                self.args['lb_name'] = arg_list.pop()
                arg_list.reverse()
                self.args['command'] = list(arg_list)
                break
        if self.args['lb_name'] and self.args['lb_name'].startswith('-'):
            self.args['lb_name'] = None
        if self.args['command'] and self.args['command'][0].startswith('-'):
            self.args['command'] = []


def setup_logging(verbose):
    # Set Level for console handler
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    # Set up Console Handler
    handler_console = logging.StreamHandler()
    handler_console.setFormatter(
        logging.Formatter(fmt='%(levelname)-8s %(name)s : %(message)s')
    )
    handler_console.setLevel(log_level)
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    # Add Handlers
    root_logger.addHandler(handler_console)


def version():
    return '0.2.0'


def main():
    '''
    Entry point for the package, as defined in setup.py.
    '''
    # Parse args
    optarg = Optarg(sys.argv[1:])
    optarg.parse()
    if optarg.args['version']:
        print(version())
        exitcode = 1
    elif optarg.args['lb_type'] and optarg.args['lb_name'] and \
            optarg.args['command']:
        # Logging
        setup_logging(optarg.args['verbose'])
        # Args
        logger.debug('Command line arguments: %s', optarg.args)
        exitcode = Clustercron(optarg.args).exitcode
    else:
        print(optarg.usage)
        exitcode = 1
    sys.exit(exitcode)


if __name__ == '__main__':
    main()
