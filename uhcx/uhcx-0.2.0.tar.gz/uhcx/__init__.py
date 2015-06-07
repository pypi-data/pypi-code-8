"""
Python library for the uh.cx link shortener.

http://uh.cx/
"""

import json

import requests


class Manager:
    _url = 'http://uh.cx/api/create'

    class Link:
        url_original = ''
        url_redirect = ''
        url_preview = ''
        qr_redirect = ''
        qr_preview = ''

    class InvalidResponseException(Exception):
        pass

    class CouldNotCreateLinkException(Exception):
        pass

    class ResponseValidator:
        _keys = ['QrDirect', 'QrPreview', 'UrlDirect', 'UrlOriginal', 'UrlPreview']

        @staticmethod
        def check(response):
            for key in Manager.ResponseValidator._keys:
                if key not in response:
                    return False

            return True

    @staticmethod
    def create(url):
        data = json.dumps({'url': url})
        response = requests.post(Manager._url, data)

        if response.status_code != 200:
            raise Manager.CouldNotCreateLinkException()

        response_data = response.json()

        if not Manager.ResponseValidator.check(response_data):
            raise Manager.InvalidResponseException()

        link = Manager.Link()
        link.qr_preview = response_data['QrPreview']
        link.qr_redirect = response_data['QrDirect']
        link.url_original = response_data['UrlOriginal']
        link.url_preview = response_data['UrlPreview']
        link.url_redirect = response_data['UrlDirect']

        return link
