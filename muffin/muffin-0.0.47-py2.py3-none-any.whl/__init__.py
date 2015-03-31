"""
    muffin description.

"""

# Package information
# ===================

__version__ = "0.0.47"
__project__ = "muffin"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"

from asyncio import *           # noqa
from aiohttp.web import *       # noqa

CONFIGURATION_ENVIRON_VARIABLE = 'MUFFIN_CONFIG'

from .app import Application    # noqa
from .handler import Handler    # noqa
from .utils import to_coroutine # noqa
