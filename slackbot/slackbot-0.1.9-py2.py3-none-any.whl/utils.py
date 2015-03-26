# -*- coding: utf8 -*-

import os
import logging
import tempfile
import math
import thread
import Queue
import requests
from contextlib import contextmanager

logger = logging.getLogger(__name__)

def download_file(url, fpath):
    logger.debug('starting to fetch %s', url)
    r = requests.get(url, stream=True)
    with open(fpath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*64):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    logger.debug('fetch %s', fpath)
    return fpath


def to_utf8(s):
    """Convert a string to utf8. If the argument is an iterable
    (list/tuple/set), then each element of it would be converted instead.

    >>> to_utf8('a')
    'a'
    >>> to_utf8(u'a')
    'a'
    >>> to_utf8([u'a', u'b', u'\u4f60'])
    ['a', 'b', '\\xe4\\xbd\\xa0']
    """
    if isinstance(s, str):
        return s
    elif isinstance(s, unicode):
        return s.encode('utf-8')
    elif isinstance(s, (list, tuple, set)):
        return [to_utf8(v) for v in s]
    else:
        return s

def to_unicode(s):
    """Convert a string to unicode. If the argument is an iterable
    (list/tuple/set), then each element of it would be converted instead.

    >>> to_unicode('a')
    u'a'
    >>> to_unicode(u'a')
    u'a'
    >>> to_unicode(['a', 'b', '你'])
    [u'a', u'b', u'\u4f60']
    """
    if isinstance(s, str):
        return s.decode('utf-8')
    elif isinstance(s, unicode):
        return s
    elif isinstance(s, (list, tuple, set)):
        return [to_unicode(v) for v in s]
    else:
        return s

@contextmanager
def create_tmp_file(content=''):
    fd, name = tempfile.mkstemp()
    try:
        if content:
            os.write(fd, content)
        yield name
    finally:
        os.close(fd)
        os.remove(name)

def log2(x):
    return math.log(x, 2)

_suffixes = ['bytes', 'KB', 'MB', 'GB', 'TB', 'EB', 'ZB']
def readable_file_size(size):
    # determine binary order in steps of size 10
    # (coerce to int, // still returns a float)
    order = int(log2(size) / 10) if size else 0
    # format file size
    # (.4g results in rounded numbers for exact matches and max 3 decimals,
    # should never resort to exponent values)
    return '{:.4g} {}'.format(size / (1 << (order * 10)), _suffixes[order])

class WorkerPool(object):
    def __init__(self, func, nworker=10):
        self.nworker = nworker
        self.func = func
        self.queue = Queue.Queue()

    def start(self):
        for _ in xrange(self.nworker):
            thread.start_new_thread(self.do_work, tuple())

    def add_task(self, msg):
        self.queue.put(msg)

    def do_work(self):
        while True:
            msg = self.queue.get()
            self.func(msg)
