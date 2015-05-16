import inspect, sys, pkgutil, importlib

class Casa():

    def __init__(self, pkg, hideExceptions=False, interface=None):
        if pkg is None:
            raise Exception
        self.pkg = pkg
        __import__(self.pkg)
        self.package = sys.modules[pkg]
        self.prefix = pkg+'.'
        self.casa = {}
        self._fill_casa()
    
    def _fill_casa(self):
        for importer, modname, ispkg in pkgutil.iter_modules( self.package.__path__, self.prefix):
            module = __import__(modname, locals(), [], -1)
            for name, cls in inspect.getmembers(module):
                if inspect.isclass(cls): # and of type interface
                    self.casa[cls.__name__] = cls()

    def rebuild(self):
        importlib.reload(pkg)
        self._fill_casa()

    def run(self, method):
        for name, cls in self.casa.items():
            module = name.lower()
            full_module = self.pkg + '.' + module
            mod = sys.modules[full_module]
            getattr(getattr(mod, name), method)(self)

    def generate(self, function):
        pass
