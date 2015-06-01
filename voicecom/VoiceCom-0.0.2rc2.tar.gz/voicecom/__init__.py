#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import logging
import logging.handlers

from voicecom import paths

__version__ = '0.0.2rc2'

_log = logging.getLogger(__name__)


def main():
    """Main VoiceCom routine.

    Returns 0 if everything went as expected, otherwise non-zero.
    """
    # Initiate root logger.
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Setup for console output
    console = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(console)
    console_fmt = logging.Formatter('[%(levelname)s] %(message)s')
    console.setFormatter(console_fmt)
    console.setLevel(logging.INFO)

    # Setup for file output.
    log_path = paths.expand_path('logs', 'unnamed.log')
    do_rollover = os.path.isfile(log_path)
    logfile = logging.handlers.RotatingFileHandler(log_path, backupCount=9)
    if do_rollover:
        logfile.doRollover()
    logfile.setLevel(logging.DEBUG)
    logfile_fmt = logging.Formatter(
        '[%(asctime)s:%(msecs).03d][%(levelname)s][%(name)s:%(lineno)d]'
        ' %(message)s', '%Y.%m.%d-%H.%M.%S')
    logfile.setFormatter(logfile_fmt)
    root_logger.addHandler(logfile)

    # Logging setup done, initialize the rest of the system.
    _log.info('Initializing system.')

    return 0


def run():
    """Runs VoiceCom and exists after completion.

    Catches every Exception and logs it. The exit-code is 0 if
    everything went as expected, otherwise non-zero.
    """
    try:
        sys.exit(main())
    except Exception:
        _log.critical('System failure.', exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(run())
