from logging import getLogger
from nekbot.protocols.base.group_chat import GroupChats
from nekbot.protocols.xmpp.user import UsersXMPP

__author__ = 'nekmo'

from nekbot.protocols import GroupChat

logger = getLogger('nekbot.protocols.telegram.group_chat')


class GroupChatXMPP(GroupChat):

    def get_users(self, override=True):
        pass

    @property
    def own_nick(self):
        return self.protocol.plugin['xep_0045'].ourNicks[self.id]

    def send_message(self, body, notice=False):
        msubject = None
        mtype = 'groupchat'
        body = self.protocol.prepare_message(body)
        self.protocol.sleek_send_message(self.id, body, msubject, mtype)


class GroupChatsXMPP(GroupChats):
    pass