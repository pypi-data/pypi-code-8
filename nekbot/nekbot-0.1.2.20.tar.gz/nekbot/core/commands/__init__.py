# coding=utf-8
from collections import defaultdict
from logging import getLogger
import shlex
import traceback
import threading
from nekbot import settings
from nekbot.core.commands.argparse import ArgParse
from nekbot.core.exceptions import PrintableException
from nekbot.utils.decorators import optional_args

__author__ = 'nekmo'

logger = getLogger('nekbot.core.commands')

def get_arguments(body):
    """Dividir una cadena de texto en un listado de argumentos como en un shell.
    """
    return shlex.split(body)

class Command(object):
    symbol = True

    def __init__(self, name=None, function=None, symbol=None, *args):
        self.name = name
        self.function = function
        self.symbol = symbol if symbol is not None else self.symbol
        self.argparse = self.get_argparse(args, function)

    def get_argparse(self, arg_types, function):
        argparse = ArgParse()
        argparse.set_arg_types(arg_types)
        argparse.set_from_function(function)
        # argparse.get_from_function(self.function)
        return argparse

    def execute(self, msg):
        if not hasattr(msg, 'args'):
            msg.args = get_arguments(msg.body)[1:]
        try:
            args = self.argparse.parse(msg.args)
        except Exception as e:
            return msg.short_reply(e)
        try:
            self.control(msg)
        except PrintableException as e:
            return msg.user.send_warning(e)
        try:
            response = self.function(msg, *args)
        except PrintableException as e:
            response = str(e)
        except Exception:
            logger.error(traceback.format_exc())
            msg.user.send_warning('El comando %s no finalizó correctamente.' % repr(self))
            return
        if response is not None:
            msg.reply(response)

    def control(self, msg):
        if hasattr(self.function, 'control'):
             return self.function.control.check(msg)
        if hasattr(self.function, 'command_decorator') and \
                hasattr(self.function.command_decorator, 'control'):
            return self.function.command_decorator.control.check(msg)
        return True

    def __repr__(self):
        if self.symbol:
            return settings.SYMBOL + self.name
        else:
            return self.name


class Commands(defaultdict):
    def __init__(self):
        super(Commands, self).__init__(list)

    def incoming(self, msg):
        if msg.is_from_me:
            return
        if not msg.body.startswith(settings.SYMBOL):
            return
        if msg.historical:
            return
        args = get_arguments(msg.body)
        if not args[0] in self:
            # No es un comando, se ignora
            return
        cmd, args = args[0], args[1:]
        msg.args = args
        for command in self[cmd]:
            l = threading.Thread(target=command.execute, args=(msg,))
            l.start()

    def add_command(self, name, function, *args, **kwargs):
        cmd = Command(name, function, *args, **kwargs)
        self[repr(cmd)].append(cmd)

cmds = Commands()


@optional_args
def command(func, *args, **kwargs):
    return func(*args, **kwargs)


@optional_args
class command:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        if len(args) > 1:
            name = args[1]
        else:
            name = args[0].func_name
        args[0].command_decorator = self
        self.name = name
        cmds.add_command(name, args[0], *args[1:], **kwargs)

    def __repr__(self):
        return '<@Command %s>' % self.name

    def __call__(self, func):
        if hasattr(self, 'control'): print('!!!')
        return func(*self.args, **self.kwargs)