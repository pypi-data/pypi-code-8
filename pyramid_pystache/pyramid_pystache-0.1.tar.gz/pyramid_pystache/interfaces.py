from zope.interface import (
    Attribute,
    Interface,
    )
from pyramid.interfaces import IRenderer

class IMustacheLookup(Interface):
    def __call__(self, info):
        """ Return an ITemplateRenderer based on IRendererInfo ``info`` """

class ITemplateRenderer(IRenderer):
    def implementation():
        """ Return the object that the underlying templating system
        uses to render the template; it is typically a callable that
        accepts arbitrary keyword arguments and returns a string or
        unicode object """
