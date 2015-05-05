# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client.exceptions.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Runtime exceptions thrown by package.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""
import arrow



class ProdiguerClientException(Exception):
    """Default package exception class.

    """
    def __init__(self, msg):
        """Object constructor.

        """
        self.message = unicode(msg)
        self.timestamp = unicode(arrow.get())


    def __str__(self):
        """Returns a string representation.

        """
        return "IPSL PRODIGUER EXCEPTION : {0}".format(repr(self.message))


class WebServiceException(ProdiguerClientException):
    """Web service exception class.

    """
    def __init__(self, endpoint, response):
        """Object constructor.

        """
        super(WebServiceException, self).__init__(response['error'])

        self.endpoint = endpoint
        self.error_type = response['errorType']


    def __str__(self):
        """Returns a string representation.

        """
        text = """
        IPSL PRODIGUER WEB SERVICE API EXCEPTION :
        \tTimestamp = {0}
        \tEndpoint = {1}
        \tError = {2}
        \tError Type = {3}
        """

        text = text.format(
            self.timestamp,
            self.endpoint,
            self.message,
            self.error_type
            )

        return text
