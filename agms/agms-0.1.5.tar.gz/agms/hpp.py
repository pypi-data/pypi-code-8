from __future__ import absolute_import
from agms.configuration import Configuration
from agms.agms import Agms
from agms.request.hpp_request import HPPRequest
from agms.response.hpp_response import HPPResponse
from agms.exception.unexpected_exception import UnexpectedException
from agms.exception.invalid_request_exception import InvalidRequestException


class HPP(Agms):
    """
    A class representing AGMS Hosted Payment Page objects.
    """

    def __init__(self):
        Agms.__init__(self)
        self._api_url = 'https://gateway.agms.com/roxapi/AGMS_HostedPayment.asmx'
        self._requestObject = HPPRequest
        self._responseObject = HPPResponse
        self._hash = None

    def generate(self, params):
        self._op = 'ReturnHostedPaymentSetup'
        self._reset_parameters()
        for param, config in params.items():
            self._set_parameter(param, config)
        self._execute()
        return self.response.to_array()

    def get_hash(self):
        return self._hash 
        
    def get_link(self):
        if not self._hash:
            raise UnexpectedException('Requested HPP link but no hash generated in HPP.')
        else:
            formatted_field = self.request.get_field('HPPFormat')

            if formatted_field['value']:
                if formatted_field['value'] == '1':
                    return 'https://gateway.agms.com/HostedPaymentForm/HostedPaymentPage.aspx?hash=' + self._hash
                else:
                    return 'https://gateway.agms.com/HostedPaymentForm/HostedPaymentPage2.aspx?hash=' + self._hash
            else:
                if Configuration.hpp_template == 'TEMPLATE_1':
                    return 'https://gateway.agms.com/HostedPaymentForm/HostedPaymentPage.aspx?hash=' + self._hash
                else:
                    return 'https://gateway.agms.com/HostedPaymentForm/HostedPaymentPage2.aspx?hash=' + self._hash

    def _execute(self):
        if self._op == 'ReturnHostedPaymentSetup':
            self._do_connect('ReturnHostedPaymentSetup', self._responseObject)
            self._hash = self.response.get_hash()
        else:
            raise InvalidRequestException('Invalid request to HPP API ' + self.op)