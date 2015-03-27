from django.views.generic import View

from oauthlib.oauth2 import Server

from ..settings import oauth2_settings
from .mixins import ProtectedResourceMixin, ScopedResourceMixin, ReadWriteScopedResourceMixin


class ProtectedResourceView(ProtectedResourceMixin, View):
    """
    Generic view protecting resources by providing OAuth2 authentication out of the box
    """
    server_class = Server
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS


class ScopedProtectedResourceView(ScopedResourceMixin, ProtectedResourceView):
    """
    Generic view protecting resources by providing OAuth2 authentication and Scopes handling out of the box
    """
    pass


class ReadWriteScopedResourceView(ReadWriteScopedResourceMixin, ProtectedResourceView):
    """
    Generic view protecting resources with OAuth2 authentication and read/write scopes.
    GET, HEAD, OPTIONS http methods require "read" scope. Otherwise "write" scope is required.
    """
    pass
