from __future__ import absolute_import
from agms.configuration import Configuration
from agms.connect import Connect
from agms.exception.request_validation_exception import RequestValidationException
from agms.exception.invalid_parameter_exception import InvalidParameterException


class Agms():
    """
    A class representing base AGMS objects.

    """
    # Version data
    MAJOR = 0
    MINOR = 1
    TINY = 0

    API = 3

    def __init__(self, username=None, password=None, account=None, api_key=None, client=None):
        if username and password:
            self._username = username
            self._password = password
            self._account = account
            self._api_key = api_key
            self._client = client
        else:
            self._username = Configuration.gateway_username
            self._password = Configuration.gateway_password
            self._account = Configuration.gateway_account
            self._api_key = Configuration.gateway_api_key
            self._client = Configuration.http_client_name

        self._api_url = None

        self._op = None
        
        self.request = None
        self.response = None
    
    @staticmethod
    def get_library_version():
        return str(Agms.MAJOR) + '.' + str(Agms.MINOR) + '.' + str(Agms.TINY)

    @staticmethod
    def get_api_version():
        return Agms.API

    def what_card_type(self, truncated, card_format='name'):
        card_abb = {
            '3': 'AX',
            '4': 'VX',
            '5': 'MC',
            '6': 'DS',
        }

        card_name = {
            '3': 'American Express',
            '4': 'Visa',
            '5': 'Mastercard',
            '6': 'Discover',
        }

        first_digit = truncated[0:1]

        if card_format == 'abbreviation':
            return card_abb.get(first_digit, 'Unknown')
        else:
            return card_name.get(first_digit, 'Unknown')

    def _do_connect(self, request_method, response_object):
        if not isinstance(self.request, self._requestObject):
            raise RequestValidationException('No request has been created, please define request parameters.')
        else:
            connect = Connect(Configuration.instantiate())
            request_body = self.request.get(self._username, self._password, self._account, self._api_key)
            request_body = self.request.get_params(request_body)
            response = connect.connect(self._api_url, request_body, request_method, response_object)
            self.response = (self._responseObject)(response, self._op)
            return True
            
    def _set_parameter(self, field, opts):
        if not self.request:
            self._reset_parameters()

        if isinstance(opts, dict) and len(opts) > 0:
            for param, value in opts.items():
                self.request.set_field(field, param, value)
            return True
        else:
            raise InvalidParameterException('Provided options are not in valid array format.')

    def _reset_parameters(self):
        self.request = None
        self.request = (self._requestObject)(self._op)

