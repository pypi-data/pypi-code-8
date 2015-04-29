from nekbot.protocols.base.group_chat import GroupChats

__author__ = 'nekmo'

from nekbot.protocols import GroupChat

class GroupChatTelegram(GroupChat):
    def __init__(self, protocol, name, id):
        GroupChat.__init__(self, protocol, name)
        self.id = id

    def send_message(self, body):
        self.protocol.tg.msg('chat#%i' % self.id, self.protocol.prepare_message(body))

class GroupChatsTelegram(GroupChats):
    pass