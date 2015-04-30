from collections import defaultdict
from nekbot.protocols.base.user import Users

__author__ = 'nekmo'

class GroupChat(object):

    def __init__(self, protocol, name):
        self.users = Users(protocol)
        self.protocol, self.name = protocol, name

    def send_message(self, body):
        raise NotImplementedError("This protocol can't send public messages.")

    @property
    def bot(self):
        raise NotImplementedError('This protocol does not know who I am')

    def __str__(self):
        return self.name

class GroupChats(dict):
    def __init__(self, protocol):
        self.protocol = protocol
        super(GroupChats, self).__init__()
