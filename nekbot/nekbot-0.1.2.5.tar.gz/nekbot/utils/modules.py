# coding=utf-8
__author__ = 'nekmo'

def get_module(path):
    try:
        return __import__(path, globals(), locals(), [path.split('.')[-1]])
    except ImportError:
        # Puede ser un método  o propiedad
        module = '.'.join(path.split('.')[:-1])
        module = __import__(module, globals(), locals(), [module.split('.')[-1]])
        return getattr(module, path.split('.')[-1])

def get_main_class(module, name):
    if hasattr(module, name.capitalize()):
        instance = getattr(module, name.capitalize())
    else:
        raise ImportError
    return instance
