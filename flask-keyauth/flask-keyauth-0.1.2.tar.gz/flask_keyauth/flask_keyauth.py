"""
    flask.ext.keyauth
    ---------------

    This module provides RSA authentication and authorization for
    Flask. It lets you work with requests in a database-independent manner.

initiate the KeyManager with a app and set account ID, signature and timestamp
"""

from flask import current_app, request, abort
from functools import update_wrapper
import datetime
import urllib.parse
from Crypto.Hash import SHA256

#simple macros where x is a request object
GET_TIMESTAMP = lambda x: x.values.get('TIMESTAMP')
GET_ACCOUNT = lambda x: x.values.get('ACCOUNT_ID')
GET_SIGNATURE = lambda x: x.headers.get('X-Auth-Signature')


class KeyManager(object):
    """
    This object is used to hold the settings for authenticating requests.  Instances of
    :class:`HmacManager` are not bound to specific apps, so you can create one in the
    main body of your code and then bind it to your app in a factory function.
    """
    def __init__(self, account_broker, app=None, account_id=GET_ACCOUNT, signature=GET_SIGNATURE,
                 timestamp=GET_TIMESTAMP, valid_time=5):
        """
        :param app Flask application container
        :param account_broker AccountBroker object
        :param account_id :type callable that takes a request object and :returns the Account ID (default
            ACCOUNT_ID parameter in the query string or POST body)
        :param signature :type callable that takes a request object and :returns the signature value (default
            X-Auth-Signature header)
        :param timestamp :type callable that takes a request object and :returns the timestamp (default
            TIMESTAMP parameter in the query string or POST body)
        :param valid_time :type integer, number of seconds a timestamp remains valid (default 20)
        """

        self._account_id = account_id
        self._signature = signature
        self._timestamp = timestamp
        self._account_broker = account_broker
        self._valid_time = valid_time

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.key_manager = self

    def is_authorized(self, request_obj, required_rights):
        try:
            timestamp = self._timestamp(request_obj)
            assert timestamp is not None
        except:
            #TODO: add logging
            return False

        ts = datetime.datetime.fromtimestamp(float(timestamp))

        #is the timestamp valid?
        if ts < datetime.datetime.now()-datetime.timedelta(seconds=self._valid_time) \
                or ts > datetime.datetime.now():
            #TODO: add logging
            return False

        #do we have an account ID in the request?
        try:
            account_id = self._account_id(request_obj)
        except:
            #TODO: add logging
            return False

        try:
            sent_signature = self._signature(request_obj)
        except:
            #TODO: add logging
            return False

        #do we have a key and rights for this account?
        #implicitly, does this account exist?
        key = self._account_broker.get_key(account_id)
        if key is None:
            #TODO: add logging
            return False

        #Is the account active, valid, etc?
        if not self._account_broker.is_active(account_id):
            #TODO: add logging
            return False

        #hash the request URL and Body
        url = urllib.parse.urlparse(request.url.encode())
        hasher = SHA256.new()
        hasher.update(url.path + "?" + url.query)
        if request.method == "POST":
            hasher.update(request.body)
        calculated_signature = key.sign(hasher.hexdigest(), '')

        #compare to what we got as the sig
        if not calculated_signature == sent_signature:
            #TODO: add logging
            return False

        #ensure this account has the required rights
        #TODO: add logging
        if required_rights is not None:
            if isinstance(required_rights, list):
                return self._account_broker.has_rights(account_id, required_rights)
            else:
                return self._account_broker.has_rights(account_id, [required_rights])

        return True

def key_auth(rights=None):
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if current_app.hmac_manager.is_authorized(request, rights):
                return f(*args, **kwargs)
            else:
                abort(403)
        return update_wrapper(wrapped_function, f)
    return decorator