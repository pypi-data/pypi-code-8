#!/usr/local/bin/python
# coding: utf-8

# -----------------------------------------------------------------------------

# 3rd Party
from colors import *

# -----------------------------------------------------------------------------
# User feedback
# -----------------------------------------------------------------------------


def log_divline():
    print("-"*80)


def log_header(string):
    print(color_text('==> ', 'green') + color_text(string, 'white'))


def log_success(string):
    print(color_text('[✓] ', 'green') + string)


def log_error(string):
    print(color_text('[✗] ', 'magenta') + string)


def log_warning(string):
    print(color_text('[!] ', 'yellow') + string)


def log_info(string):
    print(color_text('[i] ', 'cyan') + string)


def log_declined(string):
    print(color_text('[✗] ', 'magenta') + color_text(string, 'cyan') +
          color_text(' declined. ') + color_text('Skipping...', 'green'))

# -----------------------------------------------------------------------------
# User Input
# -----------------------------------------------------------------------------


def prompt(question):
    try:  # python 2.x
        response = raw_input(color_text('[?] ', 'yellow') +
                             color_text(question, 'cyan') + ' ')
    except NameError:  # python 3.x
        response = input(color_text('[?] ', 'yellow') +
                         color_text(question, 'cyan') + ' ')
    return response


def confirm(question):
    try:  # python 2.x
        response = raw_input(color_text('[?] ', 'yellow') +
                             color_text(question, 'cyan') + '? (y/n) ')
    except NameError:  # python 3.x
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

    answer = prompt('What is your name?')
    print(answer)

    if confirm('Confirm this'):
        print('You confirmed!')
