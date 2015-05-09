
from django.apps import AppConfig

default_app_config = 'leonardo_module_redcator.RedactorConfig'


class Default(object):

    apps = [
        'redactor',
        'leonardo_module_redcator',
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


class RedactorConfig(AppConfig, Default):
    name = 'leonardo_module_redcator'
    verbose_name = ("Leonardo Redactor")

default = Default()
