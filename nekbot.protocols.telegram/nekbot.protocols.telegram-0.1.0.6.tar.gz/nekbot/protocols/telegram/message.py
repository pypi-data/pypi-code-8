from logging import getLogger
from datetime import datetime, timedelta
from nekbot.protocols.telegram.group_chat import GroupChatTelegram
from nekbot.protocols.telegram.user import UserTelegram
from nekbot.protocols import Message

__author__ = 'nekmo'

logger = getLogger('nekbot.protocols.telegram.message')


class MessageTelegram(Message):
    def __init__(self, protocol, msg):
        logger.debug('New message: %s' % vars(msg))
        user = UserTelegram(protocol, msg.user)
        self.msg = msg
        if self.is_groupchat:
            groupchat = GroupChatTelegram(protocol, msg.groupname, int(self.msg.groupid))
        else:
            groupchat = None
        if protocol.bot is None and self.msg.ownmsg:
            protocol.bot = user
        # HACK: Mark messages from historic
        if self.protocol.nekbot.start_datetime > (datetime.now() + timedelta(seconds=10)) and \
                        self.msg.timestamp != datetime.now().strftime("%H:%M"):
            self.historical = True
        super(MessageTelegram, self).__init__(protocol, msg.message, user, groupchat)

    def reply(self, body, notice=False):
        self.protocol.tg.msg(self.msg.reply.cmd, self.protocol.prepare_message(body))

    @property
    def is_from_me(self):
        return self.msg.ownmsg

    @property
    def is_groupchat(self):
        return self.msg.groupname is not None