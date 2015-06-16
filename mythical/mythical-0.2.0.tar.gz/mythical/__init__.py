__version__ = '0.2.0'

__all__ = [
    'Client',
    'Error',
    'configure',
    'cli',
    'credit_card',
    'bank_account',
    'merchant',
    'Currencies',
    'Countries',
    'mime',
]

import collections
import contextlib
import copy
import json
import os
import StringIO
import threading
import urlparse

import paramiko

from .packages import pilo
from .packages import requests


class Enum(list):

    def __init__(self, values):
        super(Enum, self).__init__(values)
        for value in values:
            setattr(self, value, value)

class Error(Exception):
    pass


class MultipleFound(Exception):
    pass


class NoneFound(Exception):
    pass


ConfirmationCodes = Enum([
    'ACCEPTED',
    'MALFORMED',
])


class Config(pilo.Form):

    username = pilo.fields.String(default=None)

    password = pilo.fields.String(default=None)

    trace_id = pilo.fields.String(default=None)

    http_root = pilo.fields.String(default='http://127.0.0.1:8080')

    http_headers = pilo.fields.Dict(
        pilo.fields.String(), pilo.fields.String(), default=None
    )

    http_proxies = pilo.fields.Dict(pilo.fields.String(), pilo.fields.String(), default=None)

    sftp_address = pilo.fields.Tuple(
        (pilo.fields.String(), pilo.fields.Integer()),
        default=('127.0.0.1', 8022),
    )


default = Config()

configure = default.update


class HTTP(threading.local):

    def __init__(self, config=None):
        self.session = requests.Session()
        self.config = config or default

    def configure(self, **kwargs):
        src = self.config.copy()
        src.update(kwargs)
        self.config = Config(src)

    def method(self, method, uri, data, params, headers):
        url = urlparse.urljoin(self.config.http_root, uri)
        headers.update({
            'accept-type': mime.accept_types,
        })
        if self.config.trace_id:
            headers['x-mythical-trace-id'] = self.config.trace_id
            headers['x-verygood-guru'] = self.config.trace_id
        if data:
            text = mime.encoder_for(mime.json_type)(data)
            headers['content-type'] = mime.json_type
        else:
            text = None
        if self.config.http_headers:
            headers.update(self.config.http_headers)
        if params:
            params = mime.encoder_for(mime.urlencoded_type)(params)
        response = method(
            url,
            params=params,
            data=text,
            headers=headers,
            auth=(self.config.username, self.config.password),
            proxies=self.config.http_proxies,
        )
        response.raise_for_status()
        if not response.content:
            return
        source = mime.source_for(response.headers['content-type'])
        return source(
            response.content, encoding=response.encoding,
        )

    def get(self, uri, params=None):
        return self.method(self.session.get, uri, None, params, {})

    def delete(self, uri, params=None):
        return self.method(self.session.delete, uri, None, params, {})

    def post(self, uri, params=None, data=None):
        return self.method(self.session.post, uri, data, params, {})

    def put(self, uri, params=None, data=None):
        return self.method(self.session.put, uri, data, params, {})


http = HTTP()


class SFTP(threading.local):

    def __init__(self, config=None):
        self.config = config or default
        self.cli = None

    def configure(self, **kwargs):
        self.disconnect()
        src = self.config.copy()
        src.update(kwargs)
        self.config = Config(src)

    def connect(self):

        @contextlib.contextmanager
        def _nop():
            yield

        if self.cli is not None:
            return _nop()

        @contextlib.contextmanager
        def _disconnect():
            try:
                yield
            finally:
                self.disconnect()

        transport = paramiko.Transport(self.config.sftp_address)
        transport.connect(
            username=self.config.username, password=self.config.password
        )
        self.cli = paramiko.SFTPClient.from_transport(transport)
        return _disconnect()

    def disconnect(self):
        if self.cli:
            # NOTE; self.sftp.sock.close() doesn't send disconnect msg
            self.cli.sock.transport.close()
            self.cli = None

    def upload(self, external_id, data, remote_dir):
        text = mime.encoder_for(mime.json_type)(data)
        remote_file = os.path.join(
            'uploads', remote_dir, '{0}.json'.format(external_id)
        )
        self.cli.putfo(StringIO.StringIO(text), remote_file, confirm=False)
        return remote_file

    def download(self, external_id, remote_dir):
        remote_file = os.path.join(
            'downloads', remote_dir, '{0}.json'.format(external_id)
        )
        io = StringIO.StringIO()
        self.cli.getfo(remote_file, io)
        return mime.source_for(mime.json_type)(io.getvalue())


sftp = SFTP()


class Page(pilo.Form):

    link = pilo.fields.String()

    number = pilo.fields.Integer()

    size = pilo.fields.Integer()

    first_link = pilo.fields.String()

    @property
    def first(self):
        return type(self)(http.get(self.first_link))

    next_link = pilo.fields.String(default=None)

    @property
    def next(self):
        return (
            type(self)(http.get(self.next_link))
            if self.next_link else None
        )

    previous_link = pilo.fields.String(default=None)

    @property
    def previous(self):
        return (
             type(self)(http.get(self.previous_link))
             if self.previous_link else None
        )

    last = pilo.fields.String()

    @property
    def last(self):
        return type(self)(http.get(self.last_link))

    items = pilo.fields.List(pilo.Field())

    @items.field.parse
    def items(self, path):
        item = self.ctx.item_type()
        errors = item.map()
        if errors:
            return pilo.ERROR
        return item

    total = pilo.fields.Integer()


class Pagination(object):

    def __init__(self, uri, params, item_type):
        self.uri = uri
        self.params = params
        self.item_type = item_type
        self.page = None

    def __iter__(self):
        return self

    def next(self):
        with pilo.ctx(item_type=self.item_type):
            if not self.page:
                source = http.get(self.uri, params=self.params)
                self.page = Page(source)
                return self.page
            if self.page.next:
                self.page = self.page.next
                return self.page
            raise StopIteration()



class QueryIndex(pilo.Form):

    offset = pilo.fields.Integer(optional=True)

    limit = pilo.fields.Integer(optional=True)


class Query(object):

    def __init__(self, uri, form, index):
        self.uri = uri
        self.form = form
        self.index = index

    def all(self):
        return [item for item in self]

    def count(self):
        return copy.copy(self).limit(1).pages.next().total

    def first(self):
        items = list(copy.copy(self).limit(1))
        if len(items) == 0:
            raise NoneFound()
        return items[0]

    def one(self):
        items = list(copy.copy(self).limit(2))
        if len(items) == 0:
            raise NoneFound()
        elif len(items) > 1:
            raise MultipleFound()
        return items[0]

    def filter_by(self, **kwargs):
        self.index.map(kwargs, error='raise')
        return self

    def limit(self, value):
        self.index.map({'limit': value}, error='raise')
        return self

    def offset(self, value):
        self.index.map({'offset': value}, error='raise')
        return self

    @property
    def pages(self):
        return Pagination(self.uri, self.index.copy(), self.form)

    def __iter__(self):
        pages = self.pages
        for page in pages:
            i = 0
            while i < len(page.items):
                item = page.items[i]
                i += 1
                yield item


class ResourceMixin(object):

    def refresh(self):
        return self.map(http.get(self.link), reset=True, error='raise')


Currencies = Enum([
    'USD',
    'CAD',
])

Countries = Enum([
    'US',
    'CA',
])


from . import mime
from . import merchant
from . import bank_account
from . import credit_card
