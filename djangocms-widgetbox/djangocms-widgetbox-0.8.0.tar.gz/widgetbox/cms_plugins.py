from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import ButtonPlugin, QuotePlugin, GalleryPlugin, GalleryImagePlugin


class CMSButtonPlugin(CMSPluginBase):
    model = ButtonPlugin
    module = "Widget Box"
    name = "Button"
    render_template = "widgetbox/button.html"


class CMSQuotePlugin(CMSPluginBase):
    model = QuotePlugin
    module = "Widget Box"
    name = "Quote"
    render_template = "widgetbox/quote.html"


class CMSGalleryPlugin(CMSPluginBase):
    model = GalleryPlugin
    module = "Widget Box"
    name = "Gallery"
    allow_children = True
    child_classes = ["CMSGalleryImagePlugin"]
    render_template = "widgetbox/gallery.html"


class CMSGalleryImagePlugin(CMSPluginBase):
    model = GalleryImagePlugin
    module = "Widget Box"
    name = "Gallery Image"
    parent_classes = ["CMSGalleryPlugin"]
    render_template = "widgetbox/gallery-image.html"


plugin_pool.register_plugin(CMSButtonPlugin)
plugin_pool.register_plugin(CMSQuotePlugin)
plugin_pool.register_plugin(CMSGalleryPlugin)
plugin_pool.register_plugin(CMSGalleryImagePlugin)
