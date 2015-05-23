import os
from zope.interface import implementer

from pyramid.decorator import reify
from pyramid_pystache import renderer
from pyramid_pystache.interfaces import ITemplateRenderer

import pystache

def renderer_factory(info):
    return renderer.template_renderer_factory(info, MustacheTemplateRenderer)

class MustacheTemplateFile(object):
    def __init__(self, path):
        self.path = path
        self.renderer = pystache.Renderer(
            search_dirs=os.path.dirname(path)
        )

    def __call__(self, **kwargs):
        return self.renderer.render_path(self.path, **kwargs)

@implementer(ITemplateRenderer)
class MustacheTemplateRenderer(object):
    def __init__(self, path, lookup):
        self.path = path
        self.lookup = lookup

    @reify # avoid looking up reload_templates before manager pushed
    def template(self):
        return MustacheTemplateFile(path=self.path)

    def implementation(self):
        return self.template

    def __call__(self, value, system):
        try:
            system.update(value)
        except (TypeError, ValueError):
            raise ValueError('renderer was passed non-dictionary as value')
        result = self.template(**system)
        return result

