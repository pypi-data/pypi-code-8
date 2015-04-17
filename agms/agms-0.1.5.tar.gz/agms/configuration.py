from __future__ import absolute_import
import sys
import os
from agms.connect import Connect
from agms.util.requests_client import RequestsClient

try:
    from ConfigParser import SafeConfigParser
except:
    from configparser import SafeConfigParser

class Configuration(object):
    """
    A class representing the configuration of your AGMS Gateway account.
    You must call configure before any other AGMS operations. ::

        agms.Configuration.configure(
            "gateway_username",
            "gateway_password"
        )

    """
    server = 'gateway.agms.com'
    port = '443'
    use_unsafe_ssl = False
    
    @staticmethod
    def init(init_file):
        config = SafeConfigParser()
        config.read(init_file)
        Configuration.gateway_username = config.get('gateway','username')
        Configuration.gateway_password = config.get('gateway','password')
        Configuration.gateway_account = config.get('gateway','account')
        Configuration.gateway_api_key = config.get('gateway','api_key')
        Configuration.http_client_name = config.get('gateway','client')
        Configuration.max_amount = config.get('gateway', 'max_amount')
        Configuration.min_amount = config.get('gateway', 'min_amount')
        if config.get('gateway', 'verbose'):
            Configuration.verbose = config.get('gateway', 'verbose')
        if config.get('gateway', 'hpp_template'):
            Configuration.hpp_template = config.get('gateway', 'hpp_template')
        Configuration.max_amount = 1000
        Configuration.min_amount = 0.01

    @staticmethod
    def configure(gateway_username, gateway_password, gateway_account=None, gateway_api_key=None, http_client_name=None):
        Configuration.gateway_username = gateway_username
        Configuration.gateway_password = gateway_password
        Configuration.gateway_account = gateway_account
        Configuration.gateway_api_key = gateway_api_key
        Configuration.http_client_name = http_client_name
        Configuration.max_amount = 1000
        Configuration.min_amount = 0.01

    @staticmethod
    def instantiate():
        return Configuration(
            Configuration.gateway_username,
            Configuration.gateway_password,
            Configuration.gateway_account,
            Configuration.gateway_api_key,
            Configuration.http_client_name
        )

    def __init__(self, gateway_username, gateway_password, gateway_account=None, gateway_api_key=None, http_client_name=None):
        self.gateway_username = gateway_username
        self.gateway_password = gateway_password
        self.gateway_account = gateway_account
        self.gateway_api_key = gateway_api_key
        self.http_client_name = http_client_name

        if http_client_name:
            self._http_client = self.__http_client_from_string(http_client_name)
        else:
            self._http_client = self.__determine_http_client()


    def http(self):
        return Connect(Configuration.instantiate())

    def http_client(self):
        return self._http_client

    def __http_client_from_string(self, client_name):
        if client_name == "httplib":
            from agms.util.httplib_client import HttplibClient
            return HttplibClient()
        elif client_name == "pycurl":
            from agms.util.pycurl_client import PycurlClient
            return PycurlClient()
        elif client_name == "requests":
            from agms.util.requests_client import RequestsClient
            return RequestsClient()
        else:
            raise ValueError("Invalid http client name.")

    def __determine_http_client(self):
        if "PYTHON_HTTP_CLIENT" in os.environ:
            return self.__http_client_from_environment()

        if sys.version_info[0] == 2 and sys.version_info[1] == 5:
            return PycurlClient()
        else:
            return RequestsClient()

    def __http_client_from_environment(self):
        client_name = os.environ["PYTHON_HTTP_CLIENT"]
        if client_name == "httplib":
            return HttplibClient()
        elif client_name == "pycurl":
            return PycurlClient()
        elif client_name == "requests":
            return RequestsClient()
        else:
            raise ValueError("invalid http client")

