# -*- coding: utf-8 -*-

import os
import sys
import logging
import logging.handlers


def expand_dir(*args):
    """..."""
    path = os.path.expanduser('~/.voicecom')
    if not os.path.isdir(path):
        os.mkdir(path)
    for expansion in args[:-1]:
        path = os.path.join(path, expansion)
        if not os.path.isdir(path):
            os.mkdir(path)
    return os.path.join(path, args[-1])


def setup_logging():
    """Setup logging for console and logfile output."""
    root_logger = logging.getLogger()
    console = logging.StreamHandler(sys.stdout)
    console_fmt = logging.Formatter('[%(levelname)s] %(message)s')
    console.setFormatter(console_fmt)

    if '-v' in sys.argv:
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.INFO)

    # Setup logging for file output.
    log_path = expand_dir('logs', 'unnamed.log')
    do_rollover = os.path.isfile(log_path)
    logfile = logging.handlers.RotatingFileHandler(log_path, backupCount=5)
    if do_rollover:
        logfile.doRollover()
    logfile.setLevel(logging.DEBUG)
    logfile_fmt = logging.Formatter(
        '[%(asctime)s:%(msecs).03d][%(levelname)s][%(name)s:%(lineno)d]'
        ' %(message)s', '%Y.%m.%d-%H.%M.%S')
    logfile.setFormatter(logfile_fmt)

    # Initiate main logger.
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console)
    root_logger.addHandler(logfile)
