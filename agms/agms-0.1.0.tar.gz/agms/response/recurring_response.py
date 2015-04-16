from __future__ import absolute_import
from agms.response.response import Response
from agms.exception.invalid_request_exception import InvalidRequestException


class RecurringResponse(Response):
    """
    A class representing AGMS Recurring Response objects.
    """

    def __init__(self, response, op):
        self._response = None
        self._op = op
        response = response['soap:Envelope']['soap:Body'][op + 'Response'][op + 'Result']
        
        if self._op == 'RecurringAdd' or self._op == 'RecurringDelete' or self._op == 'RecurringUpdate':
            self._mapping = {
                'RESULT': 'result',
                'MSG': 'message',
                'RecurringID': 'recurring_id'
            }
        elif self._op == 'RetrieveRecurringID':
            self._mapping = {
                'RecurringID': 'recurring_id'
            }
        else:
            raise InvalidRequestException('Invalid op in Response.')

        self._response = response