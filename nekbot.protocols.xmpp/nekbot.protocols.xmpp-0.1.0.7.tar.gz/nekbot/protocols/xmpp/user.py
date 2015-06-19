from sleekxmpp import JID
from nekbot.protocols.base.user import Users

__author__ = 'nekmo'

from nekbot.protocols import User


class UserXMPP(User):
    def __init__(self, protocol, username, user_id=None, groupchat=None):
        if not username:
            username = user_id.user
        if isinstance(user_id, JID):
            self.user = user_id
            user_id = user_id.bare
        else:
            self.user = None
        User.__init__(self, protocol, username, user_id)

    def send_message(self, body, notice=False):
        if self.user is None:
            raise ValueError('JID is not provided.')
        msubject = None
        mtype = 'chat'
        self.protocol.sleek_send_message(self.user, body, msubject, mtype)


class UsersXMPP(Users):
    pass