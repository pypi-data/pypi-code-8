from __future__ import absolute_import
from agms.agms import Agms
from agms.request.invoicing_request import InvoicingRequest
from agms.response.invoicing_response import InvoicingResponse
from agms.exception.invalid_request_exception import InvalidRequestException


class Invoicing(Agms):
    """
    A class representing AGMS Invoice objects.
    """

    def __init__(self):
        self.op = None
        self._api_url = 'https://gateway.agms.com/roxapi/AGMS_BillPay.asmx'
        self._requestObject = InvoicingRequest
        self._responseObject = InvoicingResponse

    def customer(self, params):
        self.op = 'RetrieveCustomerIDList'
        self._reset_parameters()
        for param, config in params:
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def invoice(self, params):
        self.op = 'RetrieveInvoices'
        self._reset_parameters()
        for param, config in params:
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def submit(self, params):
        self.op = 'SubmitInvoice'
        self._reset_parameters()
        for param, config in params:
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def _execute(self):
        if self.op == 'RetrieveCustomerIDList':
            self._do_connect('RetrieveCustomerIDList', 'RetrieveCustomerIDListResponse')
        elif self.op == 'RetrieveInvoices':
            self._do_connect('RetrieveInvoices', 'RetrieveInvoicesResponse')
        elif self.op == 'SubmitInvoice':
            self._do_connect('SubmitInvoice', 'SubmitInvoiceResponse')
        else:
            raise InvalidRequestException('Invalid request to Invoicing API ' + self.op)