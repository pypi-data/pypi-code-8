import random
import sys
import functools

try:
    import ujson as json
except ImportError:
    import json

from tornado.httpclient import (
    HTTPClient, AsyncHTTPClient, HTTPRequest, HTTPError
)

try:
    from tornado.concurrent import Future
except ImportError:
    from concurrent.futures import Future


class JSONRPCError(Exception):
    """Root exception for all errors related to this library"""


class TransportError(JSONRPCError):
    """An error occurred while performing a connection to the server"""


class ProtocolError(JSONRPCError):
    """An error occurred while dealing with the JSON-RPC protocol"""
    @property
    def code(self):
        if self.args:
            return self.args[0]
        return -32700


class JSONRPCServer(object):
    """A connection to a HTTP JSON-RPC server, backed by requests"""

    RPC_CONTENT_TYPE = 'application/json'

    def __init__(self, url, http_client=AsyncHTTPClient,
                 **http_request_kwargs):
        if issubclass(http_client, AsyncHTTPClient):
            self.__is_async = True
            self._send_request = self._async_request
        elif issubclass(http_client, HTTPClient):
            self.__is_async = False
            self._send_request = self._sync_request
        else:
            raise TypeError(
                'http_client is unknown type {}'.format(
                    type(http_client)))

        self.__http_client = http_client()

        for each in ('method', 'body', 'body_producer',
                     'streaming_callback', 'expect_100_continue'):
            if each in http_request_kwargs:
                del http_request_kwargs[each]

        if 'headers' not in http_request_kwargs:
            http_request_kwargs['headers'] = {}

        http_request_kwargs['headers'].update({
            'Content-Type': self.RPC_CONTENT_TYPE,
            'Accept': self.RPC_CONTENT_TYPE,
        })

        self._request = functools.partial(
            self.__http_client.fetch,
            url, method='POST', **http_request_kwargs)

    @property
    def is_async(self):
        return self.__is_async

    @property
    def http_client(self):
        return self.__http_client

    def _async_request(self, method_name, is_notification, params):
        request_body = self.serialize(method_name, params, is_notification)
        try:
            resp_future = Future()
            self._request(
                body=request_body,
                callback=functools.partial(self.parse_http_response,
                                           is_notification,
                                           resp_future)
            )
        except HTTPError as err:
            raise TransportError(
                'Error calling method {}'.format(method_name),
                err
            )

        return resp_future

    def _sync_request(self, method_name, is_notification, params):
        request_body = self.serialize(method_name, params, is_notification)
        try:
            http_response = self._request(body=request_body)
        except HTTPError as err:
            # error 4xx contains JSON-RPC error explanation in err.response
            http_response = err.response
            # raise only server errors
            if err.code >= 500:
                raise TransportError(
                    'Error calling method {}'.format(method_name),
                    err
                )

        resp, exc = self.get_response_and_exception(http_response,
                                                    is_notification)
        if exc:
            raise exc
        return resp

    def parse_http_response(self, is_notification, resp_future, http_response):
        resp, exc = self.get_response_and_exception(http_response,
                                                    is_notification)
        if exc:
            resp_future.set_exception(exc)
        else:
            resp_future.set_result(resp)

    def get_response_and_exception(self, http_response, is_notification):
        if 600 > http_response.code >= 500:
            return None, TransportError(http_response.code, 
                                        HTTPError(http_response.code))

        if is_notification:
            return None, None

        try:
            parsed = json.loads(http_response.body.decode())
        except ValueError as value_error:
            return (
                None,
                TransportError('Cannot deserialize response body',
                               value_error)
            )

        try:
            return self.parse_result(parsed), None
        except ProtocolError as err:
            return None, err

    @staticmethod
    def parse_result(result):
        """Parse the data returned by the server according to the JSON-RPC spec.
        Try to be liberal in what we accept."""
        if not isinstance(result, dict):
            raise ProtocolError(-32700, 'Response is not a dictionary')
        if result.get('error'):
            code = result['error'].get('code', '')
            message = result['error'].get('message', '')
            raise ProtocolError(code, message, result)
        elif 'result' not in result:
            raise ProtocolError(-32700, 'Response without a result field')
        else:
            return result['result']

    @staticmethod
    def dumps(data):
        """Override this method to customize the serialization process
        (eg. datetime handling)"""
        return json.dumps(data)

    def serialize(self, method_name, params, is_notification):
        """Generate the raw JSON message to be sent to the server"""
        data = {'jsonrpc': '2.0', 'method': method_name}
        if params:
            data['params'] = params
        if not is_notification:
            # some JSON-RPC servers complain when receiving str(uuid.uuid4()).
            # Let's pick something simpler.
            data['id'] = random.randint(1, sys.maxsize)
        return self.dumps(data)

    def __getattr__(self, method_name):
        return Method(self.__request, method_name)

    def __request(self, method_name, args=None, kwargs=None):
        """Perform the actual RPC call. If _notification=True,
        send a notification and don't wait for a response"""
        is_notification = kwargs.pop('_notification', False)
        if args and kwargs:
            raise ProtocolError(
                -32700,
                'JSON-RPC spec forbids mixing arguments and keyword arguments'
            )
        return self._send_request(method_name, is_notification, args or kwargs)


class Method(object):
    def __init__(self, request_method, method_name):
        if method_name.startswith("_"):  # prevent rpc-calls for private methods
            raise AttributeError("invalid attribute '%s'" % method_name)
        self.__request_method = request_method
        self.__method_name = method_name

    def __getattr__(self, method_name):
        if method_name.startswith("_"):  # prevent rpc-calls for private methods
            raise AttributeError("invalid attribute '%s'" % method_name)
        return Method(self.__request_method, "%s.%s" % (self.__method_name, method_name))

    def __call__(self, *args, **kwargs):
        return self.__request_method(self.__method_name, args, kwargs)
