import requests

__all__ = ['Kimono']

BASE_URL = 'https://www.kimonolabs.com'

API_DATA = '{base_url}/api/{api_id}?apikey={api_key}'
API_ONDEMAND_DATA = '{base_url}/api/ondemand/{api_id}?apikey={api_key}'
RETRIEVE_API = '{base_url}/kimonoapis/{api_id}?apikey={api_key}'
LIST_APIS = '{base_url}/kimonoapis?apikey={api_key}'


class KimonoError(Exception):
    '''Base class for kimono errors'''
    def __init__(self, response):
        super(KimonoError, self).__init__(response)
        self.response = response

    def __str__(self):
        return self.response.get('message') \
        if self.response.has_key('message') \
        else self.response.get('error', 'No error provided.')


class Kimono(object):
    def __init__(self, apikey=None, apiid=None, ondemand=False):
        self.apikey = apikey
        self.apiid = apiid
        self.ondemand = ondemand

    @staticmethod
    def _get_request(url):
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise KimonoError(response.json())

    def api_data(self):
        '''Returns the data fetched by kimono APIs'''
        if self.ondemand:
            return self._get_request(API_ONDEMAND_DATA.format(
                base_url=BASE_URL,
                api_id=self.apiid,
                api_key=self.apikey))
        else:
            return self._get_request(API_DATA.format(base_url=BASE_URL,
                api_id=self.apiid,
                api_key=self.apikey))

    def retrieve_api(self):
        '''Returns an API object matching a specific API id'''
        return self._get_request(RETRIEVE_API.format(base_url=BASE_URL,
            api_id=self.apiid,
            api_key=self.apikey))

    def list_apis(self):
        '''Returns a list of all APIs for the specified user'''
        return self._get_request(LIST_APIS.format(base_url=BASE_URL,
            api_key=self.apikey))
