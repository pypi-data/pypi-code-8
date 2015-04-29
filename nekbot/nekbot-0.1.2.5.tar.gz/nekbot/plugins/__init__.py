# coding=utf-8
from logging import getLogger
from nekbot.core.modular import Modular
from nekbot.utils.modules import get_module

logger = getLogger('nekbot.plugins')

if '__path__' in globals():
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

class Plugins(Modular):
    module_path = 'plugins.%s'
    fail_on_not_instance = False

    def __init__(self, nekbot, protocols):
        Modular.__init__(self, nekbot, protocols)

    def get_module(self, module_path):
        """Probar primero a cargar el módulo desde el directorio plugins
        del proyecto. Si no funciona, cargarlo desde NekBot.
        """
        try:
            return get_module(module_path)
        except ImportError:
            return get_module('nekbot.' + module_path)

    def start(self, protocol):
        logger.info('Loading %s plugin', protocol)
        Modular.start(self, protocol)