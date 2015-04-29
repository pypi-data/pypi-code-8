import requests


# Use to grab paginated data as needed
class AsyncList(object):
    def __init__(self, data, link, requester, headers):
        self._backing = data
        self._link = link
        self._requester = requester
        self._headers = headers
        self._parser = None

    def __iter__(self):
        ind = 0
        try:
            while self[ind] and self._link is not None:
                yield self[ind]
                ind += 1
        except IndexError:
            raise StopIteration

    def __len__(self):
        return len(self._backing)

    def __getitem__(self, ind):
        while ind >= len(self._backing):
            self.retrieve_next()
            if self._link is None:
                break

        return self._backing[ind]

    def retrieve_next(self):
        if self._link is None:
            return
        next_section = self._requester.get_url(self._link, self._headers)
        try:
            if self._parser:
                self._parser(next_section, self._requester.cache)
            self._backing.extend(next_section._backing)
            self._link = next_section._link
        except AttributeError:
            self._backing.extend(next_section)
            self._link = None


class AsyncRequest(object):
    def __init__(self, retrieved=None):
        self.json = {}
        self.urls = {}
        self.retrieved = retrieved

    def get_url(self, url, headers):
        if url not in self.json:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if type(data) == list and "next" in response.links:
                    data = AsyncList(data, response.links["next"]["url"], self, headers)
                self.cache(url, data)
            else:
                raise Exception("Unable to reach %s" % url)
        return self.json[url]

    def cache(self, url, json):
        self.json[url] = json

    def __get__(self, instance, owner):
        url = self.urls[instance]
        json = self.get_url(url, headers=instance.get_headers())

        # allow the owner object to do operations on the JSON object
        try:
            instance.parse(json, self.cache)
            if type(json) == AsyncList:
                json._parser = instance.parse
        except AttributeError:
            pass

        self.cache(url, json)
        return json

    def __set__(self, instance, value):
        if value is None:
            self.urls[instance] = value
            return
        try:
            evaluated = type(instance).validate_url(value)
            if evaluated:
                self.urls[instance] = evaluated
            else:
                raise ValueError("URL %s does not comply to API for %s" % (value, str(type(instance))))
        except AttributeError:
            self.urls[instance] = value


class RemoteModel(object):

    data = AsyncRequest()

    def get_headers(self):
        return {}

    def __init__(self, url=None):
        self.data = url
        self._url = url

    def __geturl(self):
        return self._url

    def __seturl(self, value):
        self._url = value
        self.data = value

    url = property(__geturl, __seturl)

    def __dir__(self):
        directory = ["data"]
        if self.data:
            directory.extend(self.data.json().keys())

    def __getitem__(self, key):
        if self.data:
            return self.data[key]

    def __iter__(self):
        if self.data:
            return iter(self.data)
        else:
            return iter([])

    def __len__(self):
        if self.data:
            return len(self.data)
        return 0
