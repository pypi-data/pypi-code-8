"""Interface for HTTP dependencies and default implementation using python 2 or 3 standard library."""
__author__ = 'jsterling'


class IHttpClient(object):
    """Interface for the http interactions"""
    def url(self, url, query_params):
        """Escapes and appends query params to a URL
        :param str url:
        :param dict query_params:
        :return url:
        """
        return NotImplementedError("You must override this")

    def post_form(self, url, params, headers=None):
        """Sends a url encoded post
        :param str url:      The destination
        :param dict params:  Request form data to be url encoded
        :param dict headers: Request headers
        :return dict, str: A dictionary of response headers, with lower case keys, and the response body
        """
        return NotImplementedError("You must override this")

    def query_params(self, url):
        """Parses the query params of a URL into a dictionary
        :param str url:
        :return dict:
        """
        return NotImplementedError("You must override this")

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

import sys
if sys.version_info.major < 3:
    import python2_http_client
    HttpClient = python2_http_client.HttpClient
else:
    import python3_http_client
    HttpClient = python3_http_client.HttpClient
