from nekbot.core import event, events
from nekbot.core.commands import cmds
from nekbot.core.commands.temp import temp_regex_patterns

__author__ = 'nekmo'


@event('message')
def commands_handler(protocol, msg):
    cmds.incoming(msg)

@event('message')
def message_by_protocol(protocol, msg):
    events.propagate('%s.message' % protocol.name, protocol, msg)

@event('message')
def temp_command(protocol, msg):
    temp_regex_patterns.match_message(msg)