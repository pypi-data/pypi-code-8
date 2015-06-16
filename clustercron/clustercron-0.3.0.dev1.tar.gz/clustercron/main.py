# clustercron/clustercron.py
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# -*- coding: utf-8 -*-

'''
clustercron.main
----------------------
'''


from __future__ import unicode_literals
from __future__ import print_function

import logging
import sys
import subprocess
from . import __version__
from . import elb


# general libary logging
logger = logging.getLogger(__name__)


def clustercron(lb_type, lb_name, command):
    '''
    API clustercron

    :param lb_type: Type of loadbalancer
    :param lb_name: Name of the loadbalancer instance
    :param command:  command as a list
    '''
    if lb_type == 'elb':
        lb = elb.Elb(lb_type)
        if lb.master:
            if command:
                logger.debug('run command: %s', ' '.join(command))
                proc = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = proc.communicate()
                logger.debug('stdout: %s', stdout)
                logger.debug('stderr: %s', stderr)
                logger.debug('returncode: %d', proc.returncode)
                return proc.returncode
            else:
                return 0
        else:
            return 1


class Optarg(object):
    '''
    Parse arguments from `sys.argv[0]` list.
    Set usage string.
    Set properties from arguments.
    '''
    def __init__(self, arg_list):
        self.arg_list = arg_list
        self.args = {
            'version': False,
            'help': False,
            'verbose': False,
            'lb_type': None,
            'lb_name': None,
            'command': [],
        }
        self.usage = '''usage:
   clustercron [(-v|--verbose)] elb <loadbalancer_name> [<cron_command>]
   clustercron --version
   clustercron (-h|--help)

Clustercron is cronjob wrapper that tries to ensure that a script gets run
only once, on one host from a pool of nodes of a specified loadbalancer.

Without specifying a <cron_command> clustercron will only check if the node
is the `master` in the cluster and will return 0 if so.
'''

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
            if arg == '-v' or arg == '--verbose':
                self.args['verbose'] = True
            if arg == 'elb':
                self.args['lb_type'] = arg
                try:
                    self.args['lb_name'] = arg_list.pop()
                except IndexError:
                    pass
                arg_list.reverse()
                self.args['command'] = list(arg_list)
                break
        if self.args['lb_name'] and self.args['lb_name'].startswith('-'):
            self.args['lb_name'] = None
        if self.args['command'] and self.args['command'][0].startswith('-'):
            self.args['command'] = []


def setup_logging(verbose):
    '''
    Sets up logging.
    '''
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    handler_console = logging.StreamHandler()
    handler_console.setFormatter(
        logging.Formatter(fmt='%(levelname)-8s %(name)s : %(message)s')
    )
    handler_console.setLevel(log_level)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler_console)


def command():
    '''
    Entry point for the package, as defined in setup.py.
    '''
    optarg = Optarg(sys.argv[1:])
    optarg.parse()
    if optarg.args['version']:
        print(__version__)
        exitcode = 2
    elif optarg.args['lb_type'] and optarg.args['lb_name']:
        setup_logging(optarg.args['verbose'])
        logger.debug('Command line arguments: %s', optarg.args)
        exitcode = clustercron(
            optarg.args['lb_type'],
            optarg.args['lb_name'],
            optarg.args['command'],
        )
    else:
        print(optarg.usage)
        exitcode = 3
    return exitcode
