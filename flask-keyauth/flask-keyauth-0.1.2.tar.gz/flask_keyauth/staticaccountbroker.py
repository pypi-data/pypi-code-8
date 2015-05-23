class StaticAccountBroker(object):

    #TODO: this doesn't work?
    GET_ACCOUNT = lambda x: "dummy"

    def __init__(self, secret=None):
        if secret is None:
            raise ValueError("you must provide a value for 'secret'")
        self._secret = secret

    def is_active(self, account):
        return True

    def get_secret(self, account):
        return self._secret

    def has_rights(self, account, rights):
        return True