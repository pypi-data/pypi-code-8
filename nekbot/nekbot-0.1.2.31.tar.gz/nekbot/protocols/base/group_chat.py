from nekbot.protocols.base.send import Send
from nekbot.protocols.base.user import Users

__author__ = 'nekmo'


class GroupChat(Send):
    def __init__(self, protocol, name, groupchat_id=None):
        self.users = Users(protocol)
        self.protocol, self.name, self.id = protocol, name, groupchat_id
        self.init()
        try:
            self.get_users()
        except NotImplementedError:
            pass

    def init(self):
        pass

    def get_users(self, override=True):
        raise NotImplementedError("This protocol can't get users list from groupchat.")

    @property
    def bot(self):
        raise NotImplementedError('This protocol does not know who I am')

    def __str__(self):
        if self.id is not None:
            return str(self.id)
        return self.name


class GroupChats(dict):
    def __init__(self, protocol):
        self.protocol = protocol
        super(GroupChats, self).__init__()
