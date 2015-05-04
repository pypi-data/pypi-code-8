# coding=utf-8
from inspect import getargspec
from nekbot.utils.iter import append_or_update


def kwargs_function(function):
    argspec = getargspec(function)
    kwarg_names = argspec.args[-len(argspec.defaults):]
    return {kwarg_name: argspec.defaults[i] for i, kwarg_name in enumerate(kwarg_names)}


class InspectFunction(object):
    def __init__(self):
        self.arg_types = []
        self.kwarg_types = []

    def set_arg_types(self, arg_types):
        append_or_update(self.arg_types, arg_types)

    def set_kwarg_types(self, kwarg_types):
        append_or_update(self.kwarg_types, kwarg_types)
    
    def set_from_function(self, function):
        argspec = getargspec(function)
        arg_types, kwargs_types = argspec.args, argspec.defaults
        if kwargs_types:
            append_or_update(self.kwarg_types, map(self.get_type, kwargs_types), False)
        # añado el argumento si no hay para la posición, pero si no no lo modifico
        # Le quito 1 porque el primer argumento es "msg", el objeto Msg
        arg_types = arg_types[:-len(kwargs_types if kwargs_types else [])]
        append_or_update(self.arg_types, [str] * (len(arg_types) - 1), False)

    def get_type(self, value):
        if hasattr(value, '__call__'):
            return value
        elif hasattr(value.__class__, '__call__'):
            return value.__class__
        else:
            return str

    def get_type_name(self, type):
        try:
            return type.__name__
        except Exception:
            return type.__class__.__name__