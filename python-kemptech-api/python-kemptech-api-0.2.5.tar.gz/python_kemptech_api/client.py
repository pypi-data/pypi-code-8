import abc
import logging as log
from os import path
from past.builtins import long
import requests
from requests import exceptions
import six
import xmltodict

log.basicConfig(level=log.DEBUG)
log = log.getLogger(__name__)


class HttpClient(object):
    """Client that performs HTTP requests."""

    endpoint = None

    def _do_request(self, http_method, rest_command,
                    parameters=None,
                    file=None):
        """Perform a HTTP request.

        :param http_method: GET or POST.
        :param rest_command: The command to run.
        :param parameters: dict containing parameters.
        :param file: Location of file to send.
        :return: The Status code of request and the response text body.
        """
        cmd_url = "{endpoint}{cmd}?".format(endpoint=self.endpoint,
                                            cmd=rest_command)
        log.debug("Request is: %s", cmd_url)

        try:
            if file is not None:
                with open(file, 'rb') as payload:
                    response = requests.request(http_method, cmd_url,
                                                params=parameters,
                                                verify=False,
                                                data=payload)
            else:
                response = requests.request(http_method, cmd_url,
                                            params=parameters,
                                            verify=False)
            if response.status_code > 299:
                raise exceptions.HTTPError
        except exceptions.ConnectionError:
            log.exception("A connection error occurred to %s",
                          self.endpoint)
            raise KempTechApiError(response.text)
        except exceptions.URLRequired:
            log.exception("%s is not a valid URL to make a request with.",
                          cmd_url)
            raise KempTechApiError(response.text)
        except exceptions.TooManyRedirects:
            log.exception("Too many redirects with request to %s", cmd_url)
            raise KempTechApiError(response.text)
        except exceptions.Timeout:
            log.exception("A connection error occurred to %s", self.endpoint)
            raise KempTechApiError(response.text)
        except exceptions.HTTPError:
            log.exception("A HTTP error occurred with request to %s", cmd_url)
            raise KempTechApiError(response.text)
        except exceptions.RequestException:
            log.exception("An unknown error occurred with request to %s",
                          cmd_url)
            raise KempTechApiError(response.text)
        return response.text

    def _get(self, rest_command, parameters):
        return self._do_request('GET', rest_command, parameters)

    def _post(self, rest_command, file):
        return self._do_request('POST', rest_command, file=file)


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
        response = self._get('set', parameters)
        return ApiXmlHelper.is_successful(response)

    def get_parameter(self, parameter):
        parameters = {
            'param': parameter,
        }
        response = self._get('get', parameters)
        value = ApiXmlHelper.get_data_field(response, parameter)
        if isinstance(value, dict):
            # This converts HTML to an awful one string disaster.
            value = "".join("{!s}={!r}".format(key, val) for (key, val) in
                            value.items())
        return value

    def update_firmware(self, file):
        response = self._post('installpatch', file)
        return ApiXmlHelper.is_successful(response)


class KempTechApiError(Exception):
    """Raised if HTTP request has failed."""

    def __init__(self, msg=None, code=None):
        if msg is not None:
            message = ApiXmlHelper.get_error_msg(msg)
        else:
            if code == 400:
                message = "Mandatory parameter missing from request."
            elif code == 401:
                message = "Username or password is missing or is incorrect."
            elif code == 403:
                message = "Incorrect permissions."
            elif code == 404:
                message = "Not found."
            elif code == 405:
                message = "Unknown command."
            else:
                message = "An unknown error has occurred."
        super(KempTechApiError, self).__init__(message)


class ApiXmlHelper(object):
    """Encapsulate the awful XML response and provide helpful functions."""
    @classmethod
    def get_success_msg(cls, xml):
        return cls._get_xml_field(xml, "Success")

    @classmethod
    def get_error_msg(cls, xml):
        return cls._get_xml_field(xml, "Error")

    @classmethod
    def is_successful(cls, xml):
        """Return True if request was successful, else return Error msg."""
        if ApiXmlHelper.get_success_msg(xml):
            return True
        else:
            return ApiXmlHelper.get_error_msg(xml)

    @classmethod
    def get_data_field(cls, xml, field):
        return cls._get_xml_field(xml, "Data", data_field=field)

    @classmethod
    def parse_to_dict(cls, xml):
        """Return the XML as an OrderedDict."""
        return xmltodict.parse(xml)

    @classmethod
    def _get_xml_field(cls, xml, field, data_field=None):
        xml_dict = xmltodict.parse(xml)
        try:
            if data_field is None:
                msg = xml_dict.get("Response").get(field)
            else:
                data = xml_dict.get("Response").get("Success").get(field)
                msg = data.get(data_field)
        except KeyError:
            return False
        return msg
