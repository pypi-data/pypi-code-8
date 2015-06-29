__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import http.client
import ssl
from base64 import b64encode
import socket
import json

class ExonResponse(object):
    """
    Easy handling of http responses
    """
    def __init__(self, response):
        self.response = response
        self.status = response.status
        self.data = None

    def close(self):
        """
        Closes the response
        """
        self.response.close()

    def getString(self):
        """
        :return: str: data from the response
        """
        if self.data == None:
            self.data = self.response.read().decode('utf-8')
        return self.data

    def getJson(self):
        """
        :return: dict: decode the Json response
        """
        if 'json' in self.response.getheader('Content-Type').lower():
            return json.loads(self.getString())
        else:
            return self.getString()


class ExonHttpsClient(http.client.HTTPSConnection):
    """
    The class extends http.client.HTTPSConnection and supports easy ssl connection with self signed certificates
    and basic auth
    """
    def __init__(self, host, port=None, key_file=None, cert_file=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                 source_address=None, cafile=None, check_hostname=True, user=None, password=False):
        """
        Creates a new https connection
        :param host: the host to connect to
        :param port: the port to connect to
        :param key_file: see http.client.HTTPSConnection
        :param cert_file:  see http.client.HTTPSConnection
        :param timeout:  see http.client.HTTPSConnection
        :param source_address:  see http.client.HTTPSConnection
        :param cafile: the ca pem file
        :param check_hostname: check if the host and the certificate are same
        :param user: the user for basic auth
        :param password: the passowrd for basic auth
        :return:
        """
        ctx = ssl.create_default_context(cafile=cafile)
        ctx.check_hostname = check_hostname
        userAndPass = b64encode(("%s:%s" % (user, password)).encode('utf-8')).decode("ascii")
        self.headers = {'Authorization': 'Basic %s' % userAndPass}
        self._lastReponse = None
        super().__init__(host, port, key_file, cert_file, timeout, source_address, context=ctx,
                         check_hostname=check_hostname)

    def request(self, method, url, body=None, headers=None):
        if headers == None:
            headers=self.headers
        elif type(headers) == type({}):
            for key in self.headers:
                headers[key] = self.headers[key]
        else:
            headers={}
        super().request(method, url, body, headers)

    def get(self, url):
        """
        Creates a get request and returns a ExonResponse for easy connecteion handling
        :param url: the url
        :return: ExonResponse
        """
        if self._lastReponse != None:
            self._lastReponse.close()
        self.request('GET', url)
        ret = ExonResponse(self.getresponse())
        self._lastReponse = ret
        return ret

    def delete(self, url):
        """
        Creates a delete request and returns a ExonResponse for easy connecteion handling
        :param url: the url
        :return: ExonResponse
        """
        if self._lastReponse != None:
            self._lastReponse.close()
        self.request('DELETE', url)
        ret = ExonResponse(self.getresponse())
        self._lastReponse = ret
        return ret

    def put(self, url, body = {}):
        """
        Creates a put request and returns a ExonResponse for easy connecteion handling
        :param url: the url
        :param body: a dict of json data
        :return: ExonResponse
        """
        if self._lastReponse != None:
            self._lastReponse.close()
        if type(body) == dict:
            body = json.dumps(body)
        self.request('PUT', url, body=body)
        ret = ExonResponse(self.getresponse())
        self._lastReponse = ret
        return ret

    def post(self, url, body = {}):
        """
        Creates a post request and returns a ExonResponse for easy connecteion handling
        :param url: the url
        :param body: a dict of json data
        :return: ExonResponse
        """
        if self._lastReponse != None:
            self._lastReponse.close()
        if type(body) == dict:
            body = json.dumps(body)
        self.request('POST', url, body=body)
        ret = ExonResponse(self.getresponse())
        self._lastReponse = ret
        return ret
