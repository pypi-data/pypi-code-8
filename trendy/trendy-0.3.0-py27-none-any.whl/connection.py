import logging
import sys

import re
from suds.client import Client
from . import services



# Module level cache of clients to avoid re-instantiating clients on every use as downloading and parsing the WSDL
# on every use can get very expensive
_clients = {}


class Connection():
    """
    Manages the connection to Trend and the process of authenticating and ending the session cleanly.

    Trend user accounts are restricted on the number of connections that can be made. If a session is not ended
    gracefully it will lock that session until a session timeout occurs.

    This class is designed to be used as context manager i.e.

        with trendy.services.Connection(url, uid, pwd) as trend:
            all_profiles = trend.securityProfileRetrieveAll()

    When used in this manner there is no need to call `connect`, `authenticate` or
    `trend.client.service.endSession(trend.sid)`

    Note: See __getattr__ on how we can call SOAP methods direct with no session id
    """

    logger = logging.getLogger(__name__)

    def __init__(self, wsdl_url, username, password):
        """
        :param wsdl_url: The URL to the Trend devices WSDL
        :param username:
        :param password:
        :return:
        """
        self.url = wsdl_url
        self.username = username
        self.password = password
        self.sid = None
        self._client = None

        self._add_services_to_self()

    def __enter__(self):
        self._authenticate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.service.endSession(self.sid)
            self.sid = None

    def __getattr__(self, attr):
        """
        Pretend that the Suds.client.services methods are direct members of this class and pass along the sessionid
        variable, which is assumed to be always required and in the last positional argument.

        This allows us to call the documented SOAP methods without needing the painful sessionid
        e.g.
            with Connection(wsdl, user, pass) as trend:
              return trend.securityProfileRetrieveAll() # yay, no session id
        """
        known_suffixes = ['Retrieve', 'RetrieveAll', 'RetrieveByName', 'Save', 'Delete']
        if any(filter(attr.endswith, known_suffixes)):
            def _wrapped(*args):
                if not self.sid:
                    raise MissingContextError("There is no active session")
                else:
                    args = args + (self.sid, )
                    return getattr(self.client.service, attr)(*args)

            return _wrapped

    @property
    def client(self):
        if not self._client:
            if not self.url in _clients:
                self.logger.debug('Starting to download and parse the WSDL {}'.format(self.url))
                _clients[self.url] = Client(self.url)
                self.logger.debug('Completed download and parse the WSDL {}'.format(self.url))

            # need to clone to avoid any multiple requests being blocked/queued
            if sys.gettrace():
                # however in debugging mode using deepcopy causes the debugger to not
                # work very well at all
                self._client = _clients[self.url]
            else:
                self._client = _clients[self.url].clone()

        return self._client

    def _authenticate(self):
        self.sid = self.client.service.authenticate(self.username, self.password)

    def _add_services_to_self(self):
        for klass in dir(services):
            if klass.endswith('Service'):
                service = getattr(services, klass)(self)
                attr = convert(klass.replace('Service', ''))
                setattr(self, attr, service)

    def __repr__(self):
        return "Connection(wsdl=%r, user=%r, pass=%r)" % self.url, self.username, self.password


class MissingContextError(StandardError):
    """
    This error is raised when a class that expects to be used as a context manager is not used without a context.
    """


def convert(name):
    """
    Convert CamelCase to snake_case

    Shamelessly 'borrowed' from http://stackoverflow.com/a/1176023/10427
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()