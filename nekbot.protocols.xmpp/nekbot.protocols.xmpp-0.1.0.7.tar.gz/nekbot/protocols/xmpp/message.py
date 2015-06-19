import warnings
from logging import getLogger
from nekbot.protocols import Message
from nekbot.protocols.xmpp.group_chat import GroupChatXMPP
from nekbot.protocols.xmpp.user import UserXMPP

__author__ = 'nekmo'

logger = getLogger('nekbot.protocols.xmpp.message')


class XMPPMessage(Message):
    def __init__(self, protocol, msg):
        user = UserXMPP(protocol, msg['mucnick'], msg['from'])
        if msg.xml.find('{urn:xmpp:delay}delay') is not None:
            self.historical = True
        self.msg = msg
        super(XMPPMessage, self).__init__(protocol, msg['body'], user)

    def get_group_chat_id(self):
        return self.msg['mucroom']

    def create_group_chat(self):
        GroupChatXMPP(self.protocol, self.msg['mucroom'].split('@')[0], self.msg['mucroom'])

    @property
    def is_public(self):
        return self.msg['type'] == 'groupchat'

    @property
    def is_own(self):
        if self.is_public:
            return self.groupchat.own_nick == self.msg['mucnick']
        return self.msg['from'].full == self.msg['to'].full

    @property
    def is_groupchat(self):
        return self.msg['mucroom'] is not None
