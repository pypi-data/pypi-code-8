# coding=utf-8
from nekbot.protocols.base.send import Send

__author__ = 'nekmo'


class User(Send):

    def __init__(self, protocol, username, id=None, groupchat=None):
        self.protocol, self.username, self.groupchat = protocol, username, groupchat
        if not hasattr(self, 'id') and id is not None:
            # id puede ser un método. No queremos entonces sobrescribirlo.
            self.id = id
        self.init()

    def init(self):
        pass

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<%s %s id:%s>' % (self.__class__.__name__, self.username, self.id)

    def __str__(self):
        return self.username

    def __eq__(self, other):
        return self.id == other.id


class Users(dict):
    def __init__(self, protocol):
        self.protocol = protocol
        dict.__init__(self)

