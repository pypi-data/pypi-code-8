from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import *

from django.db.transaction import TransactionManagementError

import logging, pprint
logger = logging.getLogger('cmsplugin_latest')

def _debug_chomp(s, sz):
    return "%s...%s"%(s[:sz], s[-sz:])

class LatestPlugin(CMSPluginBase):
    model = Latest
    name = _("Latest Items From Selected Models")
    render_template = "cmsplugin_latest/latest_plugin.html"
    render_plugin=True
    change_form_template = "cmsplugin_latest/index.html"
    inlines = (LatestInline,)

    def save_model(self, request, obj, form, change):
        logger.debug("LatestPlugin.save_model()...")
        logger.debug("Request: %s"%request)
        logger.debug("Object: %s"%obj)
        logger.debug("Form: %s"%form.as_p())
        logger.debug("Change: %s"%change)
        return super(LatestPlugin, self).save_model(request, obj, form, change)

    def render(self, context, instance, placeholder):
        latest = list(instance.get_latest())
        context['latest'] = latest
        cs = pprint.pformat(context)
        logger.debug("Latest: ")
        for l in latest:
            logger.debug("\t-%s"%l)
        return context

plugin_pool.register_plugin(LatestPlugin)
