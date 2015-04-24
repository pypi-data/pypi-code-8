from cStringIO import StringIO
import tarfile
import urlparse
import posixpath

import logging

root_logger = logging.getLogger()

def make_archive(path, logger=root_logger):
    stream = StringIO()
    try:
        tar = tarfile.open(mode='w', fileobj=stream)
        tar.add(path, arcname='.')
        logger.info(tar.getnames())
        return stream.getvalue()
    finally:
        stream.close()

def normalize_url(url):
    u1 = urlparse.urlparse(url)
    u2 = [c for c in u1]
    u2[2] = posixpath.normpath(u1.path)
    if u1.path and u1.path[-1] == "/":
        u2[2] += "/"
    u3 = urlparse.urlunparse(u2)
    return u3
    
    
    
