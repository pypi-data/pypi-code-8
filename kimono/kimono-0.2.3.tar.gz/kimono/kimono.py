import requests

__all__ = ['Kimono']

BASE = 'https://www.kimonolabs.com'

RETRIEVE_API = '{BASE_URL}/kimonoapis/{API_ID}?apikey={API_KEY}'
LIST_APIS = '{BASE_URL}/kimonoapis?apikey={API_KEY}'


class KimonoError(Exception):
    '''Base class for kimono errors'''
    def __init__(self, response):
        super(KimonoError, self).__init__(response)
        self.response = response

    def __str__(self):
        return self.response.get('message', 'No error provided.')


class Kimono(object):
    def __init__(self, apikey=None, apiid=None):
        self.apikey = apikey
        self.apiid = apiid

    @staticmethod
    def _get_request(url):
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise KimonoError(response.json())

    def retrieve_api(self):
        '''Returns an API object matching a specific API id'''
        return self._get_request(RETRIEVE_API.format(BASE_URL=BASE,
            API_ID=self.apiid,
            API_KEY=self.apikey))

    def list_apis(self):
        '''Returns a list of all APIs for the specified user'''
        return self._get_request(LIST_APIS.format(BASE_URL=BASE,
            API_KEY=self.apikey))
