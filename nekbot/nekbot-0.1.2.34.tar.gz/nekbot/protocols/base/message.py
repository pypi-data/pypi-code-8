# coding=utf-8
import warnings
from nekbot.protocols.base.event import Event
from nekbot.protocols.base.send import MessageSend


__author__ = 'nekmo'


class Message(Event, MessageSend):
    event_name = 'message'
    historical = False
    _groupchat = None

    def __init__(self, protocol, body, user, groupchat=None):
        """Un nuevo mensaje entrante
            :param protocol: Instancia del protocol
            :param body: String con el mensaje recibido.
            :param user: Instancia de User del usuario que envía el mensaje.
            :param groupchat: Instancia de GroupChat
            """
        super(Message, self).__init__(protocol)
        self.body, self.user = body, user
        self._groupchat = groupchat
        self.init()

    def init(self):
        pass

    def reply(self, body, notice=False):
        if notice and 'notice' in self.protocol.features:
            self.user.send_message(body, True)
        elif self.is_groupchat and self.is_public:
            self.groupchat.send_message(body)
        else:
            self.user.send_message(body)

    def get_group_chat_id(self):
        raise NotImplementedError("This protocol doesn't support get_group_chat_id.")

    def create_group_chat(self):
        raise NotImplementedError("This protocol can not create the object GroupChat from the message room.")

    def get_group_chat(self):
        groupchat_id = self.get_group_chat_id()
        if groupchat_id not in self.protocol.groupchats:
            self.create_group_chat()
        return self.protocol.groupchats[self.get_group_chat_id()]

    @property
    def groupchat(self):
        if not self._groupchat and self.is_groupchat:
            groupchat_id = self.get_group_chat_id()
            if groupchat_id not in self.protocol.groupchats:
                self.get_group_chat()
            self._groupchat = self.protocol.groupchats[groupchat_id]
        return self._groupchat

    @property
    def is_own(self):
        if self.user.id:
            prop = 'id'
        else:
            prop = 'username'
        if self.is_groupchat:
            return getattr(self.groupchat.bot, prop) == getattr(self.user.username, prop)
        else:
            return getattr(self.protocol.bot, prop) == getattr(self.user, prop)

    @property
    def is_from_me(self):
        warnings.warn("Use is_own instead is_from_me.", DeprecationWarning)
        return self.is_own

    @property
    def is_groupchat(self):
        raise NotImplementedError("This protocol doesn't know if the message is from a groupchat.")

    @property
    def is_public(self):
        raise NotImplementedError("This protocol doesn't know if the message is public.")

    @property
    def is_private(self):
        raise NotImplementedError("This protocol doesn't know if the message is private.")

    def _copy(self):
        return self.__class__(self.protocol, self.body, self.user, self.groupchat)

    def copy(self):
        return self._copy()

    def __str__(self):
        return self.body