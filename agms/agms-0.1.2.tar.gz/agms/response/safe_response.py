from __future__ import absolute_import
from agms.response.response import Response
from agms.exception.response_exception import ResponseException


class SAFEResponse(Response):
    """
    A class representing AGMS SAFE Response objects.
    """

    def __init__(self, response, op):
        self._response = None
        self._mapping = {
            'STATUS_CODE': 'response_code',
            'STATUS_MSG': 'response_message',
            'TRANS_ID': 'transaction_id',
            'AUTH_CODE': 'authorization_code',
            'AVS_CODE': 'avs_result',
            'AVS_MSG': 'avs_message',
            'CVV2_CODE': 'cvv_result',
            'CVV2_MSG': 'cvv_message',
            'ORDERID': 'order_id',
            'SAFE_ID': 'safe_id',
            'FULLRESPONSE': 'full_response',
            'POSTSTRING': 'post_string',
            'BALANCE': 'gift_balance',
            'GIFTRESPONSE': 'gift_response',
            'MERCHANT_ID': 'merchant_id',
            'CUSTOMER_MESSAGE': 'customer_message',
            'RRN': 'rrn',
        }
        self._response = response['soap:Envelope']['soap:Body'][op + 'Response'][op + 'Result']
        self._op = op

        if not self.is_successful():
            response_array = self.to_array()
            raise ResponseException(
                'Transaction failed with error code ' + response_array['response_code'] + ' and message ' +
                response_array['response_message'])

    def is_successful(self):
        response_array = self.to_array()
        code = response_array['response_code']
        if code != '1' and code != '2':
            return False
        return True

    def get_safe_id(self):
        return (self.to_array())['safe_id']