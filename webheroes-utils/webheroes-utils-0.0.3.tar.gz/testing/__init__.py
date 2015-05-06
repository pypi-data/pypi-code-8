
#
# WebHeroes-Utils -- Web Heroes Inc. python utility module
#
# Copyright (c) 2015, Web Heroes Inc..
#
# WebHeroes-Utils is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.  See the LICENSE file at the top of the source tree.
#
# WebHeroes-Utils is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#

__author__                      = "Matthew Brisebois"
__email__                       = "matthew@webheroes.ca"
__copyright__                   = "Copyright (c) 2015 Web Heroes Inc."
__license__                     = "Dual License: GPLv3 (or later) and Commercial (see LICENSE)"

__all__				= ["api_session", "api"]

from ..discovery	import get_docker_ip
import requests, json, random

mongrel2_ip		= get_docker_ip('mg2')
apiurl			= "http://{0}".format(mongrel2_ip)

class api_session(object):

    def __init__(self, cookies=None, test=False):
        self.test		= test
        self.session		= requests.Session()
        if cookies is not None:
            self.session.cookies.update(cookies)

    def api(self, *args, **kwargs):
        kwargs.setdefault('test', self.test)
        kwargs['session']	= self.session
        return api(*args, **kwargs)

class api(dict):

    def __init__(self, path, test=True, expect_failure=False, session=None, **kwargs):
        self.path		= path.strip('/')
        self.error		= None
        self.status		= None
        self.test		= test
        self.data		= kwargs.get('data', None)
        self.params		= kwargs.setdefault('params', {})
        self.timeout		= kwargs.setdefault('timeout', 1)
        self.cookies		= kwargs.get('cookies')

        if self.data is not None:
            if type(self.data) is str:
                self.data	= json.loads(self.data)
            else:
                kwargs['data']	= json.dumps(self.data)
        
        if self.test is True:
            self.params['__test__']	= True

        url			= "/".join([apiurl,"api",self.path])
        if session is None:
            self.req		= requests.get(url, **kwargs)
            self.cookies	= self.req.cookies
        else:
            self.req		= session.get(url, **kwargs)
            self.cookies	= session.cookies

        reply			= json.loads(self.req.text)
        if type(reply) is dict:
            self.status		= True
            self.update( reply )
        else:
            self.status		= reply

        if expect_failure is False and self.get('error') is not None:
            print json.dumps(self, indent=4)
            raise Exception("Request failed and was not expected to.")
        elif expect_failure is True and self.get('error') is None:
            print json.dumps(self, indent=4)
            raise Exception("Request did NOT fail and was expected to.")

    def has_contents(self, data):
        match		= True
        absent		= False
        for k,v in data.items():
            if v is True or v is False or v is None:
                if self.get(k,1) is 1:
                    absent	= True
                if self.get(k,1) is not v and v != "__keyonly__":
                    match	= False
            else:
                if self.get(k) is None:
                    absent	= True
                if self.get(k) != v and v != "__keyonly__":
                    match	= False
            if absent is True:
                self.error	= "Reply key '{0}' not in response".format(k)
                return False
            if match is False:
                self.error	= "Reply key '{0}' did not match: received {1} == {2} expected".format(k, self.get(k), v)
                return False
        return True

    def has_cookie(self, key, match=None):
        if match is None:
            return self.cookies.get(key) is not None
        else:
            return self.cookies.get(key) == str(match)
    
    def random_key(self, t=None):
        keys			= self.keys()
        random.shuffle( keys )
        return keys.pop() if t is None else t(keys.pop())
    
    def random(self):
        return self[ self.random_key() ]

    def dump(self):
        return json.dumps(self, indent=4)
