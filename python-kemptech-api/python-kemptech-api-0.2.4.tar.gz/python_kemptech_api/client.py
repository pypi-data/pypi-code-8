import abc
import logging as log
from past.builtins import long
import requests
import six

log.basicConfig(filename='/tmp/kemptech-api.log', level=log.DEBUG)


class HttpClient(object):
    """Client that performs HTTP requests."""

    endpoint = None

    def _do_request(self, http_method, rest_command, parameters=None):
        """Perform a HTTP request.

        :param http_method: GET or POST.
        :param rest_command: The command to run.
        :param parameters: dict containing parameters.
        :return: The Status code of request and the response text body.
        """
        cmd_url = "{endpoint}{cmd}?".format(endpoint=self.endpoint,
                                            cmd=rest_command)
        log.debug("cmd_url: %s", cmd_url)
        log.debug("params: %s", repr(parameters))

        try:
            response = requests.request(http_method, cmd_url,
                                        params=parameters,
                                        verify=False)
        except requests.exceptions.ConnectionError:
            log.error("A connection error occurred to %s",
                      self.loadbalancer)
            raise KempClientRequestError(response.status_code, response.text)
        except requests.exceptions.URLRequired:
            log.error("%s is not a valid URL to make a request with.",
                      cmd_url)
            raise KempClientRequestError(response.status_code, response.text)
        except requests.exceptions.TooManyRedirects:
            log.error("Too many redirects with request to %s", cmd_url)
            raise KempClientRequestError(response.status_code, response.text)
        except requests.exceptions.Timeout:
            log.error("A connection error occurred to %s",
                      self.loadbalancer)
            raise KempClientRequestError(response.status_code, response.text)
        except requests.exceptions.RequestException:
            log.error("An unknown error occurred with request to %s",
                      cmd_url)
            raise KempClientRequestError(response.status_code, response.text)
        return response.status_code, response.text

    def _get(self, rest_command, parameters):
        self._do_request('GET', rest_command, parameters)

    def _post(self, rest_command, parameters):
        self._do_request('POST', rest_command, parameters)


class ComplexIdMixin(object):
    """Mixin for adding non-trivial IDs."""

    @abc.abstractproperty
    def id(self):
        """Must return a dict with unique ID parameters for KEMP API."""
        raise NotImplementedError("This abstractproperty needs implementation")

    @id.setter
    @abc.abstractmethod
    def id(self, value):
        raise NotImplementedError("This abstractmethod needs implementation")


class BaseObjectModel(HttpClient):
    """A class to build objects based on KEMP RESTful API.

    Subclasses built from this class need to name their parameters
    the same as their RESTful API counterpart in order for this
    class to work.
    """

    @abc.abstractproperty
    def api_name(self):
        raise NotImplementedError("This abstractproperty needs implementation")

    def __init__(self, parameters):
        for api_key, api_value in parameters:
            self.__dict__[api_key] = api_value

    def save(self):
        command = 'mod' if self.exists else 'add'
        self._get_request('%s%s' % (command, self.api_name), self.to_dict())

    def delete(self):
        self._get_request('%s%s' % ('del', self.api_name), self.id)

    @property
    def exists(self):
        return self._get_request('show' + self.api_name, self.id) < 300

    def to_dict(self):
        """Return a dictionary containing attributes of class.

        Ignore attributes that are set to None or are not a string or int;
        also ignore endpoint as it is not an API thing.
        """
        attributes = {}
        for attr in self.__dict__:
            if (self.__dict__[attr] is not None
                    or not self.__dict__[attr] == 'endpoint'
                    or not isinstance(self.__dict__[attr], six.string_types)
                    or not isinstance(self.__dict__[attr], (int, long))):
                attributes[attr] = self.__dict__[attr]
        return attributes


class LoadMaster(HttpClient):
    """LoadMaster API object."""

    def __init__(self, ip, username, password):
        self.ip_address = ip
        self.username = username
        self.password = password

    @property
    def endpoint(self):
        return "https://{user}:{pw}@{ip}/access/".format(user=self.username,
                                                         pw=self.password,
                                                         ip=self.ip_address)

    def set_parameter(self, parameter, value):
        parameters = {
            'param': parameter,
            'value': value,
        }
        self._get('set', parameters)

    def get_parameter(self, parameter):
        parameters = {
            'param': parameter,
        }
        self._get('get', parameters)


class KempClientRequestError(Exception):
    """Raised if HTTP request has failed."""

    def __init__(self, code=None, msg=None):
        if msg is None:
            if code == 400:
                msg = "Mandatory parameter missing from request."
            elif code == 401:
                msg = "Username or password is missing or is incorrect."
            elif code == 403:
                msg = "Incorrect permissions."
            elif code == 404:
                msg = "Not found."
            elif code == 405:
                msg = "Unknown command."
            else:
                msg = "An unknown error has occurred."
        self.message = "KEMP Client Error: {code}; {msg}".format(code=code,
                                                                 msg=msg)
        super(KempClientRequestError, self).__init__(self.message)
