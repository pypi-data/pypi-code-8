import threading
from nekbot.core import events
from nekbot.protocols.base.user import User
from nekbot.protocols.base.group_chat import GroupChats

__author__ = 'nekmo'


class ProtocolBase(object):
    features = []
    groupchats = None
    _bot = None
    groupchats_class = GroupChats
    user_class = User

    def __init__(self, nekbot):
        self.nekbot = nekbot
        self.get_group_chats()
        self.init()

    def init(self):
        pass

    @property
    def bot(self):
        if self._bot is None:
            self._bot = self.get_bot()
        return self._bot

    @property
    def has_bot(self):
        return self._bot is not None

    def set_bot(self, bot):
        self._bot = bot

    def get_bot(self):
        raise NotImplementedError("This protocol does not have a global user bot.")

    def get_group_chats(self):
        self.groupchats = self.groupchats_class(self)

    def prepare_message(self, body):
        if not isinstance(body, (str, unicode)):
            body = str(body)
        return body

    def send_message(self, id, body, notice=False):
        self.user_class(self, id, id).send_message(body, notice)

    def propagate(self, event, *args, **kwargs):
        events.propagate(event, self, *args, **kwargs)

    def close(self):
        pass


class Protocol(ProtocolBase, threading.Thread):

    def __init__(self, nekbot):
        threading.Thread.__init__(self)
        self.name = self.__class__.__name__.lower()
        self.daemon = True
        ProtocolBase.__init__(self, nekbot)