from __future__ import absolute_import
from agms.request.request import Request
from agms.exception.request_validation_exception import RequestValidationException


class RecurringRequest(Request):
    """
    A class representing AGMS Recurring Request objects.
    """

    def __init__(self, op):
        Request.__init__(self,op)

        self._fields1 = {
            'RecurringID': {'setting': '', 'value': ''},
            'MerchantID': {'setting': '', 'value': ''},
            'PaymentType': {'setting': '', 'value': 'creditcard'},
            'InitialAmount': {'setting': '', 'value': ''}, 
            'RecurringAmount': {'setting': '', 'value': ''}, 
            'CCNumber': {'setting': '', 'value': ''}, 
            'CCExpDate': {'setting': '', 'value': ''},
            'CVV': {'setting': '', 'value': ''},
            'CheckName': {'setting': '', 'value': ''},
            'CheckABA': {'setting': '', 'value': ''}, 
            'CheckAccount': {'setting': '', 'value': ''}, 
            'AccountHolderType': {'setting': '', 'value': ''}, 
            'AccountType': {'setting': '', 'value': ''}, 
            'SecCode': {'setting': '', 'value': ''}, 
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
            'Website': {'setting': '', 'value': ''},
            'Custom_Field_1': {'setting': '', 'value': ''},
            'Custom_Field_2': {'setting': '', 'value': ''},
            'Custom_Field_3': {'setting': '', 'value': ''},
            'Custom_Field_4': {'setting': '', 'value': ''},
            'Custom_Field_5': {'setting': '', 'value': ''},
            'Custom_Field_6': {'setting': '', 'value': ''},
            'Custom_Field_7': {'setting': '', 'value': ''},
            'Custom_Field_8': {'setting': '', 'value': ''},
            'Custom_Field_9': {'setting': '', 'value': ''},
            'Custom_Field_10': {'setting': '', 'value': ''},
            'Custom_Field_11': {'setting': '', 'value': ''},
            'Custom_Field_12': {'setting': '', 'value': ''},
            'Custom_Field_13': {'setting': '', 'value': ''},
            'Custom_Field_14': {'setting': '', 'value': ''},
            'Custom_Field_15': {'setting': '', 'value': ''},
            'Custom_Field_16': {'setting': '', 'value': ''},
            'Custom_Field_17': {'setting': '', 'value': ''},
            'Custom_Field_18': {'setting': '', 'value': ''},
            'Custom_Field_19': {'setting': '', 'value': ''},
            'Custom_Field_20': {'setting': '', 'value': ''},
            'StartDate': {'setting': '', 'value': ''},
            'Frequency': {'setting': '', 'value': ''},
            'Quantity': {'setting': '', 'value': ''},
            'NumberOfOccurrences': {'setting': '', 'value': ''},
            'EndDate': {'setting': '', 'value': ''},
            'NumberOfRetries': {'setting': '', 'value': ''},
        }

        self._numeric = [
            'InitialAmount',
            'RecurringAmount',
            'Quantity',
            'NumberOfOccurrences',
            'NumberOfRetries',
            'CCNumber',
            'CCExpDate',
            'CheckABA',
            'CheckAccount'
        ]

        self._enums = {
            'PaymentType': ['creditcard', 'check'],
            'SecCode': ['PPD', 'WEB', 'TEL', 'CCD'],
            'AccountHolderType': ['business', 'personal'],
            'AccountType': ['checking', 'savings'],
            'Frequency': ['days', 'weeks', 'months'],
        }

        self._date = ['StartDate', 'EndDate']
        self._digit_2 = ['State', 'ShippingState']

        self._amount = ['Amount', 'TipAmount', 'Tax', 'Shipping']

        if self._op == 'RecurringAdd':
            self._fields = self._fields1

    def validate(self):
        self._required = []
        
        # If no frequency, require a frequency
        if not self._fields['Frequency']['value']:
            self._required.append('Frequency')

        # If no number of retries, require retries
        if not self._fields['NumberOfRetries']['value']:
            self._required.append('NumberOfRetries')

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
        return {'vRecurringParams': request}