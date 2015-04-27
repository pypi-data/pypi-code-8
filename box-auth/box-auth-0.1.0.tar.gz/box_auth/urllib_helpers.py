"""common junk between python 2 and 3"""
__author__ = 'jsterling'


def parse_lowercase_headers(headers):
    """makes the headers lower case
    :param HTTPMessage headers:
    :return dict:
    """
    response_headers = {}
    for header_pair in headers.items():
        name = header_pair[0].lower()
        value = header_pair[1]
        if name == 'set-cookie' and name in response_headers:
            response_headers[name] = "{};{}".format(response_headers[name], value)
        else:
            response_headers[name] = value
    return response_headers


class StopRedirecting(BaseException):
    """urllib.request.open() has a built-in redirect handler that always handles redirects or fails your request.
    this is a very hacky ghetto way of getting around it
    """
    def __init__(self, headers):
        self.headers = headers
        self.content = ""
