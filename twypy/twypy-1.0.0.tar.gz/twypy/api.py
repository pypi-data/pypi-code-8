from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1Session
from . import __version__

class Request(object):
    def __init__(self, client, path=None):
        self._client = client
        self._path   = path

    def __getitem__(self, path):
        _path = '%s/%s' % (self._path, path)
        return Request(self._client, _path)

    def __getattr__(self, path):
        return self[path]

    def get(self, **params):
        return self._client.request('GET', self._path, **params)._data

    def post(self, **params):
        return self._client.request('POST', self._path, **params)._data

    def get_path(self):
        return self._path

class Response(object):
    def __init__(self, response, request_method, json_data):
        self._resource_url   = response.url
        self._headers        = response.headers
        self._request_method = request_method
        self._data           = json_data

class Client(object):
    _api_version = '1.1'
    _api_url     = 'https://api.twitter.com'
    _user_agent  = 'Twypy v%s' % __version__

    def __getattr__(self, path):
        return Request(self, path)

    def configure_oauth_session(self, session):
        _session         = session
        _session.headers = {'User-Agent': self.get_user_agent()}
        return _session

    def get_user_agent(self):
        return self._user_agent

    def request(self, method, path, **params):
        _method         = method.upper()
        _url            = self.get_url(path)
        _request_kwargs = {}

        if _method == 'GET':
            _request_kwargs['params'] = params
        elif _method == 'POST':
            _request_kwargs['data'] = params

        _response = self.get_response(_method, _url, **_request_kwargs)

        return self.handle_response(_method, _response)

    def get_url(self, path):
        return '%s/%s/%s.json' % (self._api_url, self._api_version, '/'.join(path.split('/')[1:]))

    def get_response(self, method, url, **request_kwargs):
        return self._session.request(method, url, **request_kwargs)

    def handle_response(self, method, response):
        if response.status_code == 200:
            return Response(response, method, response.json())

class Api(Client):
    def __init__(self, consumer_key, consumer_secret, access_token=None, access_token_secret=None):
        self._request_token_url     = '%s/oauth/request_token' % self._api_url
        self._access_token_url      = '%s/oauth/access_token' % self._api_url
        self._consumer_key          = consumer_key
        self._consumer_secret       = consumer_secret
        self._access_token          = access_token
        self._access_token_secret   = access_token_secret
        self._session               = self.get_oauth_session()

    def get_oauth_session(self):
        return self.configure_oauth_session(OAuth1Session(client_key            = self._consumer_key,
                                                          client_secret         = self._consumer_secret,
                                                          resource_owner_key    = self._access_token,
                                                          resource_owner_secret = self._access_token_secret))
