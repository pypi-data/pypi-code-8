from django.apps import AppConfig
from bangoo.navigation.signals import menu_created
from bangoo.content.receivers import menu_created_callback


class ContentConfig(AppConfig):
    name = 'bangoo.content'
    verbose_name = 'Bangoo flatpage app'

    def ready(self):
        menu_created.connect(menu_created_callback)
