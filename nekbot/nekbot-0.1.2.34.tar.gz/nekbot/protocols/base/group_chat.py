from nekbot.protocols.base.send import Send
from nekbot.protocols.base.user import Users

__author__ = 'nekmo'


class GroupChat(Send):
    def __init__(self, protocol, name, group_chat_id=None):
        self.users = Users(protocol)
        self.protocol, self.name, self.id = protocol, name, group_chat_id
        self.init()
        self.protocol.groupchats[str(self)] = self
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

    def get_or_create(self, group_chat_id, name):
        if isinstance(group_chat_id, int):
            group_chat_id = str(group_chat_id)
        if group_chat_id not in self:
            GroupChat(self.protocol, name, group_chat_id)
        return self[group_chat_id]