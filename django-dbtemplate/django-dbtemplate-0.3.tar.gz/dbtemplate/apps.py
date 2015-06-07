from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DBTemplateConfig(AppConfig):
    name = 'dbtemplate'
    verbose_name = _(u'Templates')
