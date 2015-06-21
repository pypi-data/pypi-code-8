"""Description of "users" table from database.

List of classes:
Users -- contains description of "users" table.
"""

import hashlib
import uuid

from pagapp.models import db


class Users(db.Model):
    """Class with description of "users" table.

    Table "users" contains next fields:
    id -- user unique ID.
    nickname -- user login.
    password -- hashed user password.
    salt -- salt for password.
    active -- status of user (is (s)he active or not).
    """

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(), index=True, unique=True, nullable=False)
    salt = db.Column(db.String(), index=True, nullable=False)
    active = db.Column(db.Boolean(), index=True)

    def __init__(self, nickname, password, active):
        """Saves user data in internal structures:

        Arguments:
        nickname -- user login.
        password -- not hashed user password.
        salt -- salt for password.
        active -- user status.
        """
        self.nickname = nickname
        self.set_new_password(password)
        self.active = active

    def __repr__(self):
        """Prints instance contents in debug session."""
        return 'Nickname: {}, pwd: {}, salt: {}, active: {}'.format(
            self.nickname, self.password, self.salt, self.active)

    @staticmethod
    def is_authenticated():
        return True

    def is_active(self):
        return self.active

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        """Check, is given plain password equals with saved in database.

        Argument:
        password -- plain password for comparsion.
        """
        hashed_password = hashlib.sha512(
            password.encode('utf-8') + self.salt.encode('utf-8')).hexdigest()
        if hashed_password == self.password:
            return True
        else:
            return False

    def set_new_password(self, password):
        """Sets and saves new password for current user.

        Argument:
        password -- new password for user in plain format.
        """
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(
            password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        self.password = hashed_password
        self.salt = salt
