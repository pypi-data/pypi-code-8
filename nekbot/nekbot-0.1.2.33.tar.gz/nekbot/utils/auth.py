

class AuthAddress(object):
    def __init__(self, address):
        self._user = None
        self._host = None
        self._port = None
        self._endpoint = None
        self.address = address

    @property
    def user(self):
        if self._user is None:
            user_endpoint = self.address.split('@')
            if len(user_endpoint) > 1:
                self._user = user_endpoint[0]
            else:
                self._user = False
        return self._user

    @property
    def endpoint(self):
        if self._endpoint is None:
            self._endpoint = self.address.split('@')
            if len(self.endpoint) > 1:
                self._endpoint = self.endpoint[1]
            else:
                self._endpoint = self._endpoint[0]
        return self._endpoint

    @property
    def host(self):
        if self._host is None:
            self._host = self.endpoint.split(':')[0]
        return self._host

    @property
    def port(self):
        if self._port is None:
            host_port = self.endpoint.split(':')
            if len(host_port) < 2:
                self._port = False
            else:
                self._port = host_port[1]
        return self._port

    def __str__(self):
        return self.address

class UserPassword(object):
    def __init__(self, user_password):
        self._user = None
        self._password = None
        self.user_password = user_password

    @property
    def user(self):
        if self._user is None:
            self._user = self.user_password.split(':')
        return self._user

    @property
    def password(self):
        if self._password is None:
            user_password = self.user_password.split(':')
            if len(user_password) > 1:
                self._password = user_password[1]
            else:
                self._password = False
        return self._password
