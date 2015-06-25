# -- coding: utf-8 --

# Copyright 2015
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Helps outputting log messages to the console."""

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# -----------------------------------------------------------------------------

import platform

# 3rd Party
from bashutils.bashutils import get_os
from bashutils.colors import color_text
from six.moves import input

# -----------------------------------------------------------------------------
# User feedback
# -----------------------------------------------------------------------------


def divline():
    """Prints a divider line."""
    print("-"*80)


def header(string, logger=None):
    """Prints a header."""
    if logger:
        logger.info(string)

    if get_os() == 'Windows':
        print('==> ' + string)
    else:
        print(color_text('==> ', 'green') + color_text(string, 'white'))


def success(string, logger=None):
    """Prints a success message."""
    if logger:
        logger.info(string)
    if get_os() == 'Windows':
        print('[+] ' + string)
    else:
        print(color_text('[✓] ', 'green') + string)


def error(string, logger=None):
    """Prints a error message."""
    if logger:
        logger.error(string)
    if get_os() == 'Windows':
        print('[x] ' + string)
    else:
        print(color_text('[✗] ', 'magenta') + string)


def warning(string, logger=None):
    """Prints a warning message."""
    if logger:
        logger.warning(string)
    if get_os() == 'Windows':
        print('[!] ' + string)
    else:
        print(color_text('[!] ', 'yellow') + string)


def info(string, logger=None):
    """Prints a info message."""
    if logger:
        logger.info(string)
    if get_os() == 'Windows':
        print('[i] ' + string)
    else:
        print(color_text('[i] ', 'cyan') + string)


def declined(string):
    """Prints a declined message."""
    print(color_text('[✗] ', 'magenta') + color_text(string, 'cyan') +
          color_text(' declined. ') + color_text('Skipping...', 'green'))


# For backwards compatibility as we renamed our methods
log_divline = divline
log_header = header
log_success = success
log_error = error
log_warning = warning
log_info = info
log_declined = declined

# -----------------------------------------------------------------------------
# User Input
# -----------------------------------------------------------------------------


def prompt(question):
    """Prompts user for input."""
    # Python 2to3 compatbility
    response = input(color_text('[?] ', 'yellow') +
                     color_text(question, 'cyan') + ' ')
    return response


def confirm(question):
    """Prompts user to confirm with (y/n)."""
    # Python 2to3 compatbility
    response = input(color_text('[?] ', 'yellow') +
                     color_text(question, 'cyan') + '? (y/n) ')

    if response in ['y', 'yes']:
        return True
    else:
        declined(question)
        return False

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    divline()
    header('header')
    success('success')
    error('error')
    warning('warning')
    info('info')
    declined('something')

    print(prompt('What is your name?'))

    if confirm('Confirm this'):
        print('You confirmed!')
