# -*- coding: utf-8 -*-
from Acquisition import aq_inner
# The interface used should be the same as in ../content/agls
from Products.Archetypes.interfaces import IBaseContent
from Products.Archetypes.utils import shasattr
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from plone.indexer import indexer
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class AGLSView(BrowserView):

    def Title(self):
        """@return agls override of Title or None"""
        context = aq_inner(self.context)

        # AGLS Title
        if shasattr(context, 'agls_title_override') and \
           context.agls_title_override:
            return context.agls_title
        else:
            return None

    def Description(self):
        """@return agls override of Description or None"""
        context = aq_inner(self.context)

        # AGLS Description
        if shasattr(context, 'agls_desc_override') and \
           context.agls_desc_override:
            return context.agls_desc
        else:
            return None

    def Created(self):
        """@return ISO8601 of creation_date"""
        context = aq_inner(self.context)

        # AGLS Date
        value = ''
        if shasattr(context, 'creation_date'):
            value = context.creation_date
            # try to convert value to ISO8601 format w/o time component
            if hasattr(value, 'strftime'):
                value = value.strftime('%Y-%m-%d')
            else:
                value = ''
        return value

    def Creator(self):
        """@return agls override of author or None"""
        context = aq_inner(self.context)

        # get global AGLS settings
        registry = getUtility(IRegistry)

        # AGLS Author
        default_author = registry[
            'pretaweb.agls.browser.controlpanel.IAGLSSchema.default_author']
        if shasattr(context, 'agls_author_override') and \
           context.agls_author_override:
            value = context.agls_author
        elif default_author:
            value = default_author
        else:
            value = None
        return value

    def Subject(self):
        """@return agls override of Subject or None"""
        context = aq_inner(self.context)

        # AGLS Subject
        if shasattr(context, 'agls_subject_override') and \
           context.agls_subject_override:
            value = '; '.join(context.agls_subject)
        else:
            value = ''
        return value

    def Type(self):
        """@return agls tyoe"""
        context = aq_inner(self.context)

        # AGLS Type
        value = ''
        if shasattr(context, 'AGLSType'):
            value = context.AGLSType
        return safe_unicode(value)

    def Identifier(self):
        """@return agls identifier or UUID"""
        context = aq_inner(self.context)

        # AGLS Identifier
        if shasattr(context, 'agls_id_override') and \
           context.agls_id_override:
            value = u'urn:uuid:' + safe_unicode(context.agls_id)
        elif shasattr(context, 'UID'):
            value = u'urn:uuid:' + safe_unicode(context.UID())
        else:
            value = safe_unicode(context.absolute_url())
        return value

    def Publisher(self):
        """@return agls publisher or None"""
        context = aq_inner(self.context)
        # get global AGLS settings
        registry = getUtility(IRegistry)

        # AGLS Publisher
        default_publisher = registry[
            'pretaweb.agls.browser.controlpanel.IAGLSSchema.default_publisher']
        if shasattr(context, 'agls_publisher_override') and \
           context.agls_publisher_override:
            value = context.agls_publisher
        elif default_publisher:
            value = default_publisher
        else:
            value = None
        return safe_unicode(value)

    def Format(self):
        """@return agls format override"""
        context = aq_inner(self.context)

        # AGLS Format
        if shasattr(context, 'agls_format_override') and \
           context.agls_format_override:
            value = context.agls_format
        else:
            value = None
        return safe_unicode(value)


@indexer(IBaseContent)
def agls_subject(object, **kw):
    return object.unrestrictedTraverse('agls').Subject()


@indexer(IBaseContent)
def agls_type(context, **kw):
    schema = context.Schema()
    atype = schema.get('AGLSType', None)
    if atype is not None:
        return atype.get(context)
    else:
        return None
