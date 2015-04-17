from __future__ import absolute_import
from agms.agms import Agms
from agms.request.transaction_request import TransactionRequest
from agms.response.transaction_response import TransactionResponse
from agms.exception.invalid_request_exception import InvalidRequestException


class Transaction(Agms):
    """
    A class representing AGMS Transaction objects.
    """

    def __init__(self):
        Agms.__init__(self)
        self._api_url = 'https://gateway.agms.com/roxapi/agms.asmx'
        self._requestObject = TransactionRequest
        self._responseObject = TransactionResponse
        self._op = 'ProcessTransaction'

    def process(self, params):
        self._reset_parameters()
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def _execute(self):
        if self._op == 'ProcessTransaction':
            self._do_connect('ProcessTransaction', self._responseObject)
        else:
            raise InvalidRequestException('Invalid request to Transaction API ' + self.op)