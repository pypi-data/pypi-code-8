#!/usr/bin/env python
"""
Python based logging module that when imported and called is
capable of logging both stdout,stderr and redirect to local
logging directory.  The local logging directory can either be
$HOME/logs/%TIMESTAMP%SCRIPTNAME%.log or a user specified
path/file.
"""
__author__ = "Gary Wright<zerosignal0@msn.com>"
__contributors__ = ["Gary Wright"]
__version__ = "1.0.0"
__maintainer__ = "Gary Wright"


import datetime
import time
import logging
import logging.handlers
import os
import sys
import argparse
import inspect
import getpass
import random

from rainbow_logging_handler import RainbowLoggingHandler #<- Third party module

# Globals
LOGGER = None #Setup default global
FORMATTER = None #Setup default global

def linenum():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def create_log_dir():
    """Determines users homedir and creates logging directory
       if it doesn't already exist."""
    logdir = os.path.join(os.path.expanduser('~'),'logs')

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    return logdir

def default_argparse(pre_parse=True, description=None):
    """Creates argparse for logging mechanism"""

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-l',
                        '--log',
                        action="store",
                        default='info',
                        type=str,
                        nargs='?',
                        help="Specify the logging level you would like to display to STDOUT\
                         for this execution (Default is INFO).\
                         Choices are debug,info,warning,error.")
    parser.add_argument('-ld',
                        '--log_dir',
                        action="store",
                        default='',
                        type=str,
                        nargs='?',
                        help="Specify the logging directory to have logging files be stored. (Default is $HOME/logs/)")
    parser.add_argument('-lr',
                        '--logfile_rotate',
                        action="store_true",
                        help="Specify whether you wish for your log files to auto-rotate daily.  This will create a new logfile at UTC 00:00:00 and continue logging.")
    parser.add_argument('-ls',
                        '--logsize',
                        action="store",
                        default=0,
                        type=int,
                        nargs='?',
                        help="(Optional) Specify the max logfile size (in MB) you would like to use for automatic logfile rotation.  *NOTE -lr must be selected for this to take affect.")
    parser.add_argument('-sl',
                        '--syslog',
                        action="store_true",
                        help="Specify whether you wish to emit to syslog servers. Specification of the syslog is made with initalize_logger kwarg 'syslog_server'")
    parser.add_argument('-sll',
                        '--syslog_level',
                        action="store",
                        default='error',
                        choices=['error', 'info', 'warning'],
                        type=str,
                        nargs='?',
                        help="If the -sl flag has been specified, you can specify the logging level in which will emit syslogs (By default this level is 'error').  Logging levels you have to choose from are ('info', 'warning', 'error'). *NOTE DEBUG is NOT allowed.")


    if pre_parse:
        return parser.parse_args()
    else:
        return parser

def contains(str, set):
    """Check whether 'str' contains ALL of the chars in 'set'"""
    return 0 not in [c in str for c in set]


class SizedTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None,
                 delay=0, when='midnight', interval=1, utc=True):
        """
        If rotation/rollover is wanted, it doesn't make sense to use another
        mode. If for example 'w' were specified, then if there were multiple
        runs of the calling application, the logs from previous runs would be
        lost if the 'w' is respected, because the log file would be truncated
        on each run.
        """
        logging.handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes


    def shouldRollover(self, record):
        """
        Determine if logfile rollover is necessary.  This funciton will essentially
        determine if the supplied record would cause the file to exceed
        the size threshold in MB that has been configured.
        """
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0


def initialize_logger(args, script_name, syslog_server=None):
    """
    Initialize the logging instance with the values provided
    by the user and return the logging object.

    """
    LOGGER = logging.getLogger(script_name)

    FORMATTER = logging.Formatter(
        ""+script_name+" : "+str(getpass.getuser())+" : %(asctime)s : %(levelname)s : %(message)s",
                                  datefmt='%m/%d/%Y %I:%M:%S %p')

    # create console handler and set level to info
    logging.StreamHandler()

    # setup `RainbowLoggingHandler`
    handler = RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'white', True))
    handler.setFormatter(FORMATTER)
    LOGGER.addHandler(handler)

    # setup log level from arguments
    if args.log:
        if contains('DEBUG', args.log.upper()):
            handler.setLevel(logging.DEBUG)
            LOGGER.setLevel(logging.DEBUG)
        elif contains('WARNING', args.log.upper()):
            handler.setLevel(logging.WARNING)
            LOGGER.setLevel(logging.WARNING)
        elif contains('ERROR', args.log.upper()):
            handler.setLevel(logging.ERROR)
            LOGGER.setLevel(logging.ERROR)
        else:
            handler.setLevel(logging.INFO)
            LOGGER.setLevel(logging.INFO)
        LOGGER.info('Logging level has been set to {}'.format(args.log.upper()))

    # setup logging directory to store log files
    if args.log_dir:

        if not os.path.isdir(args.log_dir):
            os.makedirs(args.log_dir)
        output_dir = args.log_dir

    else:
        output_dir = create_log_dir()

    LOGGER.info('Logging directory has been set to {}'.format(output_dir))


    # create optional syslog handler, if the argument has been supplied to support it
    if args.syslog:

        DESIG_SYSLOG_SERVER = syslog_server

        handler = logging.handlers.SysLogHandler(address=(DESIG_SYSLOG_SERVER,
                                                          logging.handlers.SYSLOG_UDP_PORT))
        syslog_format = logging.Formatter(
            '[appname]: %(name)s: [alias]: '+str(getpass.getuser())+' %(message)s')
        handler.setFormatter(syslog_format)

        if args.syslog_level:
            # Set syslog level to the user specified level
            if args.syslog_level == 'info':
                handler.setLevel(logging.INFO)
            elif args.syslog_level == 'warning':
                handler.setLevel(logging.WARNING)
            elif args.syslog_level == 'error':
                handler.setLevel(logging.ERROR)

        LOGGER.info(
            'Syslog has been enabled for [{}] logging level, sent to syslog server [{}]'.format(
                                                                            args.syslog_level,
                                                                            DESIG_SYSLOG_SERVER))

        # Add syslog handler to logging object
        LOGGER.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(
        output_dir, "error.log"),"a", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    handler.setFormatter(FORMATTER)
    LOGGER.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "all.log"),"a")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(FORMATTER)
    LOGGER.addHandler(handler)

    if args.logfile_rotate:
        '''
        User has specified they would like to create a daily rotating logfile.
        Create an instance and DO NOT create a single serving logfile.
        '''
        LOGGER.info('Logfiles are now set to auto-rotate at midnight UTC.')
        filepath_and_name_format = ('{}/{}'.format(output_dir, script_name.replace('.py','')))
        LOGGER.info('Logfiles are now being written at {}'.format(filepath_and_name_format))

        log_filename=filepath_and_name_format
        # maxBytes takes the max file size in MB and bit-shift converts to bytes
        handler=SizedTimedRotatingFileHandler(
            log_filename, maxBytes=args.logsize<<20)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(FORMATTER)
        handler.suffix = "%Y-%m-%d.log"
        LOGGER.addHandler(handler)

    else:
        # create individual execution file handler and set level to debug
        now = datetime.datetime.now()
        datetime_stamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        datetime_stamp = ('{}_{}.log'.format(datetime_stamp, script_name.replace('.py','')))
        filename = os.path.join(output_dir, datetime_stamp)

        handler = logging.FileHandler(filename, "a")

        if contains('DEBUG', args.log.upper()):
            handler.setLevel(logging.DEBUG)
        elif contains('WARNING', args.log.upper()):
            handler.setLevel(logging.WARNING)
        elif contains('ERROR', args.log.upper()):
            handler.setLevel(logging.ERROR)
        else:
            handler.setLevel(logging.INFO)

        handler.setFormatter(FORMATTER)
        LOGGER.addHandler(handler)

        # display the exact file name / path to the user
        LOGGER.info('Logs for this session now being written to {}'.format(filename))

        # Attach filepath / filename string to logger
        LOGGER.filename = filename

    return LOGGER
