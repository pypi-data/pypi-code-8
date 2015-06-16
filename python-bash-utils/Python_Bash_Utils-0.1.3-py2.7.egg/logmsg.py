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

# 3rd Party
from bashutils.colors import color_text
from six.moves import input

# -----------------------------------------------------------------------------
# User feedback
# -----------------------------------------------------------------------------


def log_divline():
    """Prints a divider line."""
    print("-"*80)


def log_header(string):
    """Prints a header."""
    print(color_text('==> ', 'green') + color_text(string, 'white'))


def log_success(string):
    """Prints a success message."""
    print(color_text('[✓] ', 'green') + string)


def log_error(string):
    """Prints a error message."""
    print(color_text('[✗] ', 'magenta') + string)


def log_warning(string):
    """Prints a warning message."""
    print(color_text('[!] ', 'yellow') + string)


def log_info(string):
    """Prints a info message."""
    print(color_text('[i] ', 'cyan') + string)


def log_declined(string):
    """Prints a declined message."""
    print(color_text('[✗] ', 'magenta') + color_text(string, 'cyan') +
          color_text(' declined. ') + color_text('Skipping...', 'green'))

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
        log_declined(question)
        return False

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    log_divline()
    log_header('header')
    log_success('success')
    log_error('error')
    log_warning('warning')
    log_info('info')
    log_declined('something')

    print(prompt('What is your name?'))

    if confirm('Confirm this'):
        print('You confirmed!')
