"""
Rdio Python Client

Resources:
http://www.rdio.com/developers/docs/
http://www.rdio.com/developers/docs/web-service/overview/
http://www.rdio.com/developers/docs/web-service/oauth/
"""

import cgi
import oauth2 as oauth
import json
from urllib import urlencode


BASE_URL = "http://api.rdio.com/1/"
BASE_AUTH_URL = "http://api.rdio.com/oauth"
REQUEST_METHOD = 'POST'


class RdioClient(oauth.Consumer):
    def __init__(self, consumer_key, consumer_secret, redirect_uri):
        self.key = consumer_key
        self.secret = consumer_secret
        self.redirect_uri = redirect_uri
        self.login_url = None
        self.oauth_token = None
        self.request_token = None
        self.access_token = None

    def request_request_token_and_login_url(self):
        client = oauth.Client(self)
        endpoint = "/request_token"
        request_token_url = "%s%s" % (BASE_AUTH_URL, endpoint)
        response, content = client.request(
            request_token_url,
            'POST',
            urlencode({'oauth_callback': self.redirect_uri})
        )
        parsed_content = dict(cgi.parse_qsl(content))
        oauth_token = parsed_content['oauth_token']
        request_token = oauth.Token(
            parsed_content['oauth_token'],
            parsed_content['oauth_token_secret']
        )
        login_url = parsed_content['login_url']
        return request_token, oauth_token, login_url

    def get_authorize_url(self):
        if not self.login_url or not self.oauth_token:
            self.request_token, self.oauth_token, self.login_url = self.request_request_token_and_login_url()
        return "%s?oauth_token=%s" % (self.login_url, self.oauth_token)

    def _parse_url_parameters(self, url):
        query_string = url.split('?')[1]
        if not query_string:
            return
        params = query_string.split('&')
        result = {}
        for param in params:
            key, value = param.split('=')
            result[key] = value
        return result

    def _get_oauth_verifier(self, url):
        oauth_verifier_response = self._parse_url_parameters(url)
        if not oauth_verifier_response:
            return
        oauth_verifier = oauth_verifier_response.get('oauth_verifier')
        return oauth_verifier

    def verify_request_token(self, url):
        if not self.request_token:
            self.request_token, self.oauth_token, self.login_url = self.request_request_token_and_login_url()
        oauth_verifier = self._get_oauth_verifier(url)
        self.request_token.set_verifier(oauth_verifier)

    def request_access_token(self, as_dict=True):
        if not self.request_token.verifier:
            return
        verified_client = oauth.Client(self, self.request_token)
        endpoint = "/access_token"
        access_token_url = "%s%s" % (BASE_AUTH_URL, endpoint)
        response, content = verified_client.request(
            access_token_url,
            'POST'
        )
        parsed_content = dict(cgi.parse_qsl(content))
        oauth_token = parsed_content['oauth_token']
        oauth_token_secret = parsed_content['oauth_token_secret']
        if not as_dict:
            return oauth.Token(oauth_token, oauth_token_secret)
        access_token = {
            'oauth_token': oauth_token,
            'oauth_token_secret': oauth_token_secret
        }
        return access_token

    """API endpoints"""
    def _client(self):
        if not self.access_token:
            return oauth.Client(self)
        return oauth.Client(self, self.access_token)

    def set_access_token(self, access_token):
        self.access_token = access_token

    def _make_request(self, method, endpoint, params={}):
        client = self._client()
        if not client:
            print "pyrdio error! Couldn't get a client!"
            return
        params['method'] = endpoint
        response = client.request(BASE_URL,
                                  method,
                                  urlencode(params))
        return response

    def me(self):
        response = self._make_request(REQUEST_METHOD,
                                      'currentUser')
        return response

    def search(self, query=None, params=None):
        if not query and not params.get('query'):
            return
        response = self._make_request(REQUEST_METHOD,
                                      'search',
                                      params)
        if not response:
            return
        results = json.loads(response[1])
        results = results.get('result')
        results = results.get('results')
        return results

    def get_tracks_by_isrc(self, params=None):
        """
            Required parameter: 
                * isrc
        """
        response = self._make_request(REQUEST_METHOD,
                                      'getTracksByISRC',
                                      params)
        if not response:
            return
        results = json.loads(response[1])
        results = results.get('result')
        if not results:
            return
        return results

    def playlist_create(self, params=None):
        name = params.get('name')
        description = params.get('description')
        tracks = params.get('tracks')
        if not (name and description and tracks):
            return
        response = self._make_request(REQUEST_METHOD,
                                      'createPlaylist',
                                      params)
        if not response:
            return
        results = json.loads(response[1])
        return results

    def playlist_add_tracks(self, params=None):
        name = params.get('playlist')
        tracks = params.get('tracks')
        if not (name and tracks):
            return
        response = self._make_request(REQUEST_METHOD,
                                      'addToPlaylist',
                                      params)
        if not response:
            return
        results = json.loads(response[1])
        return results

    def get_heavy_rotation(self, params=None):
        response = self._make_request(REQUEST_METHOD,
                                      'getHeavyRotation',
                                      params)
        if not response:
            return
        response = json.loads(response[1])
        return response
