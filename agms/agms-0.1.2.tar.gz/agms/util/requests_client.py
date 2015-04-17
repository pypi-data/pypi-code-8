from __future__ import absolute_import
from agms.exception.not_found_exception import NotFoundException

try:
    import requests
except ImportError as e:
    raise NotFoundException(e)


class RequestsClient(object):
    
    def http_do(self, http_verb, url, headers, request_body):
        response = requests.request(
            http_verb,
            url,
            headers=headers,
            data=request_body,
            verify=True
        )
        return [response.status_code, response.text]
