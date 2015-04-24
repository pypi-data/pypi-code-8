
import json

class Resource(object):

    def __init__(self, client=None):
        self._data = {}
        self._client = client

    def update(self, data):
        self._data.update(data)

    def get(self):
        r = self._client._get(self.url%self, stream=False)
        assert 200 <= r.status_code and r.status_code <= 300
        d = json.loads(r.text)
        self._data = d
        return d

    def put(self, update=False):
        url = self.url%self

        print "put at %s"%url
        r = self._client._put(url, stream=False, update=update, data=json.dumps(self._data))

        print "result",r, r.text
        assert 200 <= r.status_code and r.status_code <= 300

    def view_short(self):
        return self.view_simple()

    def view_simple(self):
        return self.view_full()

    def view_full(self):
        return json.dumps(self._data, indent=2)

    def __getitem__(self, key):
        return self._data[key]

    def __getattr__(self, name):
        if name not in self._data:
            raise AttributeError(name)
        return self._data[name]


class ROResource(Resource):
    def put(self):
        raise RuntimeError("not implemented")


