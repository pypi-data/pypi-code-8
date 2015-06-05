
import re
import ssl
import sys
import json
import base64

import urllib2
import urllib
from cookielib import CookieJar

from httplib import HTTPSConnection

from pyngdomdriver import PyngdomDriver

__version__ = '0.1.1'

if sys.version_info >= (2, 7, 9):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE


class Pyngdom(object):
    def __init__(self, username, password, apikey, account, version='2.0'):
        self.username = username
        self.password = password
        self.apikey = apikey
        self.account = account
        self.version = version

    def request(self, method, endpoint, headers=None, **params):

        url = "https://api.pingdom.com/api/{version}/{endpoint}".format(
            **dict(
                username=self.username, password=self.password,
                version=self.version, endpoint=endpoint
            )
        )

        if headers is None:
            headers = dict()

        if 'Account-Email' not in headers:
            headers['Account-Email'] = self.account
        if 'App-Key' not in headers:
            headers['App-Key'] = self.apikey
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        if 'Authorization' not in headers:
            headers['Authorization'] = 'Basic %s' % base64.encodestring(
                "{username}:{password}".format(username=self.username, password=self.password)
            )

        conn = HTTPSConnection('api.pingdom.com', context=ctx)
        conn.request(
            method,
            "/api/{version}/{endpoint}".format(version=self.version, endpoint=endpoint),
            headers=headers
        )

        response = conn.getresponse()
        body = response.read()
        return json.loads(body)

    def get_check_list(self):
        return self.request('GET', 'checks')

    def get_detailed_check_information(self, checkid):
        return self.request('GET', 'checks/%s' % checkid)

    def get_summary_performance(self, checkid, **params):
        headers = {}
        for header in ['includeuptime', 'from', 'to', 'order', 'resolution', 'probes']:
            if header in params:
                headers[header] = params.pop(header)

        return self.request('GET', 'summary.performance/%s' % checkid, headers=headers)


class PyngdomRum(object):
    def __init__(self, username, password, apikey=None, account=None):

        self.username = username
        self.password = password
        self.apikey = apikey
        self.account = account
        self.opener = None

    def start(self):
        self.login()

    def quit(self):
        pass

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def login(self):
        cj = CookieJar()
        rc = re.compile('''.*name *=[ '"]*__csrf_magic[^>]+?value *?=[ '"]*?(?P<csrf>[^'"; ]+)''')

        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        body = self.opener.open("https://my.pingdom.com/")

        csrf_magic = filter(None, map(rc.match, body))[0].groupdict().get('csrf')

        login_response = self.opener.open("https://my.pingdom.com/", urllib.urlencode(
            {'__csrf_magic': csrf_magic, 'password': self.password, 'email': self.username})
        )
        login_response.read()
        return login_response

    def realtime_rum(self, checkid, sample_interval=60):
        raise NotImplemented("PyngdomRum does not have a realtime method")

    def today_rum(self, checkid):
        response = self.opener.open("https://my.pingdom.com/rum/%s#filter&timetype=average&datefilter=today" % checkid)
        rc = re.compile(r".*Pingdom.rum.aggregatedData *= *(?P<rum_data>.+);")

        return json.loads(filter(None, map(rc.match, response)).pop(0).groupdict().get('rum_data'))
