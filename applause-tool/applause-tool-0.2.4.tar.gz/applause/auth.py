from applause import __program_name__, __version__
import logging
try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

import requests
from applause.errors import InvalidLogin

from . import settings


class ApplauseAuth(object):
    """
    Handles Applause's 3 legged OAuth API.
    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        self.session = requests.Session()
        self.session.auth = (client_id, client_secret)

        self.access_token = None
        self.refresh_token = None
        self.user_id = None

    def _get_code(self, username, password):
        """
        Returns user specific oAuth access code.
        """
        response = self.session.post(settings.PLATFORM_SECURITY_CHECK_URL, data={
            'j_username': username,
            'j_password': password,
        }, allow_redirects=False)
        cookies = response.cookies

        if not cookies:
            raise InvalidLogin("Invalid credentials")

        response = self.session.get(settings.OAUTH_AUTHORIZE_URL, params={
            'client_id': self.client_id
        }, allow_redirects=False, cookies=cookies)

        location = response.headers['location']
        parts = urlparse(location)

        if not parts.query:
            return None

        query = parse_qs(parts.query)

        if 'code' not in query:
            raise InvalidLogin("Unable to obtain authorization code")

        return query['code'][0]

    def _fetch_tokens(self, code):
        """
        Ask for access and refresh token based on given authorization
        code and client credentials stored in settings.
        Return deserialized data from platform's JSON response.
        These would include: `access_token`, `expires_in`, `refresh_token`,
        `refresh_token_expires_in`, `user_id` and some other OAuth-related
        metadata.
        """
        response = self.session.post(
            settings.OAUTH_TOKEN_URL,
            data={
                "response_type": "token",
                "grant_type": "authorization_code",
                "code": code,
            }
        )

        if not response.ok:
            logging.debug("Response: {data}".format(data=response.content))
            raise InvalidLogin("Provided authorization code was invalid")

        return response.json()

    def _refresh_token(self, token):
        """
        Return a new access token in exchange for a refresh token.
        """
        response = self.session.post(
            settings.OAUTH_REFRESH_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": token,
            }
        )

        if not response.ok:
            logging.debug('Response: {data}'.format(data=response.content))
            raise InvalidLogin("Provided refresh token was invald.")

        return response.json()

    def _generate_session(self, access_token):
        """
        Generates a new requests `Session` object objects with all the
        necessary auth headers and version header for debug purposes set.
        """
        session = requests.Session()
        session.headers = {
            "Authorization": "Bearer " + access_token,
            "Accept": "application/json",
            "User-Agent": "%s v.%s" % (__program_name__, __version__)
        }

        return session

    def login(self, username=None, password=None, refresh_token=None):
        """
        Initiates user session with one of the following arguments:
        * username, password
        * refresh_token
        """
        if username and password:
            logging.debug("Logging in with username & password")
            code = self._get_code(username, password)
            tokens = self._fetch_tokens(code)

        elif refresh_token:
            logging.debug("Logging in with refresh token: {token}".format(token=refresh_token))
            tokens = self._refresh_token(token=refresh_token)

        self.access_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']
        self.user_id = tokens['user_id']

        return self._generate_session(self.access_token)

    def logged_in(self):
        """
        Returns true if a user auth session has been initiated.
        """
        return self.access_token is not None

    def who_am_i(self):
        """
        Returns platform user ID for the logged in account.
        """
        return self.user_id
