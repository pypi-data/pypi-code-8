
from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig

default_app_config = 'leonardo_module_redactor.RedactorConfig'


class Default(object):

    urls_conf = 'redactor.urls'

    apps = [
        'redactor',
        'leonardo_module_redactor',
    ]

    js_files = [
        'redactor/redactor.init.js',
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

    config = {
        'REDACTOR_UPLOAD': ('uploads/', _('Redactor upload directory')),
    }


class RedactorConfig(AppConfig, Default):
    name = 'leonardo_module_redactor'
    verbose_name = _("Leonardo Redactor")

    def ready(self):

        # path forms
        from leonardo.module.web.widgets import forms as widget_forms
        from redactor.widgets import RedactorEditor
        widget_forms.WIDGETS['text'] = RedactorEditor()

default = Default()
