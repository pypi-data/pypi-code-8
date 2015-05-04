
from ..cachetree import install
from django.core.exceptions import MiddlewareNotUsed

class InstallCachetree(object):
    """
    Installs cachetree after Django has loaded, using the approach described here:
    
    http://stackoverflow.com/questions/5439650/how-to-run-arbitrary-code-after-django-is-fully-loaded
    """
    
    def __init__(self):
        install()
        raise MiddlewareNotUsed