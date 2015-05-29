from nekbot.protocols.base.user import Users

__author__ = 'nekmo'

from nekbot.protocols import User


class UserTelegram(User):
    def __init__(self, protocol, user, user_id=None, groupchat=None):
        self.user = user
        if hasattr(user, 'print_name'):
            username = user.print_name
        else:
            username = user
        if user_id is None:
            user_id = user.id
        User.__init__(self, protocol, username, user_id)

    def send_message(self, body, notice=False):
        body = self.protocol.prepare_message(body)
        if hasattr(self.user, 'cmd'):
            cmd = self.user.cmd
        else:
            cmd = u'user#%s' % self.get_id()
        self.protocol.sender.send_msg(cmd, body)


class UsersTelegram(Users):
    pass