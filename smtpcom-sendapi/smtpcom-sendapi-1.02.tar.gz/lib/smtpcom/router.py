import os
import json
import requests

from argparse import ArgumentParser

from smtpcom.config import Config


class Router(object):

    _CONFIG_LOADED = False

    def __init__(self):
        self.__content_type = 'html'
        self.load_config()

    @classmethod
    def load_config(cls):
        if cls._CONFIG_LOADED:
            return

        parser = ArgumentParser('smtpcom-sendapi')
        parser.add_argument('-c', '--config', dest='config')
        args = parser.parse_args()

        if args.config:
            path = args.config
        else:
            path = os.path.join(os.path.dirname(__file__), '../../etc')

        try:
            Config.load('smtpcom_sendapi', default_path=path)
        except OSError:
            print "Config doesn't exists in %s" % path
            exit(0)
        cls._CONFIG_LOADED = True

    def get(self, data, method):
        url = self.get_url(method)
        self.add_auth(data)
        result = requests.get(url, params=data)
        return self.output(result)

    def is_json(self):
        return self.__content_type == 'json'

    def output(self, result):
        if self.is_json():
            try:
                res = json.loads(result.content)
                return res
            except ValueError:
                raise ValueError("Could not decode json object: %s" \
                    % result.content)
        return result.content

    def post(self, data, method, raw_data=False):
        url = self.get_url(method)
        self.add_auth(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        result = requests.post(url, data=json.dumps(data), headers=headers)
        if raw_data:
            return result.content
        else:
            return self.output(result)

    def get_url(self, flag):
        url = Config.get_url(flag)
        if self.is_json():
            url += '.json'
        return url

    def set_content_type(self, content_type):
        if content_type:
            if content_type not in ('json', '', 'html'):
                raise ValueError("Content Type could be html or json")
            self.__content_type = content_type

    def add_auth(self, data):
        key = Config.get('api_key')
        if not key:
            raise ValueError("ApiKey should not be blank")
        data['ApiKey'] = key
