from __future__ import absolute_import
import re
from agms.configuration import Configuration
from agms.exception.invalid_parameter_exception import InvalidParameterException
from agms.exception.request_validation_exception import RequestValidationException


class Request():
    """
    A class representing AGMS Abstract Request objects.
    """

    def __init__(self, op):
        self._validateErrors = -1
        self._validateMessages = None

        self._op = None
        self._fields = None

        self._required = None
        self._numeric = None
        self._optionable = None
        self._enums = None
        self._date = None
        self._time = None
        self._boolean = None
        self._digit_2 = None
        self._amount = None

        self._needs_account = None
        self._needs_key = None

        self._mapping_alias = None

        self._mapping = {
            'gateway_username': 'GatewayUserName',
            'gateway_password': 'GatewayPassword',
            'gateway_account': 'AccountNumber',
            'gateway_key': 'TransactionAPIKey',
            'amount': 'Amount',
            'description': 'OrderDescription',
            'order_description': 'OrderDescription',
            'return_url': 'RetURL',
            'enable_ach': 'ACHEnabled',
            'transaction_type': 'TransactionType',
            'payment_type': 'PaymentType',
            'enable_auto_add_to_safe': 'AutoSAFE',
            'processing_account_id': 'ProcessorID',
            'enable_donation': 'Donation',
            'max_link_uses': 'UsageCount',
            'cc_number': 'CCNumber',
            'cc_exp_date': 'CCExpDate',
            'cc_cvv': 'CVV',
            'cc_track_1': 'Track1',
            'cc_track_2': 'Track2',
            'cc_track_3': 'Track3',
            'cc_encrypted_data': 'MagData',
            'cc_encrypted_hardware': 'MagHardware',
            'ach_name': 'CheckName',
            'ach_routing_number': 'CheckABA',
            'ach_account_number': 'CheckAccount',
            'ach_business_or_personal': 'AccountHolderType',
            'ach_checking_or_savings': 'AccountType',
            'ach_sec_code': 'SecCode',
            'safe_action': 'SAFE_Action',
            'safe_id': 'SAFE_ID',
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'company_name': 'Company',
            'company': 'Company',
            'address': 'Address1',
            'address_1': 'Address1',
            'address_2': 'Address2',
            'city': 'City',
            'state': 'State',
            'zip': 'Zip',
            'country': 'Country',
            'phone': 'Phone',
            'fax': 'Fax',
            'email': 'EMail',
            'website': 'Website',
            'tax_amount': 'Tax',
            'shipping_amount': 'Shipping',
            'tip_amount': 'TipAmount',
            'order_id': 'OrderID',
            'po_number': 'PONumber',
            'clerk_id': 'ClerkID',
            'ip_address': 'IPAddress',
            'receipt_type': 'ReceiptType',
            'shipping_first_name': 'ShippingFirstName',
            'shipping_last_name': 'ShippingLastName',
            'shipping_company_name': 'ShippingCompany',
            'shipping_company': 'ShippingCompany',
            'shipping_address': 'ShippingAddress1',
            'shipping_address_1': 'ShippingAddress1',
            'shipping_address_2': 'ShippingAddress2',
            'shipping_city': 'ShippingCity',
            'shipping_state': 'ShippingState',
            'shipping_zip': 'ShippingZip',
            'shipping_country': 'ShippingCountry',
            'shipping_email': 'ShippingEmail',
            'shipping_phone': 'ShippingPhone',
            'shipping_fax': 'ShippingFax',
            'shipping_tracking_number': 'ShippingTrackingNumber',
            'shipping_carrier': 'ShippingCarrier',
            'custom_field_1': 'Custom_Field_1',
            'custom_field_2': 'Custom_Field_2',
            'custom_field_3': 'Custom_Field_3',
            'custom_field_4': 'Custom_Field_4',
            'custom_field_5': 'Custom_Field_5',
            'custom_field_6': 'Custom_Field_6',
            'custom_field_7': 'Custom_Field_7',
            'custom_field_8': 'Custom_Field_8',
            'custom_field_9': 'Custom_Field_9',
            'custom_field_10': 'Custom_Field_10',
            'start_date': 'StartDate',
            'end_date': 'EndDate',
            'expiring_in_30_days': 'Expiring30',
            'recurring_id': 'RecurringID',
            'merchant_id': 'MerchantID',
            'initial_amount': 'InitialAmount',
            'recurring_amount': 'RecurringAmount',
            'frequency': 'Frequency',
            'quantity': 'Quantity',
            'number_of_times_to_bill': 'NumberOfOccurrences',
            'number_of_retries': 'NumberOfRetries',
            'hpp_format': 'HPPFormat',
            'cc_last_4': 'CreditCardLast4',
            'transaction_id': 'TransactionID',
            'start_time': 'StartTime',
            'end_time': 'EndTime',
            'suppress_safe_option': 'SuppressAutoSAFE',
        }

        self.__states = ['AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FM','FL','GA','GU','HI','ID','IL','IN','IA','KS','KY','LA','ME','MH','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','MP','OH','OK','OR','PW','PA','PR','RI','SC','SD','TN','TX','UT','VT','VI','VA','WA','WV','WI','WY','AE','AA','AP']
        
        self._op = op
        # Static Name for constants not implemented

    def get(self, username, password, account, api_key):
        request_body = self.get_fields()
        request_body['GatewayUserName'] = username
        request_body['GatewayPassword'] = password
        # Adjust for a field name variation in the Reporting API
        if self._op == 'TransactionAPI' or self._op == 'QuerySAFE':
                del request_body['GatewayUserName']
                request_body['GatewayUsername'] = username
        
        # Add Account # and API Key field to request when necessary for specific API
        if self._needs_account:
            request_body['AccountNumber'] = account

        if self._needs_key:
            # Adjust for a field name variation in the Reporting API
            if self._op == 'TransactionAPI':
                request_body['TransactionAPIKey'] = api_key
            elif self._op == 'QuerySAFE':
                request_body['APIKey'] = api_key
            else:
                pass
        return request_body

    def set_field(self, name, parameter, value):
        field_name = self._map_to_field(name)

        # Fix for odd capitalization of Email
        if field_name == 'Email':
            field_name = 'EMail'

        # Check that field exists
        if field_name not in self._fields.keys():
            raise InvalidParameterException('Invalid field name ' + name + '.')

        # Ensure that setting parameters are forced to all lowercase and are case insensitive
        if parameter == 'setting':
            value = value.lower()

        # Check that it is a valid setting
        if (parameter == 'setting' and
            value and
            value != 'required' and
            value != 'disabled' and
            value != 'visible' and
            value != 'excluded' and
            value != 'hidden'):
            raise InvalidParameterException('Invalid parameter ' + parameter + 'for ' + name + '.')

        if parameter == 'setting':
            self._fields[field_name]['setting'] = value
            return True
        elif parameter == 'value':
            self._fields[field_name]['value'] = value
            return True
        else:
            raise InvalidParameterException('Invalid parameter ' + parameter + 'for ' + name + '.')

    def get_field(self, name):
        field_name = self._map_to_field(name)
        return self._fields[field_name]

    def get_validation_errors(self):
        return self._validateErrors

    def get_validation_messages(self):
        return self._validateMessages

    def _auto_validate(self):
        errors = 0
        messages = []
        if self._required:
            for field_name in self._required:
                if not self._fields[field_name]['value']:
                    errors +=1
                    messages.append('Missing required field ' + field_name + '.')
                    
        # Validate enumerated types
        if self._enums:
            for field_name, valid_values in self._enums.items():
                if self._fields[field_name]['value'] and self._fields[field_name]['value'] not in valid_values:
                    errors += 1
                    messages.append('Invalid ' + field_name + ', value ' + self._fields[field_name]['value'] + ', must be one of ' + ', '.join(valid_values) + '.')

        # Validate numeric fields
        if self._numeric:
            for field_name in self._numeric:
                if field_name in self._fields.keys() and self._fields[field_name]['value'] and not self.__is_number(self._fields[field_name]['value']) :
                    errors += 1
                    messages.append('Field ' + field_name + ' has value ' + self._fields[field_name]['value'] + ' must be numeric.')

        # Validate optionable fields
        if self._optionable:
            for field_name in self._optionable:
                if (field_name in self._fields.keys() and
                    self._fields[field_name]['setting'] and
                    self._fields[field_name]['setting'] != 'required' and
                    self._fields[field_name]['setting'] != 'disabled' and
                    self._fields[field_name]['setting'] != 'visible' and
                    self._fields[field_name]['setting'] != 'excluded' and
                    self._fields[field_name]['setting'] != 'hidden' ):

                    errors += 1
                    messages.append('Field ' + field_name + ' has setting ' + self._fields[field_name]['value'] + ', must be required, disabled, visible, hidden, or empty.')

        # Validate date fields
        if self._date:
            for field_name in self._date:
                if self._fields[field_name]['value'] and not re.match('^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$', self._fields[field_name]['value']) :
                    errors += 1
                    messages.append('Field ' + field_name + ' has setting ' + self._fields[field_name]['value'] + ', must be in date format YYYY-MM-DD.')

        # Validate time fields
        if self._time:
            for field_name in self._time:
                if not self._fields[field_name]['value'] and not re.match('^([01][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?', self._fields[field_name]['value']) :
                    errors += 1
                    messages.append('Field ' + field_name + ' has setting ' + self._fields[field_name]['value'] + ', must be in 24h time format HH:MM:SS or HH:MM.')

        # Validate boolean fields
        if self._boolean:
            for field_name in self._boolean:
                if (field_name in self._fields.keys() and
                    not self._fields[field_name]['value'] and
                    not self._fields[field_name]['value'] is not True and
                    self._fields[field_name]['value'] is not False and
                    not self._fields[field_name]['value'] is not 'TRUE' and
                    self._fields[field_name]['value'] != 'FALSE'):
                    errors += 1
                    messages.append('Field ' + field_name + ' has setting ' + self._fields[field_name]['value']
                                    + ', must be boolean TRUE or FALSE.')
        
        # Validate state code fields
        if self._digit_2:
            for field_name in self._digit_2:
                if field_name in self._fields.keys() and self._fields[field_name]['value'] and self._fields[field_name]['value'] not in self.__states:
                    errors += 1
                    messages.append('Field ' + field_name + ' has setting ' + self._fields[field_name]['value']
                                    + ', must be valid 2 digit US State code.')
        
        # Validate amount fields
        if self._amount:
            for field_name in self._amount:
                if field_name in self._fields.keys() and self._fields[field_name]['value'] and float(self._fields[field_name]['value']) > Configuration.max_amount:
                    errors += 1
                    messages.append('Field ' + str(field_name) + ' amount ' + str(self._fields[field_name]['value'])
                                    + ', is above maximum allowable value of ' + str(Configuration.max_amount))
                if field_name in self._fields.keys() and self._fields[field_name]['value'] and float(self._fields[field_name]['value']) < Configuration.min_amount:
                    errors += 1
                    messages.append('Field ' + str(field_name) + ' amount ' + str(self._fields[field_name]['value'])
                                    + ', is below minimum allowable value of ' + str(Configuration.min_amount))
                 
        return {'errors': errors, 'messages': messages}

    def _get_field_array(self):
        request = {}
        # Call validation, which ensures we've validated and done so against current data
        self.validate()

        # TODO Do we need this
        if self._validateErrors > 0:
            raise RequestValidationException('Request validation failed with ' + '  '.join(self._validateMessages) + '.')

        for field_name, settings in self._fields.items():
            if settings['setting'] == 'required':
                request[field_name] = ''
                request[field_name + '_Visible'] = 1
                request[field_name + '_Required'] = 1
                if field_name == 'EMail':
                    request['Email_Disabled'] = 0
                else:
                    request[field_name + '_Disabled'] = 0

            elif settings['setting'] == 'disabled':
                request[field_name] = ''
                request[field_name + '_Visible'] = 1
                request[field_name + '_Required'] = 0
                if field_name == 'EMail':
                    request['Email_Disabled'] = 0
                else:
                    request[field_name + '_Disabled'] = 0
            
            elif settings['setting'] == 'visible':
                request[field_name] = ''
                request[field_name + '_Visible'] = 1
                request[field_name + '_Required'] = 0
                if field_name == 'EMail':
                    request['Email_Disabled'] = 0
                else:
                    request[field_name + '_Disabled'] = 0
            
            elif settings['setting'] == 'hidden':
                pass

            elif settings['setting'] == 'excluded':
                pass

            else:
                if self._optionable and field_name in self._optionable:
                    request[field_name + '_Visible'] = 1
                    request[field_name + '_Required'] = 1
                    if field_name == 'EMail':
                        request['Email_Disabled'] = 0
                    else:
                        request[field_name + '_Disabled'] = 0

            if settings['value']:
                if (settings['value']).upper() == 'TRUE':
                    request[field_name] = 1
                elif (settings['value']).upper() == 'FALSE':
                    request[field_name] = 0
                else:
                    request[field_name] = settings['value']
        return request

    def _map_to_field(self, field_name):
        if field_name in self._mapping.keys():
            return self._mapping[field_name]
        elif self._mapping_alias and field_name in self._mapping_alias.keys():
            return self._mapping_alias[field_name]
        elif field_name in self._fields.keys():
            return field_name
        else:
            raise InvalidParameterException('Invalid field name ' + field_name + '.')

    def _map_to_name(self, field_name):
        if field_name in self._mapping.key():
            return self._mapping[field_name]
        elif field_name in self._mapping_alias.key():
            return self._mapping_alias[field_name]
        elif field_name in self._fields.key():
            return field_name
        else:
            raise InvalidParameterException('Invalid field name ' + field_name + '.')

    def __is_number(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False