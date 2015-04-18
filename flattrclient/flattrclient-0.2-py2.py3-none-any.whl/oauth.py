import flattrclient
import flattrclient.base
import requests
from requests.auth import HTTPBasicAuth

def get():
    return AuthApi(requests.Session())

class AuthApi(flattrclient.base.BaseApi):

    _endpoint = 'oauth'

    def __init__(self, session):
        """ Initializes auth api.

        :param session: `requests.session.Session`."""
        super(AuthApi, self).__init__(session)
        self._api_url = 'https://flattr.com'

    def set_auth(self, client_id, client_secret):
        """ Set credentials to get a token.
        :param client_id: id of your application.
        :param client_secret: your client secret."""
        self._session.auth = HTTPBasicAuth(client_id, client_secret)

    def authorize(self, client_id, scope, redirect_uri, response_type='code'):
        """ Returns url. You have to send the user to this url.
        There, the user will, or will not authorize the app.
        Then he/she will be returned to redirect_uri. Either with code as param,
        or a json with an error message. Depending on the choice.
        http://developers.flattr.net/api/#authorization

        :param client_id: id of your client.
        :param scope: comma separated string of scopes.
        :param redirect_uri: Flattr will send the user to this endpoint after
        accepting or rejecting your application.
        :param response_type: flattr api only supports 'code' here.
        """
        req = requests.Request('GET', '%s/%s/authorize' %
                (self._api_url, self._endpoint),
            params={'client_id': client_id,
                    'scope': scope,
                    'redirect_uri': redirect_uri,
                    'response_type': response_type})
        prep_req = req.prepare()
        return prep_req.url

    @flattrclient.just_json
    @flattrclient.post('/token')
    def token(self, code, redirect_uri, grant_type='authorization_code'):
        """ Returns the access token, you should use with flattr.api.get.

        :param code: The obtained code from flattrs redirect.
        :param redirect_uri: Again. Flattr validates this.
        :param grant_type: Currently flattr only support authorization_code.
        """
        return {'code': code,
                'redirect_uri': redirect_uri,
                'grant_type': grant_type}
