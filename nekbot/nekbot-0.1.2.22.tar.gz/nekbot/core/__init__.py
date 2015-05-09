# coding=utf-8
from logging import getLogger
from time import sleep
import datetime
from nekbot.plugins import Plugins

from .signals import events, event
from nekbot.protocols import Protocols
from nekbot.conf import settings
from . import handlers
from .. import __version__

__author__ = 'nekmo'
logger = getLogger('nekbot')


class NekBot(object):
    version = __version__

    def __init__(self):
        self.protocols = Protocols(self, settings.PROTOCOLS)
        self.plugins = Plugins(self, settings.PLUGINS)
        self.start_datetime = datetime.datetime.now()

    def start(self):
        self.start_protocols()
        self.start_plugins()
        return self

    def start_protocols(self):
        self.protocols.start_all()

    def start_plugins(self):
        self.plugins.start_all()

    def close_protocols(self):
        self.protocols.close()

    def close_plugins(self):
        self.plugins.close()

    def loop(self):
        logger.info('Everything has started')
        while True: sleep(0.2)

    def close(self):
        logger.info('Closing...')
        logger.debug('Closing plugins...')
        self.close_plugins()
        logger.debug('Closing protocols...')
        self.close_protocols()
