"""AppConfig for relaydomains."""

from django.apps import AppConfig


class AdminRelayDomainsConfig(AppConfig):

    """App configuration."""

    name = "modoboa_admin_relaydomains"
    verbose_name = "Modoboa relay domains"

    def ready(self):
        from . import handlers
