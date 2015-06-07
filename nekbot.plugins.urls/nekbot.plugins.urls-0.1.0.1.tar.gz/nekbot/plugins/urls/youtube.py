__author__ = 'nekmo'

import pafy

class YoutubeMetadata(object):
    source_url = 'youtube.com'

    def __init__(self, url):
        self.data = pafy.new(url)

    @property
    def title(self):
        return self.data.title

    @property
    def authors(self):
        return [self.data.author]

    @property
    def extra(self):
        return '[%s]' % self.data.duration

def youtube(url):
    return YoutubeMetadata(url)