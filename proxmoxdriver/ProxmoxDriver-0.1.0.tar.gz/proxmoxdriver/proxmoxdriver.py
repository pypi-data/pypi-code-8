""" Module: ProxmoxDriver """

import re
import requests
import time

requests.packages.urllib3.disable_warnings()


class ProxmoxDriver:

    def __init__(self, host, port=8006):
        self.host = host
        self.port = port
        self.cookie = {}
        self.root = 'https://%s:%s/api2/json' % (host, port)
        self.update_headers()

    # REST methods

    def get(self, path):
        return requests.get(
            '%s/%s' % (self.root, path),
            verify=False,
            cookies=self.cookie
        ).json()

    def post(self, path, data=None):
        return requests.post(
            '%s/%s' % (self.root, path),
            data=data,
            verify=False,
            cookies=self.cookie,
            headers=self.headers
        ).json()

    def put(self, path, data=None):
        return requests.put(
            '%s/%s' % (self.root, path),
            data=data,
            verify=False,
            cookies=self.cookie,
            headers=self.headers
        ).json()

    def delete(self, path, data=None):
        return requests.delete(
            '%s/%s' % (self.root, path),
            data=data,
            verify=False,
            cookies=self.cookie,
            headers=self.headers
        ).json()

    # ticket handler

    def get_ticket(self, username, password, realm='pam'):
        data = {
            'username': '%s@%s' % (username, realm),
            'password': password
        }
        response = self.post('access/ticket', data)
        if response['data'] is not None:
            self.csrf = response['data']['CSRFPreventionToken']
            self.cookie = {'PVEAuthCookie': response['data']['ticket']}
            self.update_headers()
            return True, response

        return False, response

    def set_ticket(self, ticket, csrf):
        self.csrf = csrf
        self.cookie = {'PVEAuthCookie': ticket}

    # helper methods

    def update_headers(self):
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            self.headers['CSRFPreventionToken'] = self.csrf
        except:
            pass

    def lock(self, response):
        try:
            data = response['data']
            node = re.search(r'^UPID:([a-z0-9]+):.*', data)
        except:
            return response

        if node is None:
            return response

        while True:
            time.sleep(1)
            s = self.get('nodes/%s/tasks/%s/status' % (node.group(1), data))
            try:
                if s['data']['status'] == 'stopped':
                    break
            except:
                pass

        return 'Done'
