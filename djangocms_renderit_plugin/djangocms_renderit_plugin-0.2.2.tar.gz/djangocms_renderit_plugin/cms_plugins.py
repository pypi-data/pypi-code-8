from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import RenderitCMSPlugin


class RenderItPlugin(CMSPluginBase):
    model = RenderitCMSPlugin
    cache = False
    allow_children = True
    render_template = 'djangocms_renderit_plugin/renderit.html'


plugin_pool.register_plugin(RenderItPlugin)
