# coding=utf-8
from logging import getLogger
import logging
from nekbot import settings

from nekbot.core.modular import Modular
from .base.message import Message
from .base.user import User
from .base.group_chat import GroupChat
from .base import Protocol
from nekbot.utils.modules import get_module

if '__path__' in globals():
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

__author__ = 'nekmo'

logger = getLogger('nekbot.protocols')

class Protocols(Modular):
    module_path = 'nekbot.protocols.%s'

    def __init__(self, nekbot, protocols):
        Modular.__init__(self, nekbot, protocols)

    def load_settings(self, protocol):
        try:
            module_settings = get_module('nekbot.protocols.%s.global_settings' % protocol)
        except ImportError:
            logger.debug('%s protocol does not have settings' % protocol)
        else:
            logger.debug('Loaded %s protocol settings' % protocol)
            settings.write_conf(module_settings, True)

    def start(self, protocol):
        self.load_settings(protocol)
        logger.info('Starting %s protocol', protocol)
        Modular.start(self, protocol)