from __future__ import absolute_import
from agms.agms import Agms
from agms.request.safe_request import SAFERequest
from agms.response.safe_response import SAFEResponse
from agms.exception.invalid_request_exception import InvalidRequestException


class SAFE(Agms):
    """
    A class representing AGMS Recurring Payments objects.
    """

    def __init__(self):
        Agms.__init__(self)
        self._api_url = 'https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx'
        self._requestObject = SAFERequest
        self._responseObject = SAFEResponse

    def add(self, params):
        self._op = 'AddToSAFE'
        self._reset_parameters()
        self._set_parameter('SAFE_Action', {'value' : 'add_safe'})
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()
    
    def update(self, params):
        self._op = 'UpdateSAFE'
        self._reset_parameters()
        self._set_parameter('SAFE_Action', {'value' : 'update_safe'})
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def delete(self, params):
        self._op = 'DeleteFromSAFE'
        self._reset_parameters()
        self._set_parameter('SAFE_Action', {'value' : 'delete_safe'})
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def _execute(self):
        if self._op == 'AddToSAFE':
            self._do_connect('AddToSAFE', self._responseObject)
        elif self._op == 'UpdateSAFE':
            self._do_connect('UpdateSAFE', self._responseObject)
        elif self._op == 'DeleteFromSAFE':
            self._do_connect('DeleteFromSAFE', self._responseObject)
        else:
            raise InvalidRequestException('Invalid request to Invoicing API ' + self.op)