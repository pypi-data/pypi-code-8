"""

Useful functions

"""

def import_module(module):
    m = __import__(module)
    for x in module.split('.'):
        m = getattr(m, x)
    return m
