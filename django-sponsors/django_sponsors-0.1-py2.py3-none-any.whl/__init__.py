#Ok, this is really weird but, in python3.2 we must import app_settings before
# django imports apps; otherwise the module-class hack doesn't work as expected
from . import app_settings
from django.utils.version import get_version

VERSION = (0, 1, 0, 'alpha', 0)

__version__ = get_version(VERSION)

default_app_config = 'sponsors.apps.SponsorsConfig'
