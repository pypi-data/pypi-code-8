import pkg_resources
import os
from nagare import wsgi

from .namespaces import xhtml5


def get_file_from_package(package, path):
    """
    Return the path of a static content, located into a setuptools package

    In:
      - ``package`` -- the setuptools package of a registered application
      - ``path`` -- the url path of the wanted static content

    Return:
      - the path of the static content
    """
    path = os.path.join('static', path[1:])

    if not pkg_resources.resource_exists(package, path) or pkg_resources.resource_isdir(package, path):
        return None

    return pkg_resources.resource_filename(package, path)


class WSGIApp(wsgi.WSGIApp):

    renderer_factory = xhtml5.Renderer

    def set_publisher(self, publisher):
        publisher.register_static(
            'jquery-nagare', lambda path, r=pkg_resources.Requirement.parse('jquery_nagare'): get_file_from_package(r, path))
        super(WSGIApp, self).set_publisher(publisher)
