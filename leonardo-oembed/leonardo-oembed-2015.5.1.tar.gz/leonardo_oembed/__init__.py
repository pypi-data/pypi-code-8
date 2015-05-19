
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .widget import *


default_app_config = 'leonardo_oembed.Config'


class Default(object):

    optgroup = 'Oembed'

    apps = [
        'feincms_oembed',
        'leonardo_oembed',
    ]

    widgets = [
        OembedWidget,
        FeedWidget
    ]

    config = {
        'Web': {
            'EMBEDLY_KEY': ('62809705-1', _('Embedly API key')),
        }
    }


class Config(AppConfig, Default):
    name = 'leonardo_oembed'
    verbose_name = ("Leonardo OEmbed")

default = Default()
