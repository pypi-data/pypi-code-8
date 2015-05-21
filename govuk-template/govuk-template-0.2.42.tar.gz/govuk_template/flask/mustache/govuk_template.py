from pystache.renderer import Renderer
from os import path


def thisDir():
    return path.dirname(path.abspath(__file__))


class GovukTemplate(object):

    def render(self, *context, **kwargs):
        renderer = Renderer(search_dirs=[thisDir()])
        template = renderer.load_template('govuk_template')
        return renderer.render(template, *context, **kwargs)
