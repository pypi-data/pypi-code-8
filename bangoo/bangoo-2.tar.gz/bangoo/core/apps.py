from django.apps import AppConfig


class BangooCoreConfig(AppConfig):
    name = 'bangoo.core'
    verbose_name = "Bangoo core app"

    def ready(self):
        from bangoo.core import bangoo_plugins
        bangoo_plugins.load()
