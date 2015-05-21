#!/usr/bin/env python
"""
Unit test the ezlogger library.
"""

def test_import():
    # Assert you can import the library
    import ezlogger
    assert ezlogger

def test_argparse():
    # Assert internal argparse is working
    from ezlogger import initialize_logger, \
                         default_argparse

    logger = initialize_logger(default_argparse(), 'name_of_logging_instance')

    assert logger

    # Assert bypass of internal argparse is working
    args = default_argparse(pre_parse=True)
    logger = initialize_logger(args, 'name_of_logging_instance')

    assert logger

def assert_syslog():
    # Assert gathering of syslog env vars is functional
    from ezlogger import default_argparse, \
                         initialize_logger

    args = default_argparse(pre_parse=True)
    args.syslog = True # This will enable syslogging
    args.syslog_level = 'warning' # This is optional, can be info, warning or error and controls the syslog facility at which to write logs.
    logger = initialize_logger(args, 'name_of_logging_instance', syslog_server='10.20.30.40')

    assert logger

