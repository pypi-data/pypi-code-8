from __future__ import absolute_import
import StringIO
from agms.exception.not_found_exception import NotFoundException
try:
    import pycurl
except ImportError as e:
    raise NotFoundException(e)


class PycurlClient(object):
    
    def http_do(self, http_verb, url, headers, request_body):
        curl = pycurl.Curl()
        response = StringIO.StringIO()

        
        curl.setopt(pycurl.CAINFO, True)
        curl.setopt(pycurl.SSL_VERIFYPEER, 1)
        curl.setopt(pycurl.SSL_VERIFYHOST, 2)
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.ENCODING, 'gzip')
        curl.setopt(pycurl.WRITEFUNCTION, response.write)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.HTTPHEADER, self._format_headers(headers))
        self._set_request_method_and_body(curl, http_verb, request_body)

        curl.perform()

        status = curl.getinfo(pycurl.HTTP_CODE)
        response = response.getvalue()
        return [status, response]

    def _set_request_method_and_body(self, curl, method, body):
        if method == "GET":
            curl.setopt(pycurl.HTTPGET, 1)
        elif method == "POST":
            curl.setopt(pycurl.POST, 1)
            curl.setopt(pycurl.POSTFIELDSIZE, len(body))
        elif method == "PUT":
            curl.setopt(pycurl.PUT, 1)
            curl.setopt(pycurl.INFILESIZE, len(body))
        elif method == "DELETE":
            curl.setopt(curl.CUSTOMREQUEST, "DELETE")

        if body:
            curl.setopt(pycurl.READFUNCTION, StringIO.StringIO(body).read)

    def _format_headers(self, headers):
        return [key + ": " + value for key, value in headers.items()]
