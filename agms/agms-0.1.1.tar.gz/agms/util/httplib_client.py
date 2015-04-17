from __future__ import absolute_import
from agms.exception.not_found_exception import NotFoundException
from agms.configuration import Configuration
try:
    import httplib
except ImportError as e:
    raise NotFoundException(e)


class HttplibClient(object):
    
    def http_do(self, http_verb, url, headers, request_body):
        conn = httplib.HTTPSConnection(Configuration.server, Configuration.port)
        conn.request(http_verb, url, request_body, headers)
        response = conn.getresponse()
        status = response.status
        response_body = response.read()
        conn.close()
        return [status, response_body]
