
from django.apps import AppConfig

default_app_config = 'leonardo_module_analytics.AnalyticsConfig'


class Default(object):

    apps = [
        'analytical',
        'leonardo_module_analytics',
    ]


class AnalyticsConfig(AppConfig, Default):
    name = 'leonardo_module_analytics'
    verbose_name = ("Leonardo Analytics")

default = Default()
