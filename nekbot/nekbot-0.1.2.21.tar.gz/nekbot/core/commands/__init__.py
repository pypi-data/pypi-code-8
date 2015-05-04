# coding=utf-8
from collections import defaultdict
from logging import getLogger
import traceback
import threading
import re

from nekbot import settings
from nekbot.core.commands.argparse import ArgParse
from nekbot.core.commands.doc import Doc
from nekbot.core.exceptions import PrintableException
from nekbot.utils.decorators import optional_args
from nekbot.utils.strings import split_arguments, highlight_occurrence, limit_context


__author__ = 'nekmo'

logger = getLogger('nekbot.core.commands')


class Command(object):
    symbol = True
    _doc = None

    def __init__(self, name=None, function=None, symbol=None, *args, **kwargs):
        self.name = name
        self.function = function
        self.symbol = symbol if symbol is not None else self.symbol
        self.argparse = self.get_argparse(args, kwargs, function)
        self._args = args
        self._kwargs = kwargs # TODO el orden es importante

    def get_argparse(self, arg_types, kwargs, function):
        argparse = ArgParse()
        argparse.set_arg_types(arg_types)
        argparse.set_from_function(function)
        argparse.set_kwargs(kwargs, function)
        # argparse.get_from_function(self.function)
        return argparse

    def get_doc(self):
        doc = Doc(self.name, repr(self))
        doc.set_arg_types(self._args)
        doc.set_from_function(self.function)
        self._doc = doc
        return doc

    @property
    def doc(self):
        if self._doc is not None: return self._doc
        self._doc = str(self.get_doc())
        return self._doc

    def execute(self, msg):
        if not hasattr(msg, 'args'):
            msg.args = split_arguments(msg.body)[1:]
        if '--help' in msg.args or '-h' in msg.args:
            # Return documentation.
            msg.reply(str(self.get_doc()))
            return
        try:
            args = self.argparse.parse(msg.args, msg)
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
        args = split_arguments(msg.body)
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

    def search(self, term):
        results_cmd = []
        results_doc = []
        for cmd_repr in self.keys():
            if not term in cmd_repr:
                continue
            results_cmd.append("%s (%s)" % (cmd_repr, highlight_occurrence(cmd_repr, term)))
        for command_list in self.values():
            for command in command_list:
                if not term in command.doc:
                    continue
                context = limit_context(term, command.doc)
                print(context)
                results_doc.append("%s (%s)" % (
                    repr(command), highlight_occurrence(context, term)
                ))
        return results_cmd, results_doc


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