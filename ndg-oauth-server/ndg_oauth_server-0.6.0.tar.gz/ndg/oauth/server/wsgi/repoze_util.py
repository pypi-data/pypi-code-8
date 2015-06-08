'''
Created on 17 Apr 2015

@author: philipkershaw
'''
from zope.interface import directlyProvides

from repoze.who._compat import REQUEST_METHOD
from repoze.who.interfaces import IRequestClassifier


def oauth2basicauth_request_classifier(environ):
    """Return one of the following classifiers:

    'oauth2basicauth':  the request comes from OAuth 2.0 client
    requesting an access token.
    """
    request_method = REQUEST_METHOD(environ)

    if (request_method == 'POST' and 
        environ.get('PATH_INFO', '').startswith('/oauth/access_token')):
        return 'oauth2basicauth'
    else:
        return 'browser'

directlyProvides(oauth2basicauth_request_classifier, IRequestClassifier)