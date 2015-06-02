from views import ShoppingListViewSet
from lisa_api.lisa.routers import DynamicRouter


class ShoppingPlugin():
    def __init__(self):
        DynamicRouter().register_endpoint(r'shopping', ShoppingListViewSet)


__title__ = 'Lisa Plugins Shopping'
__version__ = '0.1.7.5'
__author__ = 'Julien Syx'
__license__ = 'Apache'
__copyright__ = 'Copyright 2015 Julien Syx'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'

