import re
from nekbot.plugins.urls.generic import generic
from nekbot.plugins.urls.meneame import meneame
from nekbot.plugins.urls.youtube import youtube

__author__ = 'nekmo'


PARSERS = [
    {'function': meneame, 'match': '^https?://www\.meneame\.net/story/(.+)'},
    {'function': youtube, 'match': '^https?://(?:www\.|)(?:youtube\.com|youtu\.be)/.+'},
    {'function': generic, 'match': '.+'},
]

def get_parser(url):
    for parser in PARSERS:
        if not re.match(parser['match'], url, re.IGNORECASE): continue
        return parser['function']


def urlinfo(url):
    parser = get_parser(url)
    parser.extra = ''
    return parser(url)