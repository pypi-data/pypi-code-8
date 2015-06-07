# coding=utf-8
import re
import requests

__author__ = 'nekmo'

class MeneameMetadata(object):
    source_url = 'meneame.net'


    def __init__(self, url):
        r = requests.get(url, stream=True)
        data = r.raw.read(1024 * 14, decode_content=True)
        self.title = re.findall('<title>([^<]+)</title>', data)
        with open('/tmp/debug', 'wb') as f:
            f.write(data)
        if self.title:
            self.title = self.title[0].decode('utf-8')
        else:
            self.title = None
        self.authors = re.findall('<a href="/user/[^/]+/history">([^<]+)</a>', data,
                                  re.MULTILINE)
        self.authors = self.authors if self.authors else None
        self.meneos = re.findall('<a id="a-votes-\d+" (?:[^>]+)>(\d+)</a>', data,
                            re.MULTILINE)
        self.meneos = self.meneos[0] if self.meneos else None
        self.negatives = re.findall('<span id="a-neg-\d+">(\d+)</span>', data)
        self.negatives = self.negatives[0] if self.negatives else None

    @property
    def extra(self):
        if not self.meneos or not self.negatives:
            return ''
        return u'(↑%s ↓%s)' % (self.meneos, self.negatives)

def meneame(url):
    return MeneameMetadata(url)