from __future__ import absolute_import
from agms.response.response import Response
from agms.exception.response_exception import ResponseException


class HPPResponse(Response):
    """
    A class representing AGMS HPP Response objects.
    """

    def __init__(self, response, op):
        self._response = {}
        self._op = op
        self._mapping = {
            '0': 'hash',
        }
        response = response['soap:Envelope']['soap:Body'][op + 'Response'][op + 'Result']
        self._response['0'] = response
        self._hash = response

        if not self.is_successful():
            raise ResponseException('HPP Generation failed with message ' + self._hash)

    def get_hash(self):
        return self._hash

    def is_successful(self):
        self._hash = self.get_hash()
        if (not self._hash or
            self._hash == 0 or
            'INVALID' in self._hash or
            'ERROR' in self._hash or
            'EXCEPTION' in self._hash or
            'REQUIRED' in self._hash or
            'IF USED' in self._hash or
            'MUST BE' in self._hash or
            'FAILED' in self._hash):
            return False
        else:
            return True