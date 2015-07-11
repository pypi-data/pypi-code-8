import reseasdk
from reseasdk.helpers import import_module

def main(args):
    try:
        command = args[0]
    except IndexError:
        command = 'help'

    try:
        m = import_module('reseasdk.commands.{}'.format(command))
    except ImportError:
        reseasdk.error('command not found: {}'.format(command))

    m.main(args[1:])

