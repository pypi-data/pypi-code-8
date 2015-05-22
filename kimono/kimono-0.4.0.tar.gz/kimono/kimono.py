import requests


class KimonoError(Exception):
    '''Base class for kimono errors'''
    def __init__(self, response):
        super(KimonoError, self).__init__(response)
        self.response = response

    def __str__(self):
        return self.response.get('message') \
            if 'message' in self.response \
            else self.response.get('error', 'No error provided.')


class Magic(object):
    def __init__(self, apikey, apiid, api_path, endpoint):
        self.apikey = apikey
        self.apiid = apiid
        self.api_path = api_path
        self.endpoint = endpoint

    def __getattr__(self, method):
        def wrapper(data={}, action=None):
            url = self._build_url(endpoint=self.endpoint,
                                  action=action,
                                  method=method)
            if data or action == 'startcrawl':
                data.update({'apikey': self.apikey})
            response = self._request(url=url,
                                     method=method,
                                     data=data)
            return response
        return wrapper

    def _build_url(self, endpoint, action, method):
        url = self.api_path + endpoint
        if self.apiid:
            url = url + '/' + str(self.apiid)
        if self.apikey and method == 'get':
            url = url + '?apikey=' + self.apikey
        if action:
            url = url + '/' + action
        return url

    def _request(self, url, method, data):
        make_request = getattr(requests, method)
        response = make_request(url=url,
                                data=data)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise KimonoError(response.json())


class Kimono(object):
    def __init__(self, apikey, apiid=None):
        self.apikey = apikey
        self.apiid = apiid
        self.api_path = 'https://www.kimonolabs.com/'

    def __getattr__(self, endpoint):
        apikey = self.apikey
        apiid = self.apiid
        api_path = self.api_path
        return Magic(apikey, apiid, api_path, endpoint)
