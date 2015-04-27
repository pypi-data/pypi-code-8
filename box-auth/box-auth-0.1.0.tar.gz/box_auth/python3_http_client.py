"""Python 3 only"""
__author__ = 'jsterling'
from http_client import IHttpClient
from urllib_helpers import StopRedirecting, parse_lowercase_headers
import urllib
import urllib.parse
import urllib.request
import logging


class HttpClient(IHttpClient):
    """
    Uses python 3 standard library in a pretty messy way
    """
    def __init__(self, encoding='utf-8', log=None):
        """:param str encoding:"""
        self._encoding = encoding
        self._log = log or logging.getLogger()

    def _escape(self, v):
        """Escapes url parameters. The standard escape doesn't do good enough percent encoding...
        I only catch + but there are probably others.
        :param str v:
        :return str:
        """
        v = v.replace('+', '%2B')
        v = urllib.parse.quote(v)
        v = v.replace('%252B', '%2B')
        return v

    def url(self, url, query_params):
        """"
        :param str url:
        :param dict query_params:
        :return str:
        """
        return "{}?{}".format(url,'&'.join(["{}={}".format(key, self._escape(value))
                                            for key, value in query_params.items()]))

    def post(self, url, post_data, headers=None):
        """
        :param str url:
        :param str post_data:
        :param dict headers:
        :return dict, str:
        """

        request = urllib.request.Request(url, post_data.encode(self._encoding), headers)
        redirect_handler = IgnoreRedirects()
        opener = urllib.request.build_opener(redirect_handler)
        try:
            response = opener.open(request)
            response_headers = parse_lowercase_headers(response.info())
            response_headers['status'] = str(response.getcode())
            content = ''.join([line.decode(self._encoding) for line in response])
        except StopRedirecting as e:
            response_headers = e.headers
            content = e.content

        return response_headers, content

    def post_form(self, url, post_data, headers=None):
        """
        :param str url:
        :param dict post_data:
        :param dict headers:
        :return dict, str:
        """
        if not headers:
            headers = {}

        headers["Content-Type"] = "application/x-www-form-urlencoded;charset={}".format(self._encoding)
        return self.post(url, urllib.parse.urlencode(post_data), headers)

    def query_params(self, url):
        """parses a url into a dict of query params. does not handle duplicates well
        :param str url:
        :return dict:
        """
        list_of_pairs = map(lambda s: s.split('='), urllib.parse.urlparse(url).query.split('&'))
        query_params = {}
        for pair in list_of_pairs:
            query_params[pair[0]] = pair[1]
        return query_params

    @classmethod
    def parse_lowercase_headers(cls, headers):
        response_headers = {}
        for header_pair in headers.items():
            name = header_pair[0].lower()
            value = header_pair[1]
            if name == 'set-cookie' and name in response_headers:
                response_headers[name] = "{};{}".format(response_headers[name], value)
            else:
                response_headers[name] = value
        return response_headers


class IgnoreRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        response_headers = parse_lowercase_headers(headers)
        response_headers['status'] = str(code)
        raise StopRedirecting(response_headers)

