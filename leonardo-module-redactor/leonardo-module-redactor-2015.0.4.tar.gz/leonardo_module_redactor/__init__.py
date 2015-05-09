
from django.apps import AppConfig

default_app_config = 'leonardo_module_redactor.RedactorConfig'


class Default(object):

    apps = [
        'redactor',
        'leonardo_module_redactor',
    ]

    js_files = [
        'redactor/redactor.js',
        'redactor/plugins/table.js',
        'redactor/plugins/video.js',
        'redactor/plugins/fullscreen.js',
        'redactor/plugins/filemanager.js',
        'redactor/plugins/textdirection.js',
        'redactor/plugins/fontcolor.js'
    ]

    css_files = [
        'redactor/css/redactor.css'
    ]


class RedactorConfig(AppConfig, Default):
    name = 'leonardo_module_redactor'
    verbose_name = ("Leonardo Redactor")

default = Default()
