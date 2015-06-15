"""
Exposes Flask application ``app`` for managing domain using HTTP. Run it like:

.. code:: bash

    $ mythicals http -l i

or daemonized like:

    $ mythicald http -- -c /etc/mythical/http//gunicorn.conf --log-level info

Use this `client <https://github.com/verygood/mythical-client>`_ to talk to it.
"""
from __future__ import division

__all__ = [
    'init',
    'app',
    'exc',
    'Company',
    'Merchant',
    'MerchantConfirmation',
    'MerchantOp',
    'MerchantSettlement',
    'MerchantSubmission',
    'BankAccountConfirmation',
    'BankAccountOp',
    'BankAccountSettlement',
    'BankAccountSubmission',
    'CreditCardConfirmation',
    'CreditCardHold',
    'CreditCardOp',
    'CreditCardSettlement',
    'CreditCardSubmission',
    'CreditCardVerification',
]

import errno
import logging
import inspect
import math
import re
import sys
import uuid

import coid
import flask
from flask.ext import hype
import netaddr
import newrelic.agent
import werkzeug.exceptions
import werkzeug.routing
import werkzeug.utils
import wsgim_record
import wsgim_rip

from mythicals import __version__, db, mime, form, Form, config, tracer


logger = logging.getLogger(__name__)


def init(config):
    if config.API_RECORD:
        app.wsgi_app = RecordMiddleware(app.wsgi_app)
    if config.API_NEWRELIC:
        app.wsgi_app = newrelic.agent.WSGIApplicationWrapper(app.wsgi_app)
    if config.API_PROXIED:
        app.wsgi_app = wsgim_rip.RIPMiddleware(app.wsgi_app)


class RequestMIMEMixin(object):

    def accept_match(self, *mime_types):
        mime_type = self.accept_mimetypes.best_match(
            mime_types, default=mime_types[0]
        )
        if not mime_type:
            raise exc.BadRequest('No matching accept mime-type')

    def accept_encoder(self):
        self.accept_match(mime.json.type)
        return mime.json.type, mime.json.encode

    def content_source(self):
        if self.mimetype == mime.json.type:
            charset = self.mimetype_params.get('charset') or None
            return mime.json.source(text=self.get_data(), encoding=charset)
        raise exc.BadRequest(
            'Unsupported content mime-type "{0}"'.format(self.mimetype)
        )


class RequestCompanyMixin(object):

    @werkzeug.utils.cached_property
    def company(self):
        if not self.authorization:
            return Anonymous()
        username = self.authorization.username
        if isinstance(username, str):
            username = username.decode('utf-8')
        password = self.authorization.password
        if isinstance(password, str):
            password = password.decode('utf-8')
        company = Company.authenticate(username, password)
        if company is None:
            company = Anonymous()
        return company

    @property
    def authorize(self):
        return self.company.authorize


class RequestTraceMixin(object):

    @werkzeug.utils.cached_property
    def trace_id(self):
        return tracer.id


class Request(
          RequestMIMEMixin,
          RequestCompanyMixin,
          RequestTraceMixin,
          flask.Request,
      ):

    @werkzeug.utils.cached_property
    def remote_ip_addr(self):
        return netaddr.IPAddress(flask.request.remote_addr)


class RecordMiddleware(wsgim_record.RecordMiddleware):

    class Record(Form):
        """
        A *wag* style request/response record.
        """

        user_id = form.String(default=None)

        @user_id.compute
        def guru_id(self):
            for n, v in self.response.headers:
                if n == config.API_HEADERS['user_id']:
                    return v

        guru_id = form.String(nullable=True)

        @guru_id.compute
        def guru_id(self):
            for n, v in self.response.headers:
                if n == config.API_HEADERS['trace_id']:
                    return v

        class Request(Form):

            url = form.String('environ.PATH_INFO')

            method = form.String('environ.REQUEST_METHOD')

            headers = form.List('environ', form.Tuple(form.String(), form.String()))

            @headers.parse
            def headers(self, path):
                return werkzeug.datastructures.EnvironHeaders(
                    path.value
                ).to_list(charset='utf-8')

            payload = form.String('output', optional=True)

            @payload.munge
            def payload(self, value):
                # ignore 200 GETs
                stop = lambda frame: frame.get('form', self) is not self
                with self.ctx.rewind(stop):
                    status_code = self.ctx.form.response.status_code
                if (self.method, status_code) == ('GET', 200):
                    return form.NONE
                return value

        request = form.SubForm(None, Request)

        class Response(Form):

            status = form.String()

            status_code = form.Integer('status')

            @status_code.compute
            def status_code(self):
                return int(self.status.partition(' ')[0])

            headers = form.List(form.Tuple(form.String(), form.String()))

            body = form.String('output', optional=True)

        response = form.SubForm(None, Response)

    log = staticmethod(logging.getLogger('mythical-request').info)

    def recorded(self, environ, input, errors, status, headers, output):
        try:
            record = self.Record(
                environ=environ,
                input=input,
                errors=errors,
                status=status,
                headers=headers,
                output=output
            )
            line = mime.json.encode(record)
            self.log(line)
        except Exception as ex:
            logger.exception(ex)


class Application(flask.Flask):

    request_class = Request

    def __init__(self, *args, **kwargs):
        kwargs['static_folder'] = None
        super(Application, self).__init__(*args, **kwargs)
        self.before_request(self.set_trace_id)
        self.after_request(self.add_headers_to_response)
        self.teardown_request(self.teardown_db_session)
        self.register_error_handler(Exception, self.on_error)

    @newrelic.agent.error_trace()
    def full_dispatch_request(self):
        return super(Application, self).full_dispatch_request()

    def set_trace_id(self):
        if config.API_HEADERS['trace_id'] in flask.request.headers:
            tracer.id = flask.request.headers[config.API_HEADERS['trace_id']]
        elif 'X-MYTHICAL-TRACE-ID' in flask.request.headers:
            tracer.id = flask.request.headers['X-MYTHICAL-TRACE-ID']
        else:
            tracer.reset()
        newrelic.agent.add_custom_parameter('trace_id', tracer.id)

    def add_headers_to_response(self, response):
        response.headers[config.API_HEADERS['trace_id']] = request.trace_id
        response.headers['X-MYTHICAL-TRACE-ID'] = request.trace_id
        response.headers['X-MYTHICAL-VERSION'] = __version__
        response.headers['X-MYTHICAL-HOST'] = config.HOST_NAME
        return response

    def teardown_db_session(self, _):
        db.teardown_session()

    def on_error(self, ex):
        exc_info = sys.exc_info()
        try:
            encode_type, encode = request.accept_encoder()
        except exc.BadRequest:
            flask.app.reraise(*exc_info)
        try:
            error = exc.Error.cast(ex)
        except (ValueError, LookupError):
            flask.app.reraise(*exc_info)
        if error.status_code >= 500:
            logger.exception(exc_info[0], exc_info=exc_info)
        return Response(
            status=error.status_code,
            response=encode(error),
            content_type=encode_type,
        )


app = Application('mythicals.http')


class Resource(hype.Resource):

    registry = hype.Registry(app)


class DB(hype.Binding):

    def __init__(self, cls, *args, **kwargs):
        self.cls = cls
        super(DB, self).__init__(name='db', *args, **kwargs)

    def adapts(self, obj):
        return isinstance(obj, self.cls) and not self.polymorphic

    def cast(self, obj):
        if isinstance(obj, Resource):
            obj.obj = self.cast(obj.obj)
            return obj
        if isinstance(obj, self.cls):
            return obj
        decoded_id = obj.id
        return self.get(decoded_id)

    def get(self, decoded_id):
        return self.cls.query.get(decoded_id)


class Id(hype.Id):

    def __init__(self, *args, **kwargs):
        if 'prefix' in kwargs:
            prefix = kwargs.pop('prefix')
            encoding = kwargs.pop('encoding', 'base58')
            kwargs['codec'] = coid.Id(prefix=prefix, encoding=encoding)
        super(Id, self).__init__(*args, **kwargs)


DecodedId = hype.DecodedId


class Link(hype.Link):

    def _url_map(self):
        return app.url_map


class Index(Form):

    number = form.Integer(default=1, min_value=1)

    size = form.Integer(default=10, min_value=1, max_value=25)

    after = form.DateTime(format='iso8601', default=None)

    before = form.DateTime(format='iso8601', default=None)

    def filter(self, query):
        raise NotImplementedError

    def page(self, query):
        return query.offset((self.number - 1) * self.size).limit(self.size)

    def __call__(self, query):
        query = self.filter(query)
        items = self.page(query).all()
        view = Page(index=self, query=query, items=items)
        return view


class Page(Form):

    link = form.String('index')

    @link.parse
    def link(self, path):
        return request.path + '?' + mime.url.encode(path.value)

    first_link = form.String('index')

    @first_link.parse
    def first_link(self, path):
        index = path.value.copy()
        index.number = 1
        return request.path + '?' + mime.url.encode(index)

    previous_link = form.String('index')

    @previous_link.parse
    def previous_link(self, path):
        if self.number == 1:
            return None
        index = path.value.copy()
        index.number -= 1
        return request.path + '?' + mime.url.encode(index)

    next_link = form.String('index')

    @next_link.parse
    def next_link(self, path):
        if self.number >= self.count:
            return None
        index = path.value.copy()
        index.number += 1
        return request.path + '?' + mime.url.encode(index)

    last_link = form.String('index')

    @last_link.parse
    def last_link(self, path):
        index = path.value.copy()
        index.number = self.count
        return request.path + '?' + mime.url.encode(index)

    number = form.Integer('index.number')

    size = form.Integer('index.size')

    count = form.Integer('query')

    @count.parse
    def count(self, path):
        return int(math.ceil(path.value.count() / float(self.size)))

    items = form.List(form.Field())

    @items.field.parse
    def items(self, path):
        if isinstance(path.value, Resource):
            return path.value
        resource_cls = Resource.registry.match_obj(path.value)
        if resource_cls is None:
            self.ctx.error.invalid(
                'no resource for {}'.format(type(path.value))
            )
            return form.ERROR
        resource = resource_cls()
        errors = resource.map()
        if errors:
            return form.ERROR
        return resource

    total = form.Integer('query')

    @total.parse
    def total(self, path):
        return path.value.count()


request = flask.request

RequestForm = hype.RequestForm

has_request_context = flask.has_request_context

url_for = flask.url_for

Response = flask.Response


class Health(Form):

    mod = form.String(nullable=True)

    @mod.compute
    def mod(self):
        if not config.API_HEALTH['file_path']:
            return None
        try:
            with open(config.API_HEALTH['file_path'], 'r') as fo:
                return fo.read()
        except IOError, ex:
            if ex.errno != errno.ENOENT:
                raise
            return 'down'

    enabled = form.Boolean()

    @enabled.compute
    def enabled(self):
        return self.mod and self.mod != 'down'


@app.route('/health', methods=['GET'], endpoint='health')
def show_health():
    request.authorize(None, 'health')
    encode_type, encode = request.accept_encoder()
    health = Health({})
    status = 200 if health.enabled else 503
    return Response(
        status=status, response=encode(health), content_type=encode_type,
    )


@app.route('/boom', methods=['GET'], endpoint='boom')
def boom():
    request.authorize(None, 'boom')
    star


from . import exc
from .company import Company, Anonymous
from .merchant import (
    Merchant,
    MerchantConfirmation,
    MerchantOp,
    MerchantSettlement,
    MerchantSubmission,
)
from .bank_account import (
    BankAccountConfirmation,
    BankAccountOp,
    BankAccountSettlement,
    BankAccountSubmission,
)
from .credit_card import (
    CreditCardConfirmation,
    CreditCardHold,
    CreditCardOp,
    CreditCardSettlement,
    CreditCardSubmission,
    CreditCardVerification,
)
