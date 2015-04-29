# coding=utf-8
import inspect
from nekbot.core.exceptions import InvalidArgument, PrintableException

__author__ = 'nekmo'

class AllTypes(object):
    pass

ERRORS = {
    ValueError: {
        int: 'El valor debe ser un número.',
        AllTypes: 'Debe ser de tipo {type}',
    },
}

class ArgParse(object):
    def __init__(self):
        self.arg_types = []
        self.kwarg_types = []

    def set_arg_types(self, arg_types):
        self.arg_types = arg_types

    def set_from_function(self, function):
        kwargs_types = inspect.getargspec(function).defaults
        if kwargs_types:
            self.kwarg_types = map(self.get_type, kwargs_types)

    def get_type(self, value):
        if hasattr(value, '__call__'):
            return value
        elif hasattr(value.__class__, '__call__'):
            return value.__class__
        else:
            return str

    def parse_arg(self, type, value, pos=None):
        try:
            if hasattr(type, '__call__'):
                value = type(value)
        except Exception as e:
            if isinstance(e, InvalidArgument):
                # ¡Es una excepción creada por nosotros. Le damos por si lo necesitase
                # información adicional y lo lanzamos tal cual
                e.give_info(value, pos)
                raise e
            err_class = e.__class__
            # No es un tipo de excepción conocida.
            if not ERRORS.get(err_class): raise e
            # Es conocida, pero no tenemos tipo para el mismo, y no hay por defecto
            if not ERRORS[err_class].get(type) and not ERRORS[err_class].get(AllTypes):
                raise e
            # No tenemos tipo para él, pero sí por defecto
            if not ERRORS[err_class].get(type) and ERRORS[err_class].get(AllTypes):
                raise InvalidArgument(ERRORS[err_class][AllTypes], value, pos)
            # ¡Hemos triunfado! Hay para excepción->tipo
            raise InvalidArgument(ERRORS[err_class][type], value, pos)
        return value

    def parse(self, args):
        if len(self.arg_types) > len(args):
            raise PrintableException('Not enough arguments for this command. Missing %i argument%s.' % \
                                      (len(self.arg_types), 's' if len(self.arg_types) > 1 else ''))
        all_types = tuple(self.arg_types) + tuple(self.kwarg_types)
        for i, arg in enumerate(args):
            if len(all_types) <= i: break
            arg = self.parse_arg(all_types[i], arg, i)
            args[i] = arg
        return args