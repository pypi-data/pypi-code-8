import re
import os.path
from six.moves.urllib.parse import (
    ParseResult, urlunparse, urldefrag,
    urlparse, parse_qsl, urlencode,
    quote, unquote
)

# https://developers.google.com/safe-browsing/developers_guide_v2#Canonicalization

def canonicalize(url):
    scheme, netloc, path, params, query, fragment = urlparse(url.strip())
    netloc = canonicalize_host(netloc)
    path = canonicalize_path(path)

    fragment = ''
    return urlunparse((scheme, netloc, path, params, query, fragment))


def canonicalize_path(path):
    if path == '':
        return '/'
    prev_path = path
    while True:
        path = unquote(path)
        if path == prev_path:
            break
        prev_path = path
    path = os.path.normpath(path)
    path = re.sub('/+', '/', path)
    path = quote(path)
    return path

def canonicalize_host(host):
    host = host.strip('.')
    return host.lower()