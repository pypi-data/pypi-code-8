# coding=utf-8
from nekbot.core.exceptions import InsufficientPermissions
from nekbot.core.permissions import has_perm

__author__ = 'nekmo'

class Control(object):
    def __init__(self, perm=None, flood=None):
        self.perm = perm

    def check_perms(self, msg):
        if not self.perm: return
        if not has_perm(msg.user, self.perm):
            raise InsufficientPermissions('You need permission %s' % self.perm)

    def check_flood(self, msg):
        pass

    def check(self, msg):
        self.check_perms(msg)
        self.check_flood(msg)

def control(*args, **kwargs):
    """Decorador para añadir restricciones a la ejecución del comando.

    Uso:
        @control(perm='...', flood='...')
        def function():
            pass
    """
    def decorator(f):
        control = Control(*args, **kwargs)
        f.control = control
        return f
    return decorator