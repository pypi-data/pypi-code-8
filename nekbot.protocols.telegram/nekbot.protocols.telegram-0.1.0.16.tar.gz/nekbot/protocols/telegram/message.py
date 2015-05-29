import warnings
from logging import getLogger
from nekbot.protocols.telegram.group_chat import GroupChatTelegram
from nekbot.protocols.telegram.user import UserTelegram
from nekbot.protocols import Message

__author__ = 'nekmo'

logger = getLogger('nekbot.protocols.telegram.message')


class MessageTelegram(Message):
    def __init__(self, protocol, msg):
        logger.debug('New message: %s' % vars(msg))
        user = UserTelegram(protocol, msg.sender)
        self.msg = msg
        self.historical = msg.freshness != 'new'
        super(MessageTelegram, self).__init__(protocol, msg.text, user)
        if self.is_own and not self.protocol.has_bot:
            self.protocol.set_bot(user)

    def create_group_chat(self):
        GroupChatTelegram(self.protocol, self.msg.receiver)

    def get_group_chat_id(self):
        return str(self.msg.receiver.id)

    @property
    def is_public(self):
        return True if self.is_groupchat else False

    @property
    def is_own(self):
        return self.msg.own

    @property
    def is_groupchat(self):
        return self.msg.receiver.type == 'group'

    def _copy(self):
        return self.__class__(self.protocol, self.msg)
