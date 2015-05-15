from nekbot.protocols.base.user import Users

__author__ = 'nekmo'

from nekbot.protocols import User


class UserTelegram(User):
    def __init__(self, protocol, user):
        self.user = user
        User.__init__(self, protocol, user.print_name, user.id)

    def send_message(self, body, notice=False):
        body = self.protocol.prepare_message(body)
        self.protocol.sender.send_msg(self.user.cmd, body)


class UsersTelegram(Users):
    pass