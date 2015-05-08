from functools import wraps
import json
import logging

from .auth import get_oauth_session
from .settings import get_settings

_log = logging.getLogger(__name__)


class Tinbox:
    def __init__(self):
        self.session = get_oauth_session()
        self.settings = get_settings()

    def get_url(self, *args, **kw):
        return self.settings.get_url(*args, **kw)

    def post(self, path, *args, **kw):
        default_headers = {}
        default_headers.setdefault('content-type', 'application/json')

        kw.setdefault('headers', default_headers)

        return self.session.post(self.get_url(path), *args, **kw)

    def get(self, path, *args, **kw):
        return self.session.get(self.get_url(path), *args, **kw)

    def create_ticket(self, sender_email, subject, body, sender_name=None,
                      context=None):
        data = {'sender_email': sender_email,
                'sender_name': sender_name,
                'subject': subject,
                'body': body}

        if context is not None:
            data.update({'pks': context})

        request = self.post('tickets/',
                            data=json.dumps(data))

        return request.json()