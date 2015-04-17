from __future__ import absolute_import
from agms.agms import Agms
from agms.request.recurring_request import RecurringRequest
from agms.response.recurring_response import RecurringResponse
from agms.exception.invalid_request_exception import InvalidRequestException


class Recurring(Agms):
    """
    A class representing AGMS Recurring Payments objects.
    """

    def __init__(self):
        Agms.__init__(self)
        self._api_url = 'https://gateway.agms.com/roxapi/AGMS_Recurring.asmx'
        self._requestObject = RecurringRequest
        self._responseObject = RecurringResponse

    def add(self, params):
        self._op = 'RecurringAdd'
        self._reset_parameters()
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def delete(self, params):
        self._op = 'RecurringDelete'
        self._reset_parameters()
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def update(self, params):
        self._op = 'RecurringUpdate'
        self._reset_parameters()
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def get(self, params):
        self._op = 'RetrieveRecurringID'
        self._reset_parameters()
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()
    
    def _execute(self):
        if self._op == 'RecurringAdd':
            self._do_connect('RecurringAdd', self._responseObject)
        elif self._op == 'RecurringDelete':
            self._do_connect('RecurringDelete', self._responseObject)
        elif self._op == 'RecurringUpdate':
            self._do_connect('RecurringUpdate', self._responseObject)
        elif self._op == 'RetrieveRecurringID':
            self._do_connect('RetrieveRecurringID', self._responseObject)
        else:
            raise InvalidRequestException('Invalid request to Invoicing API ' + self.op)