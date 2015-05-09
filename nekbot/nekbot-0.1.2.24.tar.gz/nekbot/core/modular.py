# coding=utf-8
from logging import getLogger
import threading
from nekbot.utils.modules import get_module, get_main_class

__author__ = 'nekmo'

logger = getLogger('nekbot.core.modular')

class Modular(object):
    """Modular es una clase genérica para cargar módulos desde un path e instanciarlos.
    Éste se usa para Protocols y Plugins. El module_path es un string que debe tener un
    '%s'  con el path de donde se obtendrán los módulos. Por ejemplo, 'modules.%s'. Se debe
    proveer un listado con los módulos del directorio que se cargarán (modules_names) y
    éstos serán puestos en self.instances. Intentará buscarse en los módulos una "clase
    principal", con el mismo nombre del módulo, pero con camelcase, y se instanciará en
    self.instances.
    """
    ModularError = Exception
    module_path = None
    fail_on_not_instance = True

    def __init__(self, nekbot, modules_names):
        self.modules = {}  # Módulos, no las instancias.
        self.instances = {}  # Instacia ya iniciada dentro del módulo. Ej. "Telegram"
        self.nekbot = nekbot
        self.modules_names = modules_names
        if self.module_path is None:
            raise self.ModularError('Please, provide a module_path for %s' % self.__class__)

    def get_module(self, module_path):
        return get_module(module_path)

    def start(self, module_name):
        # Obtengo el módulo por el module_name
        module = self.get_module(self.module_path % module_name)
        self.modules[module_name] = module
        instance = None
        try:
            # Busco dentro de dicho módulo la "clase principal", aquella con el mismo nombre del
            # módulo, pero que comienza por mayúscula
            instance = get_main_class(module, module_name)
        except ImportError:
            if self.fail_on_not_instance:
                raise self.ModularError('Module %s has does not have a valid instance' % module_name)
        if instance is not None:
            if not hasattr(self, module_name):
                setattr(self, module_name, instance)
            try:
                instance = instance(self.nekbot)
            except Exception as e:
                logger.error('Instance for "%s" is invalid: %s' % (module_name, e))
            else:
                instance.start()  # Iniciar la instancia
                self.instances[module_name] = instance

    def close(self):
        for instance in self.instances.values():
            if hasattr(instance, 'close'):
                l = threading.Thread(target=instance.close)
                l.start()

    def start_all(self):
        for module_name in self.modules_names:
            self.start(module_name)
