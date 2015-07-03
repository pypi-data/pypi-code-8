import urllib
import urllib2
import json


class SummicsApi:

    host = 'https://api.summics.com'

    endpoints = {
        'authenticate': {
            'url': '/auth',
            'method': 'post'
        },
        'projects': {
            'url': '/projects'
        },
        'topics': {
            'url': '/topics'
        },
        'topicsOverview': {
            'url': '/topics/overview'
        },
        'texts': {
            'url': '/texts'
        },
        'dashboard': {
            'url': '/dashboard'
        },
        'addTexts': {
            'url' : '/texts',
            'method': 'put',
            'Content-Type': 'application/json'
        }
    }

    def __init__(self, client_id, client_secret, host=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.host = host if host else SummicsApi.host

    def _request(self, endpoint, param_dict=None, **params):
        assert(endpoint in SummicsApi.endpoints)

        endpoint = SummicsApi.endpoints[endpoint]

        param_dict = param_dict if param_dict else {}

        url = self.host + endpoint['url']
        data = None
        headers = {'Content-Type': endpoint['Content-Type'] if 'Content-Type' in endpoint else 'application/x-www-form-urlencoded'}

        params.update(param_dict)

        if len(params) > 0:
            if endpoint.get('method') == 'post':
                data = urllib.urlencode(params, True)
            elif endpoint.get('method') == 'put':
                data = json.dumps(params)
            else:
                qs = urllib.urlencode(params, True)
                url += '?' + qs

        if self.token:
            headers['Authorization'] = self.token

        req = urllib2.Request(url, data, headers)

        if endpoint.get('method') == 'put':
            req.get_method = lambda: "PUT"

        res = urllib2.urlopen(req)
        return json.load(res)

    def _authenticate(self):
        if not self.token:
            res = self._request('authenticate', clientId=self.client_id, secret=self.client_secret)
            self.token = res['token']

    def projects(self):
        self._authenticate()
        return self._request('projects')

    def topics(self, project_id):
        self._authenticate()
        return self._request('topics', projectId=project_id)

    def topicsOverview(self, sources, date_from, date_to):
        self._authenticate()
        params = {
            'sources[]': sources,
            'fromDate': date_from.strftime('%Y-%m-%d'),
            'toDate': date_to.strftime('%Y-%m-%d')
        }
        return self._request('topicsOverview', params)

    def texts(self, sources, date_from, date_to, topics=None):
        self._authenticate()
        params = {
            'sources[]': sources,
            'fromDate': date_from.strftime('%Y-%m-%d'),
            'toDate': date_to.strftime('%Y-%m-%d'),
            'topics[]': topics if topics else []
        }
        return self._request('texts', params)

    def dashboard(self, sources, date_from, date_to):
        self._authenticate()
        params = {
            'sources[]': sources,
            'fromDate': date_from.strftime('%Y-%m-%d'),
            'toDate': date_to.strftime('%Y-%m-%d')
        }
        return self._request('dashboard', params)

    def addTexts(self, source, texts):
        self._authenticate()

        return self._request('addTexts', {"sourceId": source, "texts": texts})



