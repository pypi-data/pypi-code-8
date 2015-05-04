# coding=utf-8
import re
from nekbot.core.exceptions import InvalidArgument
from nekbot.utils.strings import split_arguments

__author__ = 'nekmo'

class ArgParseType(object):
    name = None

    def parse(self, arg, args, msg, position, parser=None):
        return arg

    def set_name(self, name):
        pass

    def match(self, arg, args, msg, position, parser):
        return False

class Text(ArgParseType):
    def __init__(self, min_length=1, max_length=None):
        self.max_length = max_length
        self.min_length = min_length

    def parse(self, arg, args, msg, position, parser=None):
        # Cojo el mensaje original, incluyendo comillas, con los argumentos que quedan
        # hasta el momento
        args.insert(0, arg) # Me han dado como primer argumento parte de la frase. La reintroduzco
        new_args = map(lambda x: '["\']?%s["\']?' % x, args)
        last_body = re.match(".*" + "(%s)$" % ' '.join(new_args), msg.body)
        if not last_body and self.min_length:
            raise InvalidArgument('The argument of type text is required.', last_body, position)
        last_body = last_body.group(1)
        if self.min_length > len(last_body):
            raise InvalidArgument('The text argument type must have at least %i characters.' % self.min_length,
                                  last_body, position)
        if self.max_length is not None:
            try:
                args[:] = split_arguments(last_body[self.max_length:])
            except ValueError:
                raise InvalidArgument('Failed to Divide up the argument of type text.'
                                      'Surely there are unmatched quotes.', last_body[self.max_length:], position)
            last_body = last_body[:self.max_length]
        else:
            # Al no haber límite de caracteres, se toma el resto de la frase. No quedan argumentos.
            args[:] = []
        return last_body

class List(ArgParseType):
    pass

class SetBool(ArgParseType):
    shortcut = ''
    argument = ''
    position = None
    value = None

    def __init__(self, *args):
        if not args:
            return
        i = 0
        for arg_type in [self.set_shortcut, self.set_argument, self.set_value]:
            if i >= len(args):
                break
            try:
                arg_type(args[i])
            except ValueError:
                pass
            finally:
                i += 1

    def set_shortcut(self, shortcut):
        if not isinstance(shortcut, (str, unicode)):
            raise ValueError
        if not re.match('^\-[A-z0-9]', shortcut):
            raise ValueError
        self.shortcut = shortcut

    def set_argument(self, argument):
        if not isinstance(argument, (str, unicode)):
            raise ValueError
        if not argument.startswith('--'):
            raise ValueError
        self.argument = argument

    def set_value(self, value):
        self.value = value

    def set_name(self, name):
        if not self.shortcut:
            self.set_shortcut('-%s' % name[0])
        if not self.argument:
            self.set_argument('--%s' % name.replace('_', '-'))
        self.name = name

    def match(self, arg, args, msg, position, parser):
        if arg not in [self.argument, self.shortcut]:
            return False
        return True

    def get_value(self, kwargs):
        """Obtener el valor a devolver con setBool
        :param kwargs: El kwargs {kwarg: valor} de la función
        :return:
        """
        if self.value is not None:
            return self.value
        value = kwargs[self.name]
        if value in [True, False]:
            return not value

    def parse(self, arg, args, msg, position, parser=None):
        value = self.get_value(parser.kwargs)
        return value