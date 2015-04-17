from __future__ import absolute_import
import re
from agms.request.request import Request
from agms.exception.request_validation_exception import RequestValidationException


class HPPRequest(Request):
    """
    A class representing AGMS HPP Request objects.
    """

    def __init__(self, op):
        Request.__init__(self,op)

        self._fields = {
            'TransactionType': {'setting': '', 'value': ''},
            'Amount': {'setting': '', 'value': ''}, 
            'Tax': {'setting': '', 'value': ''},
            'Shipping': {'setting': '', 'value': ''},
            'OrderDescription': {'setting': '', 'value': ''},
            'OrderID': {'setting': '', 'value': ''},
            'PONumber': {'setting': '', 'value': ''},
            'RetURL': {'setting': '', 'value': ''},
            'ACHEnabled': {'setting': '', 'value': ''},
            'SAFE_ID': {'setting': '', 'value': ''}, 
            'Donation': {'setting': '', 'value': ''},
            'UsageCount': {'setting': '', 'value': '9999999'}, 
            'Internal': {'setting': '', 'value': ''}, 
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
            'ShippingFirstName': {'setting': '', 'value': ''},
            'ShippingLastName': {'setting': '', 'value': ''},
            'ShippingCompany': {'setting': '', 'value': ''},
            'ShippingAddress1': {'setting': '', 'value': ''},
            'ShippingAddress2': {'setting': '', 'value': ''},
            'ShippingCity': {'setting': '', 'value': ''},
            'ShippingState': {'setting': '', 'value': ''},
            'ShippingZip': {'setting': '', 'value': ''},
            'ShippingCountry': {'setting': '', 'value': ''},
            'ShippingEmail': {'setting': '', 'value': ''},
            'ShippingPhone': {'setting': '', 'value': ''},
            'ShippingFax': {'setting': '', 'value': ''},
            'ProcessorID': {'setting': '', 'value': ''},
            'TransactionID': {'setting': '', 'value': ''},
            'Tracking_Number': {'setting': '', 'value': ''},
            'Shipping_Carrier': {'setting': '', 'value': ''},
            'IPAddress': {'setting': '', 'value': ''},
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
            'HPPFormat': {'setting': '', 'value': ''},
            'StartDate': {'setting': '', 'value': ''},
            'EndDate': {'setting': '', 'value': ''},
            'StartTime': {'setting': '', 'value': ''},
            'EndTime': {'setting': '', 'value': ''},
            'SuppressAutoSAFE': {'setting': '', 'value': ''},
        }

        self._optionable = [
            'FirstName', 'LastName', 'Company', 'Address1', 'Address2', 
            'City', 'State', 'Zip', 'Country', 'Phone', 'Fax',
            'EMail', 'Website', 'Tax', 'Shipping', 'OrderID', 
            'PONumber', 'ShippingFirstName', 'ShippingLastName', 'ShippingCompany', 'ShippingAddress1',
            'ShippingAddress2', 'ShippingCity', 'ShippingState', 'ShippingZip', 'ShippingCountry', 
            'ShippingEmail', 'ShippingPhone', 'ShippingFax', 'ShippingTrackingNumber', 'ShippingCarrier',
            'Custom_Field_1', 'Custom_Field_2', 'Custom_Field_3', 'Custom_Field_4', 'Custom_Field_5',
            'Custom_Field_6', 'Custom_Field_7', 'Custom_Field_8', 'Custom_Field_9', 'Custom_Field_10'
        ]

        self._numeric = [
            'Amount',
            'Tax',
            'Shipping',
            'ProcessorID',
            'TransactionID',
            'CheckABA',
            'CheckAccount',
            'CCNumber',
            'CCExpDate'
        ]

        self._enums = {
            'TransactionType': ['sale', 'auth', 'safe only', 'capture', 'void', 'refund', 'update', 'adjustment'],
            'Shipping_Carrier': ['ups', 'fedex', 'dhl', 'usps', 'UPS', 'Fedex', 'DHL', 'USPS'],
            'HPPFormat': ['1', '2']
        }

        self._boolean = ['Donation', 'AutoSAFE', 'SupressAutoSAFE']
        
        self._date = ['StartDate', 'EndDate']

        self._digit_2 = ['State', 'ShippingState']

        self._amount = ['Amount', 'TipAmount', 'Tax', 'Shipping']

        self._required = ['TransactionType']

        # Override mapping with api-specific field maps
        self._mapping['shipping_tracking_number'] = 'Tracking_Number'
        self._mapping['shipping_carrier'] = 'Shipping_Carrier'

    def validate(self):
        # All sales and auth require an amount unless donation
        if ((not self._fields['Donation']['value'] or
                self._fields['Donation']['value'] is not False) and
            (self._fields['TransactionType']['value'] == 'sale' or
                self._fields['TransactionType']['value'] == 'auth')):
            self._required.append('Amount')

        error_array = self._auto_validate()
        errors = error_array['errors']
        messages = error_array['messages']

        # ExpDate MMYY
        if ('CCExpDate' in self._fields.keys() and
            self._fields['CCExpDate']['value'] and
            (len(self._fields['CCExpDate']['value']) != 4 or
                not re.match("^(0[1-9]|1[0-2])([0-9][0-9])$", self._fields['CCExpDate']['value']))):
            errors += 1
            messages.append('CCExpDate (credit card expiration date) must be MMYY.')
        
        # CCNumber length
        if ('CCNumber' in self._fields.keys() and
            self._fields['CCNumber']['value'] and
            len(self._fields['CCNumber']['value']) != 16 and
            len(self._fields['CCNumber']['value']) != 15):
            errors += 1
            messages.append('CCNumber (credit card number) must be 15-16 digits long.')
        
        # ABA length
        if ('CheckABA' in self._fields.keys() and
            self._fields['CheckABA']['value'] and
            len(self._fields['CheckABA']['value']) != 9):
            errors += 1
            messages.append('CheckABA (routing number) must be 9 digits long.') 
        
        self.validate_errors = errors
        self.validate_messages = messages

        if errors == 0:
            return {'errors': errors, 'messages': messages}
        else:
            raise RequestValidationException('Request validation failed with ' + ' '.join(messages))

    def get_fields(self):
        fields = self._get_field_array()

        if 'AutoSAFE' in fields.keys():
            if fields['AutoSAFE'] is True:
                fields['AutoSAFE'] = 1
            else:
                fields['AutoSAFE'] = 0
        
        if 'SuppressAutoSAFE' in fields.keys():
            if fields['SuppressAutoSAFE'] is True:
                fields['SuppressAutoSAFE'] = 1
            else:
                fields['SuppressAutoSAFE'] = 0
        return fields

    def get_params(self, request):
        return {'objparameters': request}