from flask import request, session
from flask_oauthlib.client import OAuthException

config = {
    'id': 'naver',
    'name': 'Naver',
    'request_token_params': {'scope': 'email'},
    'base_url': 'https://nid.naver.com/oauth2.0/',
    'request_token_url': None,
    'access_token_url': 'https://nid.naver.com/oauth2.0/token',
    'authorize_url': 'https://nid.naver.com/oauth2.0/authorize'
}


def initial(self, callback, *args, **kwargs):
    return self.authorize(callback=callback, *args, **kwargs)


def login(self):
    import json
    resp = self.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message
    session['token'] = (resp['access_token'], '')
    me = self.get('https://apis.naver.com/nidlogin/nid/getUserProfile.xml')

    import xmltodict
    data = xmltodict.parse(me.raw_data)
    result = {
        'user': data['data']['response'],
        'token': session['token']
    }
    return result