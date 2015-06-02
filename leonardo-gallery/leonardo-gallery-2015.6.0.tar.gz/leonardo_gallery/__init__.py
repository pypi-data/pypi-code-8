
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


default_app_config = 'leonardo_gallery.Config'


class Default(object):

    apps = [
        'leonardo_gallery'
    ]

    js_files = [
        'js/photoswipe.min.js',
        'js/photoswipe-ui-default.min.js',
    ]

    css_files = [
        'css/photoswipe.css',
        'css/default-skin.css',
    ]

    """
        'js/angular/angular-touch.min.js',
        'js/angular/angular-carousel.min.js',

    angular_modules = [
        'angular-carousel',
    ]
    """


class Config(AppConfig, Default):
    name = 'leonardo_gallery'
    verbose_name = _("Gallery")

default = Default()
