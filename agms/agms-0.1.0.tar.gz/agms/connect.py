from __future__ import absolute_import
from agms.util.parser import Parser
from agms.exception.authentication_exception import AuthenticationException
from agms.exception.authorization_exception import AuthorizationException
from agms.exception.down_for_maintenance_exception import DownForMaintenanceException
from agms.exception.not_found_exception import NotFoundException
from agms.exception.server_error_exception import ServerErrorException
from agms.exception.unexpected_exception import UnexpectedException
from agms.exception.upgrade_required_exception import UpgradeRequiredException


class Connect(object):
    @staticmethod
    def is_exception_status(status):
        return status not in [200, 201, 422]

    @staticmethod
    def raise_exception_from_status(status, message=None):
        if status == 401:
            raise AuthenticationException()
        elif status == 403:
            raise AuthorizationException(message)
        elif status == 404:
            raise NotFoundException()
        elif status == 426:
            raise UpgradeRequiredException()
        elif status == 500:
            raise ServerErrorException()
        elif status == 503:
            raise DownForMaintenanceException()
        else:
            raise UnexpectedException("Unexpected HTTP_RESPONSE " + str(status))

    def __init__(self, config):
        self.config = config

    def connect(self, url, request, request_method, response_object):
        headers = self.__build_headers(request_method)
        request_body = self.__build_request(request, request_method)
        response_body = self.post(url, headers, request_body)
        return response_body

    def post(self, url, headers=None, request_body=None):
        return self.__http_do("POST", url, headers, request_body)

    def delete(self, url, headers=None, request_body=None):
        return self.__http_do("DELETE", url, headers, request_body)

    def get(self, url, headers=None, request_body=None):
        return self.__http_do("GET", url, headers, request_body)

    def put(self, url, headers=None, request_body=None):
        return self.__http_do("PUT", url, headers, request_body)

    def __http_do(self, http_verb, url, headers=None, request_body=None):
        http_client = self.config.http_client()
        status, response_body = http_client.http_do(http_verb, url, headers, request_body)

        if Connect.is_exception_status(status):
            Connect.raise_exception_from_status(status)
        else:
            if len(response_body.strip()) == 0:
                return {}
            else:
                return self.__parse_response(response_body)

    def __build_headers(self, request_method):
        # Shited to module block to ensure we avoid circular dependencies
        from agms.agms import Agms

        return {
            "Accept": "application/xml",
            "Content-type": "text/xml; charset=utf-8",
            "User-Agent": "(Agms Python " + Agms.get_library_version() + ")",
            "X-ApiVersion": Agms.get_api_version(),
            "SOAPAction": "https://gateway.agms.com/roxapi/" + request_method
        }

    def __build_request(self, request, request_method):
        header = """<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
            """
        header_line = '<' + request_method + ' xmlns="https://gateway.agms.com/roxapi/">'
        body = self.__dict_to_xml(request)
        footer_line = '</' + request_method + '>'
        footer = """</soap:Body>
            </soap:Envelope>"""
        return header + header_line + body + footer_line + footer

    def __dict_to_xml(self, request):
        data = ''
        for key, value in request.items():
            if value != '':
                try:
                    # Open Tag
                    data = data + "<" + key + ">"
                    # Check whether value is still a dict
                    if isinstance(value, dict):
                        value = self.__dict_to_xml(value)
                    # Add Data
                    data = data + str(value)
                    # Close Tag
                    data = data + "</" + key + ">"
                except Exception as e:
                    pass
        return data

    def __parse_response(self, xml):
        return Parser(xml).parse()
