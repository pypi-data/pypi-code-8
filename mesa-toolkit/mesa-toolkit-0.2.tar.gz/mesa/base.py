import inspect, sys, pkgutil, importlib

class Casa():

 def __init__(self, pkg, hideExceptions=False, interface=None):
  if pkg is None:
   raise Exception
  self.pkg = pkg
  __import__(self.pkg)
  self.package = sys.modules[pkg]
  self.prefix = pkg+'.'
  self._fill_casa()
 
 def _fill_casa(self):
  self.casa = {}
  for importer, modname, ispkg in pkgutil.iter_modules( self.package.__path__, self.prefix):
   module = __import__(modname, locals(), [], -1)
   for name, cls in inspect.getmembers(module):
    if inspect.isclass(cls): # and of type interface
     self.casa[cls.__name__] = cls()

 def rebuild(self):
  for importer, modname, ispkg in pkgutil.iter_modules( self.package.__path__, self.prefix):
   if modname in sys.modules:
    module = sys.modules[modname]
   else:
    module = __import__(modname, locals(), [], -1)
   importlib.reload(module)
  self._fill_casa()

 def _exec(self, name, cls, member):
  module = name.lower()
  full_module = self.pkg + '.' + module
  mod = sys.modules[full_module]
  return getattr(getattr(mod, name), member)(self)

 # run method in each casa member
 def run(self, method):
  for name, cls in self.casa.items():
   self._exec(name, cls, method)

 # yield result of function in each casa member; (name, return value) tuple.
 def generate(self, function):
  for name, cls in self.casa.items():
   yield (name, self._exec(name, cls, function))
