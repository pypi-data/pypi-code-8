from __future__ import absolute_import
from agms.response.response import Response


class InvoicingResponse(Response):
    """
    A class representing AGMS Invoicing Response objects.
    """

    def __init__(self):
        self._response = None
        self._mapping = []