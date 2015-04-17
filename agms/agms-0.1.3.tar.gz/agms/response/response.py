from __future__ import absolute_import
from agms.exception.unexpected_exception import UnexpectedException


class Response():
    """
    A class representing AGMS Response objects.
    """
    
    def __init__(self, response, op):
        self._response = response
        self._op = op
        self._mapping = None

    def to_array(self):
        return self._map_response(self._response)

    def _map_response(self, arr):
        if self._mapping:
            response = self.__do_map(arr)
            return response
        else:
            raise UnexpectedException('Response mapping not defined for this API.')

    def __do_map(self, arr):
        response = {}
        mapping = self._mapping
        if mapping:
            # We only map the end of the array containing data
            # If this element is an array, then we map its individual sub-arrays
            # Otherwise, we map

            for key, value in arr.items():
                if isinstance(value, dict):
                    response.append(self.__do_map(value))
                else:
                    if key not in mapping.keys():
                        raise UnexpectedException('Unmapped field ' + key + ' in response')
                    else:
                        response[mapping[key]] = value
        return response