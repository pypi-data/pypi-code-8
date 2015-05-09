# coding=utf-8
from nekbot.utils.strings import long_message

__author__ = 'nekmo'

class User(object):

    def __init__(self, protocol, username, id=None, groupchat=None):
        self.protocol, self.username, self.groupchat = protocol, username, groupchat
        if not hasattr(self, 'id') and id is not None:
            # id puede ser un método. No queremos entonces sobrescribirlo.
            self.id = id

    def send_message(self, body, notice=False):
        raise NotImplementedError("This protocol can't send messages to users.")

    def send_warning(self, body):
        self.send_message('Warning: %s' % body, not long_message(body))

    def send_error(self, body):
        self.send_message('Error: %s' % body, not long_message(body))

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<%s %s id:%s>' % (self.__class__, self.username, self.id)

    def __str__(self):
        return self.username

    def __eq__(self, other):
        return self.id == other.id

class Users(dict):
    def __init__(self, protocol):
        self.protocol = protocol
        dict.__init__(self)