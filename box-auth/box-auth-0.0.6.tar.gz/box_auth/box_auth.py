__author__ = 'jsterling'
import re
import getpass
import json
import datetime
import argparse
from http_client import HttpClient
import logging
import sys


class BoxAuth(object):

    DEFAULT_REDIRECT_URI = "http://localhost"

    def __init__(self, client_id, client_secret, username, password, redirect_uri=None, http_client=None, log=None):
        self._client_id = client_id
        self._client_secret = client_secret

        self._access_token = None
        self._refresh_token = None
        self._access_token_expiration = None
        self._refresh_token_expiration = None
        self._username = username
        self._password = password
        self._redirect_uri = redirect_uri or self.DEFAULT_REDIRECT_URI
        self._http_client = http_client or HttpClient()
        self._log = log or logging.getLogger()

    def get_access_token(self):
        """
        :return str:
        """
        if self._is_access_token_expired():
            if not self._generate_new_tokens():
                self._log.critical("Unable to log in to Box")
        return self._access_token

    def _generate_new_tokens(self):
        """
        :return bool:
        """
        self._access_token = None
        self._access_token_expiration = None
        self._refresh_token = None
        self._refresh_token_expiration = None
        return self._get_access_tokens()

    def _login(self, state):
        url = self._http_client.url('https://app.box.com/api/oauth2/authorize', {
            "response_type": "code",
            "client_id": self._client_id,
            "state": state,
            "redirect_uri": self._redirect_uri
        })
        login_body = {
            "login":                      self._username,
            "password":                   self._password,
            "login_submit":               "Authorizing...",
            "dologin":                    "1",
            "client_id":                  self._client_id,
            "response_type":              "code",
            "redirect_uri":               self._redirect_uri,
            "scope":                      "root_readwrite",
            "folder_id":                  "",
            "file_id":                    "",
            "state":                      state,
            "reg_step":                   "",
            "submit1":                    "1",
            "folder":                     "",
            "login_or_register_mode":     "login",
            "new_login_or_register_mode": "",
            "__login":                    "1",
            # Skip a GET on the page and dont have the RT the first time.
            # this works anyway
            #"request_token",              "44bccf0747cd3e97a1018600bbd599383895500f69c0d541f6732b2ac081debf",
            "_pw_sql": ""
        }
        return self._http_client.post_form(url, login_body)

    def _grant(self, state, login_response_headers, content):
        ic, request_token = self._extract_ic_and_request_token(content)
        url = 'https://app.box.com/api/oauth2/authorize'
        grant_post_data = {
            "client_id":      self._client_id,
            "response_type":  "code",
            "redirect_uri":   self._redirect_uri,
            "scope":          "root_readwrite",
            "file_id":        "",
            "state":          state,
            "doconsent":      "doconsent",
            "ic":             ic,
            "consent_accept": "Grant+access+to+Box",
            "request_token":  request_token,
        }
        headers = {
            'Cookie': login_response_headers['set-cookie']
        }
        return self._http_client.post_form(url, grant_post_data, headers)

    def _get_access_tokens(self):
        """:return bool: True when tokens successfully acquired, False otherwise"""
        state = "state"
        success = False
        login_response_headers, content = self._login(state)
        if login_response_headers['status'] == '200':
            if "There seems to be a problem with this app." in content:
                self._log.debug("There is a box config issue. Check redirect uri")
            else:
                grant_response_headers, content = self._grant(state, login_response_headers, content)
                if grant_response_headers['status'] == '302' and 'location' in grant_response_headers:
                    redirect = grant_response_headers['location']
                    access_code = self._http_client.query_params(redirect)['code']
                    success = self._trade_access_code_for_token(access_code)
                else:
                    self._log.debug("BAD RESPONSE FROM BOX ON GRANT\n{}\n{}".format(grant_response_headers, content))
        else:
            self._log.debug("ERROR Logging in to box HTTP {}:\n{}".format(login_response_headers['status'], content))

        return success

    def _trade_access_code_for_token(self, access_code):
        """
        :param str access_code:
        :return bool:
        """
        url = 'https://api.box.com/oauth2/token'
        post_data = {
            "grant_type":    "authorization_code",
            "code":          access_code,
            "client_id":     self._client_id,
            "client_secret": self._client_secret,
            "redirect_uri":  self._redirect_uri
        }
        resp, content = self._http_client.post_form(url, post_data)
        if resp['status'] == '200':
            box_json = json.loads(content)
            self._access_token = box_json['access_token']
            self._access_token_expiration = datetime.datetime.now() + datetime.timedelta(hours=1)
            self._refresh_token = box_json['refresh_token']
            self._refresh_token_expiration = datetime.datetime.now() + datetime.timedelta(seconds=box_json['expires_in'])
            return True
        else:
            return False

    def _expired(self, date):
        """
        :param  datetime.datetime date:
        :return bool:
        """
        return date and (date - datetime.datetime.now()).total_seconds() < 1

    def _extract_ic_and_request_token(self, content):
        """
        Example request token:
        var request_token = '4f12a9401c227a6533efe689b5e9cdb0c9a5d32af08c0af917e3418a577cf94e';

        Example ic:
        <input type="hidden" name="ic" value="a700791197d122a306a6002f9bfafb240975171fc4b11f75221e0c86512e99b7" />

        :param content:
        :return str, str:
        """
        ic = None
        request_token = None
        ic_groups = re.search('name="ic" value="([A-Za-z0-9]{64})', content)
        if ic_groups:
            ic = ic_groups.groups(0)[0]

        request_token_groups = re.search("request_token = '([A-Za-z0-9]+)'", content)
        if request_token_groups:
            request_token = request_token_groups.groups(0)[0]

        return ic, request_token

    def _is_access_token_expired(self):
        """:return bool:"""
        return self._access_token_expiration is None or self._expired(self._access_token_expiration)

    def _is_token_expired(self):
        """:return bool:"""
        return self._refresh_token_expiration is None or self._expired(self._refresh_token_expiration)


class BoxAuthTester(object):

    OPTIONS = ['client-id', 'client-secret', 'username', 'password']

    def test(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--client-id", help="client id", dest='client_id')
        parser.add_argument("--client-secret", help="client secret", dest='client_secret')
        parser.add_argument("--username", help="email")
        parser.add_argument("--password", help="password")
        args = parser.parse_args()
        options = {
            'client-id': args.client_id or None,
            'client-secret': args.client_secret or None,
            'username': args.username or None,
            'password': args.password or None,
        }

        if self._has_stdin():
            stdin_data = json.loads(''.join(sys.stdin.readlines()))
            for option in BoxAuthTester.OPTIONS:
                if option in stdin_data and options[option] is None:
                    options[option] = stdin_data[option]

        client_id = options['client-id'] or input("Api key: ")
        client_secret = options['client-secret'] or getpass.getpass("Api secret: ")
        username = options['username'] or input("Username: ")
        password = options['password'] or getpass.getpass("Password: ")

        box_auth = BoxAuth(client_id, client_secret, username, password)
        access_token = box_auth.get_access_token()
        print({
            "access_token": access_token,
            "refresh_token": box_auth._refresh_token,
        })

    def _has_stdin(self):
        """:return bool: True if there is stuff on stdin, false otherwise"""
        return not sys.stdin.isatty()

if __name__ == "__main__":
    tester = BoxAuthTester()
    tester.test()