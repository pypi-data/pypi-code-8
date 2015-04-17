# -*- encoding: utf-8 -*-

import sys
import urllib
from flask import make_response, redirect, request, current_app
from werkzeug.local import LocalProxy
from session import Session
from dissect_exception import DissectException
from functools import wraps

class Dissect():

    def __init__(self, app=None, config={}):
        self.app = app
        if app is not None:
            self.init_app(app)
        else:
            raise DissectException('Flask app not provided.')

        self.config = config
        self.callbacks = {}
        self.session = LocalProxy(self.get_session)

    def unauthorized(self, dest_url=None):
        return make_response(dest_url, 401)

#============================================================================================================
    def init_app(self, app):
    
        @self.app.before_request
        def request_enter():
            current_app._session = Session(self, request.cookies, request)

        @self.app.after_request
        def request_exit(response):
            session = self.get_session()
            response.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With,Content-Type, Accept"
            return session.set_cookie(response)
#============================================================================================================
    def get_session(self):
        return current_app._session
#============================================================================================================
    def register(self, name):

        def w(fun):

            self.callbacks[name] = fun

            @wraps(fun)
            def w2(*args, **kwargs):
                return fun(*args, **kwargs)
            return w2
        return w

#============================================================================================================
    def __call__(self, name, raw_url=True):
        def w(fun):
            @wraps(fun)
            def w2(*args, **kwargs):

                valfun = self.callbacks.get(name)

                if not valfun:
                    sys.stderr.write('Invalid callback function: %s\n' % name)
                    return self.unauthorized()

                session = self.get_session()
                
                r = valfun(session=session)

                if not r: #authorization failed
                    ret = session.request.url if raw_url else None
                    return self.unauthorized(ret)
                return fun(*args, **kwargs)
            return w2
        return w

#============================================================================================================
