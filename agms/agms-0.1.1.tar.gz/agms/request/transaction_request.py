from __future__ import absolute_import
import re
from agms.request.request import Request
from agms.exception.request_validation_exception import RequestValidationException


class TransactionRequest(Request):
    """
    A class representing AGMS Transaction Request objects.
    """

    def __init__(self, op):
        
        Request.__init__(self,op)

        self._fields = {
            'TransactionType': {'setting': '', 'value': ''},
            'PaymentType': {'setting': '', 'value': 'creditcard'},
            # Required for sale or auth
            'Amount': {'setting': '', 'value': ''},
            # Required for Adjustment
            'TipAmount': {'setting': '', 'value': ''},
            'Tax': {'setting': '', 'value': ''},
            'Shipping': {'setting': '', 'value': ''},
            'OrderDescription': {'setting': '', 'value': ''},
            'OrderID': {'setting': '', 'value': ''},
            'ClerkID': {'setting': '', 'value': ''},
            'PONumber': {'setting': '', 'value': ''},
            # Required for sale and auth if payment type = creditcard without safe id
            'CCNumber': {'setting': '', 'value': ''},
            # Required for sale and auth if payment type = creditcard without safe id
            'CCExpDate': {'setting': '', 'value': ''},
            'CVV': {'setting': '', 'value': ''},
            # Required for sale and auth if payment type = check without safe id
            'CheckName': {'setting': '', 'value': ''},
            # Required for sale and auth if payment type = check without safe id
            'CheckABA': {'setting': '', 'value': ''},
            # Required for sale and auth if payment type = check without safe id
            'CheckAccount': {'setting': '', 'value': ''},
            # Required for sale and auth if payment type = check without safe id
            'AccountHolderType': {'setting': '', 'value': ''},
            # Required for sale and auth if payment type = check without safe id
            'AccountType': {'setting': '', 'value': ''},
            # Required for sale and auth if payment type = check without safe id
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
            'Track1': {'setting': '', 'value': ''},
            'Track2': {'setting': '', 'value': ''},
            'Track3': {'setting': '', 'value': ''},
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
            'SAFE_Action': {'setting': '', 'value': ''},
            'SAFE_ID': {'setting': '', 'value': ''},
            'ReceiptType': {'setting': '', 'value': ''},
            'MagData': {'setting': '', 'value': ''},
            'MagHardware': {'setting': '', 'value': ''},
        }

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
            'SAFE_Action': ['add_safe', 'update_safe', 'delete_safe'],
            'PaymentType': ['creditcard', 'check'],
            'SecCode': ['PPD', 'WEB', 'TEL', 'CCD'],
            'AccountHolderType': ['business', 'personal'],
            'AccountType': ['checking', 'savings'],
            'MagHardware': ['MAGTEK', 'IDTECH'],
            'Shipping_Carrier': ['ups', 'fedex', 'dhl', 'usps', 'UPS', 'Fedex', 'DHL', 'USPS'],
        }

        self._digit_2 = ['State', 'ShippingState']

        self._amount = ['Amount', 'TipAmount', 'Tax', 'Shipping']

        # Override mapping with api-specific field maps
        self._mapping['shipping_tracking_number'] = 'Tracking_Number'
        self._mapping['shipping_carrier'] = 'Shipping_Carrier'

    def validate(self):
        self._required = []
        # Unless this is a safe action only request, require a transaction type
        if not self._fields['SAFE_Action']['value']:
            self._required.append('TransactionType')

        # If no transaction type, require a Safe Action
        if not self._fields['TransactionType']['value']:
            self._required.append('SAFE_Action')

        # All sales and auth require an amount
        if (self._fields['TransactionType']['value'] == 'sale' or
            self._fields['TransactionType']['value'] == 'auth'):
            self._required.append('Amount')

        # Captures, refunds, voids, updates, adjustments need a Transaction ID
        if (self._fields['TransactionType']['value'] == 'capture' or
            self._fields['TransactionType']['value'] == 'refund' or
            self._fields['TransactionType']['value'] == 'void' or
            self._fields['TransactionType']['value'] == 'adjustment'):
            self._required.append('TransactionID')

        # Require TipAmount for Tip Adjustment transactions
        if self._fields['TransactionType']['value'] == 'adjustment':
            self._required.append('TipAmount')

        # All safe updates and deletes require a safe id
        if (self._fields['SAFE_Action']['value'] == 'update' or
            self._fields['SAFE_Action']['value'] == 'delete'):
            self._required.append('SAFE_ID')


        if self._fields['PaymentType']['value'] == 'check':
            # Cheque transaction
            if not self._fields['SAFE_ID']['value']:
                # If no Safe ID we need all the check info
                self._required.append('CheckName')
                self._required.append('CheckABA')
                self._required.append('CheckAccount')
                if (self._fields['TransactionType']['value'] == 'sale' or
                    self._fields['TransactionType']['value'] == 'auth'):
                    self._required.append('SecCode')
        else:
            # Credit card transaction
            # If no SAFE ID and its a sale or auth
            if (not self._fields['SAFE_ID']['value'] and
                (self._fields['TransactionType']['value'] == 'sale' or
                    self._fields['TransactionType']['value'] == 'auth')):
                # If no Safe ID we need the card info
                # If no MagData then we need keyed info
                if not self._fields['MagData']['value']:
                    self._required.append('CCNumber')
                    self._required.append('CCExpDate')
                else:
                    self._required.append('MagHardware')
        
        error_array = self._auto_validate()
        
        errors = error_array['errors']
        messages = error_array['messages']

        # ExpDate MMYY
        if (self._fields['CCExpDate']['value'] and
            (len(self._fields['CCExpDate']['value']) != 4 or
                not re.match("^(0[1-9]|1[0-2])([0-9][0-9])$", self._fields['CCExpDate']['value']))):
            errors += 1
            messages.append('CCExpDate (credit card expiration date) must be MMYY.')
        
        # CCNumber length
        if (self._fields['CCNumber']['value'] and
            len(self._fields['CCNumber']['value']) != 16 and
            len(self._fields['CCNumber']['value']) != 15):
            errors += 1
            messages.append('CCNumber (credit card number) must be 15-16 digits long.')
        
        # ABA length
        if (self._fields['CheckABA']['value'] and
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
        return self._get_field_array()

    def get_params(self, request):
        return {'objparameters': request}