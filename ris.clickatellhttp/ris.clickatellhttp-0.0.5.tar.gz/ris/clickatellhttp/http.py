"""
Copyright 2013 Rwizi Information Systems

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import re
import urllib
import urllib2

CLICKATELL_MAX_RECIPIENTS = 100  # Max recipients for batch messages (v2.5.3 HTTP API)

CLICKATELL_MESSAGE_STATUS_CODES = {
    '001': 'Message Unknown',
    '002': 'Message Queued',
    '003': 'Delivered to Gateway',
    '004': 'Received by Recipient',
    '005': 'Error with Message',
    '006': 'User Cancelled Delivery',
    '007': 'Error Delivering Message',
    '008': 'OK',
    '009': 'Routing Error',
    '010': 'Message Expired',
    '011': 'Message Queued for Later Delivery',
    '012': 'Out of Credit',
    '014': 'Maximum MT Limit Exceeded'
}

CLICKATELL_ERROR_CODES = {
    '001': 'Authentication Failed',
    '002': 'Unknown Username or Password',
    '003': 'Session ID Expired',
    '005': 'Missing Session ID',
    '007': 'IP Lockdown Violation',
    '101': 'Invalid or Missing Parameters',
    '102': 'Invalid User Data Header',
    '103': 'Unknown API Message ID',
    '104': 'Unknown Client Message ID',
    '105': 'Invalid Destination Address',
    '106': 'Invalid Source Address',
    '107': 'Empty Message',
    '108': 'Invalid or Missing API ID',
    '109': 'Missing Message ID',
    '113': 'Maximum Message Parts Exceeded',
    '114': 'Cannot Route Message',
    '115': 'Message Expired',
    '116': 'Invalid Unicode Data',
    '120': 'Invalid Delivery Time',
    '121': 'Destination Mobile Number Blocked',
    '122': 'Destination Mobile Opted Out',
    '123': 'Invalid Sender ID',
    '128': 'Number Delisted',
    '130': 'Maximum MT limit Exceeded Until <UNIX TIME STAMP>',
    '201': 'Invalid Batch ID',
    '202': 'No Batch Template',
    '301': 'No Credit Left',
    '901': 'Internal Error'
}


class ClickatellClient(object):
    """
    The ClickatellClient implements the Clickatell HTTP/HTTPS API for sending
    SMS messages using the Clickatell SMS Gateway as specified in v2.5.3

    https://www.clickatell.com/downloads/http/Clickatell_HTTP.pdf

    Attributes:
        MAX_RECIPIENTS (int): Maximum message recipients per request
        MESSAGE_STATUS (dict): Message delivery status codes and mappings
        ERROR_CODES (dict): Clickatell error codes and their mapping

        api_id (str): Clickatell API ID
        username (str): Clickatell username
        password (str): Clickatell password
        protocol (str): HTTP/HTTPS (insecure/secure)
        session_id (str): Session ID received after authentication with API server

        __INT_HEX_RE: Regex to match alphanumerical characters in a string
        __login(): Authenticate the client and set the session ID
        __fetch_url_response(): Fetch a URL resource

        send(): Send a message
        status(): Get the delivery status of a message
    """

    MAX_RECIPIENTS = 100  # As per v2.5.3 HTTP API

    def __init__(self, api_id, username, password, secure=False):
        self.api_id = api_id
        self.username = username
        self.password = password
        self.session_id = None
        self.protocol = 'https' if secure else 'http'
        self.__INT_HEX_RE = re.compile('([0-9a-f]+)')  # match hex and 'int' string
        self.__INT_RE = re.compile('([0-9]+)')
        self.__login()

    def __fetch_url_response(self, url):
        """
        Internal wrapper for fetching URL responses

        Raises:
            URLError:

        Returns:
            response (str): response from URL call
        """

        try:
            response = urllib2.urlopen(url).read()
        except urllib2.URLError:
            response = ''

        return response

    def __login(self):
        """
        Sends an auth request to Clickatell to get a session ID for later use.
        """

        login_url = '%s://api.clickatell.com/http/auth?api_id=%s&user=%s' \
                    '&password=%s' % (self.protocol, self.api_id, self.username,
                                      self.password)

        response = self.__fetch_url_response(login_url)

        if response.startswith('OK'):  # We are authenticated, set the session_id
            self.session_id = response[4:]
        elif response.startswith('ERR'):  # Failed to login for some reason
            # Extract error code and raise exception
            raise ClickatellException(response[5:8])
        else:  # Empty response?
            raise Exception('Failed to connect to API server')

    def send(self, message, recipients):
        """
        Sends an SMS to 1 or more recipients

        Args:
            message (str): Message to be sent
            recipients (list): List of message recipients
            **kwargs: Extra Clickatell to be sent in the request

        Raises:
            Exception: General, descriptive exception

        Returns:
            dict: {
                'success':[
                    {
                        'id': 'message_id',
                        'recipient': 'message_recipient'
                    },
                ],
                'error':[
                    {
                        'error_code': 'error_code',
                        'error_description': 'error_description',
                        'recipient': 'message_recipient'
                    },
                ]
            }
        """

        # Sanity check, raise exception for empty calls
        if not message or not recipients:
            raise Exception('Empty message or recipient. Message cannot be sent')

        # Initialise lists were responses will be kept
        raw_responses = []
        success = []
        error = []

        """
        """

        for i in range(0, len(recipients), self.MAX_RECIPIENTS):
            batch = ','.join(recipients[i:i + self.MAX_RECIPIENTS])

            send_url = '%s://api.clickatell.com/http/sendmsg?session_id=%s&to=%s&text=%s' % \
                       (self.protocol, self.session_id, batch, urllib.quote(message))

            raw_responses.extend(self.__fetch_url_response(send_url).split('\n'))

        if len(raw_responses) == 0:  # No data received back
            raise Exception('Empty response received from Clickatell server')

        elif len(raw_responses) == 1:  # Single message sent
            single_response = raw_responses[0]

            if single_response.startswith('ID'):
                data = re.findall(self.__INT_HEX_RE, single_response)
                success.append({'id': data[0], 'recipient': recipients[0]})
            else:
                if single_response != '':
                    data = re.findall(self.__INT_RE, single_response)
                    error.append({'code': data[0], 'recipient': recipients[0],
                                  'description': CLICKATELL_ERROR_CODES[data[0]]})

        else:  # Multiple messages sent
            for raw_response in raw_responses:
                if raw_response.startswith('ID'):  # Message handled successfully
                    data = re.findall(self.__INT_HEX_RE, raw_response)
                    success.append({'id': data[0], 'recipient': data[1]})
                else:
                    if raw_response != '':  # Error processing message on gateway side
                        data = re.findall(self.__INT_RE, raw_response)
                        error.append({'code': data[0], 'recipient': data[1],
                                      'description': CLICKATELL_ERROR_CODES[data[0]]})

        return {'success': success, 'error': error}

    def status(self, message_id):
        """
        Get the status of a message that has been sent

        Args:
            message_id (str): Message id to be queried

        Returns:
            str: Delivery status code
        """

        status_url = '%s://api.clickatell.com/http/querymsg?session_id=%s&apimsgid=%s' % \
                     (self.protocol, self.session_id, message_id)

        response = self.__fetch_url_response(status_url)

        if response.startswith('ID'):
            # The response has the pattern 'ID: xxxx Status: xxxx'
            # Extract the id from the pattern

            return response[response.find('Status: ') + 8:]

        else:  # Extract the error code and description, raise exception
            return


class ClickatellException(Exception):
    """
    ClickatellException extends the base Exception class

    Attributes:
        code (int): Clickatell error code
    """

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return '%s: %s' % (self.code, CLICKATELL_ERROR_CODES[self.code])
