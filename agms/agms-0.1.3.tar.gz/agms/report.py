from __future__ import absolute_import
from agms.agms import Agms
from agms.request.report_request import ReportRequest
from agms.response.report_response import ReportResponse
from agms.exception.invalid_request_exception import InvalidRequestException


class Report(Agms):
    """
    A class representing AGMS Report objects.
    """

    def __init__(self):
        Agms.__init__(self)
        self._api_url = None
        self._trans_api_url = 'https://gateway.agms.com/roxapi/agms.asmx'
        self._safe_api_url = 'https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx'
        self._requestObject = ReportRequest
        self._responseObject = ReportResponse

    def list_transactions(self, params):
        self._op = 'TransactionAPI'
        self._reset_parameters()
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def list_SAFEs(self, params):
        self._op = 'QuerySAFE'
        self._reset_parameters()
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def _execute(self):
        if self._op == 'TransactionAPI':
            self._api_url = self._trans_api_url
            self._do_connect('TransactionAPI', self._responseObject)
        elif self._op == 'QuerySAFE':
            self._api_url = self._safe_api_url
            self._do_connect('QuerySAFE', self._responseObject)
        else:
            raise InvalidRequestException('Invalid request to Invoicing API ' + self.op)