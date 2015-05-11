import logging

import zymbit.config

from zymbit.commands import Command
from zymbit.commands.util import filter_parser_args
from zymbit.tunnel import Tunnel


class TunnelCommand(Command):
    command_name = 'tunnel'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def run(self):
        parser_args = filter_parser_args(self.args)

        self.logger.info('parser_args={}'.format(parser_args))

        tunnel = Tunnel(**parser_args)

        try:
            while True:
                tunnel.check()
        except KeyboardInterrupt:
            tunnel.close()
