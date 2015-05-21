#!/usr/bin/env python
"""
Unit test the ezlogger library.
"""
import os
import sys

# Append parent directory in order to access the configuration files from the parent dir.
CUR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR_PATH = os.path.abspath(os.path.join(CUR_DIR_PATH, os.pardir))

sys.path.append(os.path.join(PARENT_DIR_PATH, 'ezlogger'))

def test_import():
    # Assert you can import the library
    import ezlogger
    assert ezlogger

def test_argparse():
    # Assert internal argparse is working
    import ezlogger

    logger = initialize_logger(default_argparse(), 'name_of_logging_instance')

    assert logger

    # Assert bypass of internal argparse is working
    args = ezlogger.default_argparse(pre_parse=True)
    logger = initialize_logger(args, 'name_of_logging_instance')

    assert logger

def assert_syslog():
    # Assert gathering of syslog env vars is functional
    import ezlogger

    args = ezlogger.default_argparse(pre_parse=True)
    args.syslog = True # This will enable syslogging
    args.syslog_level = 'warning' # This is optional, can be info, warning or error and controls the syslog facility at which to write logs.
    logger = ezlogger.initialize_logger(args, 'name_of_logging_instance', syslog_server='10.20.30.40')

    assert logger

