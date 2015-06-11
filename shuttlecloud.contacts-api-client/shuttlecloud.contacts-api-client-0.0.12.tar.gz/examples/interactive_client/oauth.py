import random
import string
import urllib
import urlparse
import webbrowser


class OAuthError(Exception):
    pass


class BaseOAuth(object):

    def _format_url(self, path, params=None):
        params = params or dict()
        query = urllib.urlencode(params)
        url = "{}?{}".format(path, query)
        return url

    def _generate_state(self, length):
        alphabet = string.ascii_letters + string.digits
        state = "".join(random.choice(alphabet) for _ in xrange(length))
        return state

    def _open_browser(self, url):
        print ("\nComplete the OAuth process in the browser"
               "\nAfterwards, copy the URL from the address bar")
        webbrowser.open(url)
        result = raw_input("URL: ").strip()
        return result

    def _extract_fragment(self, url, key):
        fragment = urlparse.urlparse(url).fragment
        params = dict(urlparse.parse_qsl(fragment))
        try:
            result = params[key]
        except KeyError:
            raise OAuthError("Missing URL fragment: '{}'".format(key))
        return result


class ImplicitOAuth(BaseOAuth):

    def __init__(self, client_id, callback, scope):
        self._client_id = client_id
        self._callback = callback
        self._scope = scope

    def authorize(self):
        url = self._open_browser(self.access_token_url)
        token = self._extract_fragment(url, self.access_token_param)
        auth = self.create_auth(token)
        return auth

    @property
    def access_token_param(self):
        return "access_token"

    @property
    def access_token_url(self):
        raise NotImplementedError()


class ExplicitOAuth(BaseOAuth):

    def __init__(self, client_id, client_secret, callback, scope):
        self._client_id = client_id
        self._client_secret = client_secret
        self._callback = callback
        self._scope = scope

    def authorize(self):
        url = self._open_browser(self.authorization_code_url)
        code = self._extract_fragment(url, self.authorization_code_param)
        token = self.exchange_for_token(code)
        auth = self.create_auth(token)
        return auth

    @property
    def authorization_code_param(self):
        return "code"

    @property
    def authorization_code_url(self):
        raise NotImplementedError()

    def exchange_for_token(code):
        raise NotImplementedError()


class SimpleAccessMixin(object):

    def create_auth(self, token):
        data = {
            "access": token,
            "refresh": ""
        }
        return data


class ThreeLeggedMixin(object):

    def create_auth(self, token):
        data = {
            "3loauth": token,
        }
        return data


class YahooOAuth(ImplicitOAuth, SimpleAccessMixin):

    @property
    def access_token_url(self):
        path = "https://api.login.yahoo.com/oauth2/request_auth"
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._callback,
            "response_type": "token"
        }
        return self._format_url(path, params)


class MicrosoftOAuth(ImplicitOAuth, SimpleAccessMixin):

    @property
    def access_token_url(self):
        path = "https://login.live.com/oauth20_authorize.srf"
        params = {
            "client_id": self._client_id,
            "callback": self._callback,
            "scope": " ".join(self._scope),
            "response_type": "token"
        }
        return self._format_url(path, params)


class GoogleOAuth(ImplicitOAuth, ThreeLeggedMixin):

    @property
    def access_token_url(self):
        path = "https://accounts.google.com/o/oauth2/auth"
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._callback,
            "scope": " ".join(self._scope),
            "response_type": "token",
        }
        return self._format_url(path, params)
