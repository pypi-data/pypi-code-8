import os
import logging

import click

from . import settings
from machinepack.print_helpers import print_banner


CONSOLE_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(CONSOLE_FORMATTER)

LOGGER = logging.getLogger('machinepack')
LOGGER.addHandler(CONSOLE_HANDLER)


# def set_loglevel(ctx, param, value):
# value = value.upper()
#     loglevel = getattr(logging, value, None)
#
#     if not isinstance(loglevel, int):
#         raise click.BadParameter('Invalid log level: {0}.'.format(loglevel))
#
#     logger.setLevel(loglevel)
#     return value


class AutodiscoverMultiCommand(click.MultiCommand):
    def list_commands(self, ctx):

        # printing banner
        print_banner()

        commands_list = []
        for filename in os.listdir(settings.COMMANDS_FOLDER):
            if filename.endswith('.py') and not filename.startswith('_'):
                commands_list.append(filename[:-3])

        commands_list.extend(settings.ALIASES.keys())
        commands_list.sort()

        return commands_list

    def get_command(self, ctx, name):

        command = 'cli'

        # if name in settings.ALIASES:
        #     alias = settings.ALIASES[name]
        #     name, command = alias.rsplit('.', 1)

        try:
            module_name = 'machinepack.commands.{0}'.format(name)
            module = __import__(module_name, None, None, [command])
        except ImportError:
            return

        LOGGER.debug('Command loaded: {0}'.format(module))
        return getattr(module, command)
