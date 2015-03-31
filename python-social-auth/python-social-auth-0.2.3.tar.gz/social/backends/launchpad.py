"""
Launchpad OpenId backend
"""

from social.backends.open_id import OpenIdAuth


class LaunchpadOpenId(OpenIdAuth):
    name = 'launchpad'
    URL = 'https://login.launchpad.net'
    USERNAME_KEY = 'nickname'
