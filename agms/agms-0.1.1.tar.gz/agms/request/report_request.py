from __future__ import absolute_import
from agms.request.request import Request
from agms.exception.invalid_request_exception import InvalidRequestException
from agms.exception.request_validation_exception import RequestValidationException


class ReportRequest(Request):
    """
    A class representing AGMS Report Request objects.
    """

    def __init__(self, op):
        Request.__init__(self,op)

        self._trans_fields = {
            'TransactionType': {'setting': '', 'value': ''},
            'PaymentType': {'setting': '', 'value': 'creditcard'},
            'Amount': {'setting': '', 'value': ''}, # Required for sale or auth
            'FirstName': {'setting': '', 'value': ''},
            'LastName': {'setting': '', 'value': ''},
            'Company': {'setting': '', 'value': ''},
            'Address1': {'setting': '', 'value': ''},
            'Address2': {'setting': '', 'value': ''},
            'City': {'setting': '', 'value': ''},
            'State': {'setting': '', 'value': ''},
            'Zip': {'setting': '', 'value': ''},
            'Country': {'setting': '', 'value': ''},
            'Phone': {'setting': '', 'value': ''},
            'Fax': {'setting': '', 'value': ''},
            'EMail': {'setting': '', 'value': ''},
            'SAFE_ID': {'setting': '', 'value': ''},
            'StartDate': {'setting': '', 'value': ''},
            'EndDate': {'setting': '', 'value': ''},
            'ProcessorID': {'setting': '', 'value': ''},
            'TransactionID': {'setting': '', 'value': ''},
            'CreditCardLast4': {'setting': '', 'value': ''}
        }

        self._safe_fields = {
            'Active': {'setting': '', 'value': ''},
            'PaymentType': {'setting': '', 'value': ''},
            'SAFE_ID': {'setting': '', 'value': ''},
            'StartDate': {'setting': '', 'value': ''},
            'EndDate': {'setting': '', 'value': ''},
            'FirstName': {'setting': '', 'value': ''},
            'LastName': {'setting': '', 'value': ''},
            'Company': {'setting': '', 'value': ''},
            'Email': {'setting': '', 'value': ''},
            'Expiring30': {'setting': '', 'value': ''},
        }
        self._numeric = [
            'Amount',
            'ProcessorID',
            'TransactionID',
            'CreditCardLast4'
        ]

        self._digit_2 = ['State']

        self._date = ['StartDate', 'EndDate']

        self._amount = ['Amount']

        if self._op == 'TransactionAPI':
            self._fields = self._trans_fields
            # Override mapping with api-specific field maps
            self._mapping['safe_id'] = 'SAFE_ID'
            self._mapping['gateway_username'] = 'GatewayUserName'

        elif self._op == 'QuerySAFE':
            self._fields = self._safe_fields
            # Override mapping with api-specific field maps
            self._mapping['safe_id'] = 'SAFE_ID'
            self._mapping['gateway_username'] = 'GatewayUserName'
            self._mapping['gateway_key'] = 'APIKey'

        else:
            raise InvalidRequestException('Invalid op in Request')
    
        self._needs_account = True
        self._needs_key = True

    def validate(self):
        error_array = self._auto_validate()

        errors = error_array['errors']
        messages = error_array['messages']
        
        self.validate_errors = errors
        self.validate_messages = messages

        if errors == 0:
            return {'errors': errors, 'messages': messages}
        else:
            raise RequestValidationException('Request validation failed with ' + ' '.join(messages))

    def get_fields(self):
        return self._get_field_array()

    def get_params(self, request):
        if self._op == 'TransactionAPI':
            return {'objparameters': request}
        elif self._op == 'QuerySAFE':
            return request
        else:
            return {'objparameters': request}