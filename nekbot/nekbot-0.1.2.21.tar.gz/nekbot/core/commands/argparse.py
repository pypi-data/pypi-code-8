# coding=utf-8
import inspect
from nekbot.core.exceptions import InvalidArgument, PrintableException
from nekbot.core.types.argparse import ArgParseType
from nekbot.utils.iter import append_or_update
from nekbot.utils.survey import InspectFunction, kwargs_function

__author__ = 'nekmo'


class AllTypes(object):
    pass


ERRORS = {
    ValueError: {
        int: 'El valor debe ser un número.',
        AllTypes: 'Debe ser de tipo {type}',
    },
}


class ArgParse(InspectFunction):
    def __init__(self):
        super(ArgParse, self).__init__()
        self.special_kwargs = [] # Kwargs que pueden encontrarse en cualquier parte del boy
        self.kwarg_values = []
        self.kwags = {} # {nombre: valor por defecto en función}

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

    def set_kwargs(self, kwargs, function):
        """Esta función (a la cual se le entrega un diccionario de kwargs) debe ser utilizada
        después de set_from_function
        """
        argspec = inspect.getargspec(function)
        if not argspec.defaults:
            return # No hay kwargs
        kwarg_names = argspec.args[-len(argspec.defaults):]
        self.kwarg_values = argspec.defaults
        for key, arg_type in kwargs.items():
            try:
                index = kwarg_names.index(key)
            except ValueError:
                continue
            if index > len(self.kwarg_types):
                continue
            if inspect.isclass(arg_type) and issubclass(arg_type, ArgParseType):
                # Es la clase sin instanciar de ArgParseType. Se instancia
                arg_type = arg_type()
            if isinstance(arg_type, ArgParseType):
                arg_type.set_name(key)
                # Si el index es la posición de este elemento dentro de los kwargs, el position
                # es la posición del mismo juntando args y kwargs. Esto sirve para luego a la
                # hora de construir el listado con los argumentos a entregar a la función, el
                # kwarg especial esté en la posición correcta.
                # Hago -1 por el primer argumento (msg)
                arg_type.position = index + (len(argspec.args) - len(argspec.defaults) - 1)
                self.special_kwargs.append(arg_type)
            self.kwarg_types[index] = arg_type
        self.kwargs = kwargs_function(function)

    def parse(self, args, msg=None):
        if len(self.arg_types) > len(args):
            raise PrintableException('Not enough arguments for this command. Missing %i argument%s.' %
                                     (len(self.arg_types), 's' if len(self.arg_types) > 1 else ''))
        args = list(args)  # Listado de argumentos que me han entregado
        final_args = []
        final_kwargs = {}
        all_types = list(self.arg_types) + list(self.kwarg_types)  # Todos los tipos conocidos
        i = 0  # Argumento posicional
        while True:
            if not args:
                break
            word_now = args.pop(0)  # Tomo el elemento que me toca ahora
            type_now = None
            # Los argumentos especiales son kwargs (normalmente con forma --arg), que pueden aparecer
            # en cualquier parte del mensaje. Se mira si la palabra actual es uno de estos.
            for special_kwarg in self.special_kwargs:
                if not special_kwarg.match(word_now, args, msg, i, self):
                    continue
                type_now = special_kwarg
                final_kwargs[type_now.position] = (type_now.parse(word_now, args, msg, i, self))
                break
            if type_now is not None:
                # Ya se ha obtenido este argumento por un argumento kwarg especial
                continue
            if all_types:
                type_now = all_types.pop(0)  # Tomo el tipo que me toca ahora
            else:
                type_now = str  # No hay más tipos disponibles. Uso str por defecto
            if inspect.isclass(type_now) and issubclass(type_now, ArgParseType):
                # Es la clase sin instanciar de ArgParseType. Se instancia
                type_now = type_now()
            if not isinstance(type_now, ArgParseType):
                arg = self.parse_arg(type_now, word_now, i)
            else:
                arg = type_now.parse(word_now, args, msg, i, self)
            final_args.append(arg)
            i += 1
        # En el final args, pondré también los valores por defecto de los kwargs, para poder
        # sobrescribirlos con los valores que pudiesen haberse establecido por Special types,
        # en la posición que necesitan
        final_args += self.kwarg_values[-(len(self.arg_types) + len(self.kwarg_values) - len(final_args)):]
        for position, value in final_kwargs.items():
            final_args[position] = value
        return final_args