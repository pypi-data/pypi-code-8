import requests, vlermv

DIR = '~/.spaceapi'

class int_transformer:
    def to_path(timestamp):
        return ('%d' % timestamp,)
    def from_path(path):
        assert len(path) == 1, path
        return int(path[0])

@vlermv.cache(DIR, 'directory', key_transformer = int_transformer)
def directory(timestamp):
    url = 'http://spaceapi.net/directory.json'
    return requests.get(url)

@vlermv.cache(DIR, 'space')
def space(datetime, url):
    return requests.get(url, verify = False)
