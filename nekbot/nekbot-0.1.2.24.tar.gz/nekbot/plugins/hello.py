from nekbot.core.commands import command, cmds

__author__ = 'nekmo'

@command
def hello(message):
    message.reply('Hello world!')

@command
def ping(message):
    message.reply('Pong.')