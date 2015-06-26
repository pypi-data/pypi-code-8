from __future__ import absolute_import

from werkzeug.wrappers import Response as WerkzeugBaseResponse

from .utils import locked_cached_property


class Request(object):
    """The base request class."""

    def __init__(self, initial_request):
        self.initial_request = initial_request

    def parse(self, parser_class):
        parser = parser_class()
        self.data = parser.parse(self.get_data())

    @locked_cached_property
    def method(self):
        return self.get_method()

    @locked_cached_property
    def uri(self):
        return self.get_uri()

    def get_data(self):
        raise NotImplementedError()

    def get_method(self):
        raise NotImplementedError()

    def get_uri(self):
        raise NotImplementedError()


class Response(object):
    """The base response class."""

    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {}

    def render(self, renderer_class):
        renderer = renderer_class()
        self.data = renderer.render(self.data)
        return self.make_response()

    def make_response(self):
        raise NotImplementedError()


class WerkzeugRequest(Request):
    """The request class implemented based on Werkzeug."""

    def get_data(self):
        return self.initial_request.data

    def get_method(self):
        return self.initial_request.method

    def get_uri(self):
        return self.initial_request.url


class WerkzeugResponse(Response):
    """The response class implemented based on Werkzeug."""

    def make_response(self):
        return WerkzeugBaseResponse(self.data, self.status, self.headers)
