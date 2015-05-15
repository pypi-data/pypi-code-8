from logging import getLogger
from nekbot.protocols.base.group_chat import GroupChats
from nekbot.protocols.telegram.user import UsersTelegram

__author__ = 'nekmo'

from nekbot.protocols import GroupChat

logger = getLogger('nekbot.protocols.telegram.group_chat')


class GroupChatTelegram(GroupChat):
    def __init__(self, protocol, receiver, group_chat_id=None):
        self.receiver = receiver
        self.users = UsersTelegram(protocol)
        GroupChat.__init__(self, protocol, receiver.title, receiver.id)

    def get_users(self, override=True):
        self.protocol.sender.chat_info(self.receiver.cmd)

    def send_message(self, body, notice=False):
        self.protocol.sender.send_msg(self.receiver.cmd, self.protocol.prepare_message(body))

class GroupChatsTelegram(GroupChats):
    pass