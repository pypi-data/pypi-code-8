from __future__ import absolute_import
from agms.request.request import Request


class InvoicingRequest(Request):
    """
    A class representing AGMS Invoicing Request objects.
    """

    def __init__(self, op):
        Request.__init__(self,op)
