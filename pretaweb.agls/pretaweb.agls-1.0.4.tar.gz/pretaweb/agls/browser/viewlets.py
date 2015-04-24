# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import DublinCoreViewlet
from pretaweb.agls.config import AGLS_SCHEME


class AGLSViewlet(DublinCoreViewlet):
    index = ViewPageTemplateFile('templates/agls.pt')

    def update(self):
        super(AGLSViewlet, self).update()

        # DC tags are switched off in Plone control panel
        if not self.metatags:
            return

        # map dublin core meta tags
        dc = {}
        for tag in self.metatags:
            dc[tag[0]] = tag[1]

        context = aq_inner(self.context)
        agls_tags = []

        agls = context.unrestrictedTraverse('@@agls')

        # AGLS Title (mandatory)
        value = agls.Title() or dc.get('DC.Title', '') or context.Title()
        agls_tags.append({
            'name': u'DCTERMS.title',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.title']
        })

        # AGLS Description (mandatory)
        value = agls.Description() or \
            dc.get('DC.description', '') or \
            context.Description()
        agls_tags.append({
            'name': u'DCTERMS.description',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.description']
        })
        agls_tags.append({
            'name': u'description',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['description']
        })

        # AGLS Date (mandatory)
        agls_tags.append({
            'name': u'DCTERMS.created',
            'content': agls.Created(),
            'scheme': AGLS_SCHEME['DCTERMS.created']
        })

        # AGLS Creator (mandatory)
        agls_tags.append({
            'name': u'DCTERMS.creator',
            'content': safe_unicode(
                agls.Creator() or
                dc.get('DC.creator', '')),
            'scheme': AGLS_SCHEME['DCTERMS.creator']
        })

        # AGLS Subject
        value = agls.Subject() or \
            '; '.join(dc.get('DC.subject', '').split(', '))
        agls_tags.append({
            'name': u'DCTERMS.subject',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.subject']
        })

        # AGLS Type (mandatory)
        default_type = ''
        type_method = getattr(context.aq_explicit, 'Type', None)
        if callable(type_method):
            # Catch AttributeErrors raised by some AT applications
            try:
                default_type = type_method()
            except AttributeError:
                pass

        agls_tags.append({
            'name': u'DCTERMS.type',
            'content': safe_unicode(agls.Type() or default_type),
            'scheme': AGLS_SCHEME['DCTERMS.type']
        })

        # AGLS Identifier (mandatory)
        agls_tags.append({
            'name': u'DCTERMS.identifier',
            'content': agls.Identifier(),
            'scheme': AGLS_SCHEME['DCTERMS.identifier']
        })

        # copy over keywords tag
        if 'keywords' in dc:
            agls_tags.append({
                'name': u'keywords',
                'content': safe_unicode(dc['keywords']),
                'scheme': None
            })

        # AGLS Publisher
        agls_tags.append({
            'name': u'DCTERMS.publisher',
            'content': safe_unicode(
                agls.Publisher() or
                dc.get('DC.creator', '')),
            'scheme': AGLS_SCHEME['DCTERMS.publisher']
        })

        # AGLS Format
        default_format = ''
        format_method = getattr(context.aq_explicit, 'Format', None)
        if callable(format_method):
            # Catch AttributeErrors raised by some AT applications
            try:
                default_format = format_method()
            except AttributeError:
                pass

        agls_tags.append({
            'name': u'DCTERMS.format',
            'content': safe_unicode(
                agls.Format() or
                dc.get('DC.format', '') or default_format),
            'scheme': AGLS_SCHEME['DCTERMS.format']
        })

        self.metatags = tuple(agls_tags)
