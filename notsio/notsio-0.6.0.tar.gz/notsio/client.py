# -*- coding: UTF-8 -*-
from json import dumps as json_dumps
from logging import getLogger

from requests import request


log = getLogger(__name__)


class NotsioClient(object):
    def __init__(self, baseurl, username, password, verify=True):
        self.baseurl = baseurl.rstrip('/')
        self.username = username
        self.password = password
        self.verify = verify

    def call(self, method, resource, *args, **kwargs):
        uri = '{}/index.php/apps/notsio/api/v1/{}'.format(
            self.baseurl, resource.strip('/')
        )

        kwargs['headers'] = {'content-type': 'application/json'}
        kwargs['verify'] = self.verify
        kwargs['auth'] = (self.username, self.password)

        if 'PATCH' == method:
            kwargs['data'] = json_dumps(kwargs['data'])

        log.debug('{} {}'.format(method, uri))
        response = request(method, uri, *args, **kwargs)
        log.debug(response)

        if response.status_code >= 400 and response.text:
            data = response.json()
            if 'detail' in data:
                log.warning(data['detail'])
            else:
                log.warning('Unknown error: {}'.format(data))

        response.raise_for_status()

        return response

    def get_books(self, *args, **kwargs):
        return self.call('GET', '/books', *args, **kwargs)

    def get_notes(self, *args, **kwargs):
        return self.call('GET', '/notes', *args, **kwargs)

    def post_notes(self, *args, **kwargs):
        return self.call('POST', '/notes', *args, **kwargs)

    def get_note(self, note):
        return self.call('GET', '/notes/%s' % note)

    def patch_note(self, note, **kwargs):
        return self.call('PATCH', '/notes/%s' % note, **kwargs)

    def delete_note(self, note):
        return self.call('DELETE', '/notes/%s' % note)
