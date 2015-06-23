# -*- coding: utf-8 -*-
from collective.navigationtitle import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.directives import order_after
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class INavigationTitle(model.Schema):
    """Adds a field for navigation title after the original title.
    """

    order_after(short_title='IBasic.title')
    order_after(short_title='IDublinCore.title')

    short_title = schema.TextLine(
        title=_(u"Navigation Title"),
        description=_(u"Short title that will be used in navigation."),
        required=False,
    )


@implementer(INavigationTitle)
class NavigationTitle(object):
    """
    """

    def __init__(self, context):
        self.context = context

    @property
    def short_title(self):
        return getattr(self.context, '_short_title', None)

    @short_title.setter
    def short_title(self, value):
        self.context._short_title = value
