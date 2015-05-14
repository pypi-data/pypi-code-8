from djmailgun.backends import Backend as BaseBackend


class Backend(BaseBackend):
    def get_api_url(self):
        return 'https://api.mailgun.net/v1/{server_name}/'.format(server_name=self._server_name)
