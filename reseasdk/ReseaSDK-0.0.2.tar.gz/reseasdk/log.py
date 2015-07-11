import sys
from termcolor import colored, cprint


def error(msg):
    """ Prints an error message and terminate the program. """
    sys.exit(colored('Resea SDK: {}'.format(msg), 'red'))


def info(msg):
    """ Prints an informational message. """
    cprint(msg, 'blue')


def _generating(cmd, target):
    """ Returns log message for generating something."""

    return '  {}{}{}'.format(colored(cmd, 'magenta'),
                             (' ' * (16-len(cmd))),
                             target)


def generating(cmd, target):
    """ Prints a 'GEN somthing' message. """
    print(_generating(cmd, target))
