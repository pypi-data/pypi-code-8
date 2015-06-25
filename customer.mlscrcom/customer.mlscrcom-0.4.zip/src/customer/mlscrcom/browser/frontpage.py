# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2011 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
###############################################################################
"""Custom front page view for customer.mlscrcom."""

# python imports
from DateTime.DateTime import DateTime

# zope imports
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.interface import implements
from zope.publisher.browser import BrowserView

# local imports
from customer.mlscrcom.interfaces import IMLSCRComSettings
from customer.mlscrcom.browser.interfaces import IFrontPage
from plone.mls.listing.api import recent_listings


HEADINGS = ['heading_agent_locator', 'heading_articles', 'heading_news_events',
            'heading_offering_seekings', 'heading_latest_listings', ]


class FrontPageView(BrowserView):
    """Custom front page view."""
    implements(IFrontPage)

    def __call__(self):
        """Update the view and return the template."""
        self.update()
        return self.index()

    def _get_headings(self, lang='en'):
        """Get the section headings dependend on the language."""
        headings = {}
        settings = self.registry_settings
        for heading in HEADINGS:
            try:
                label = getattr(settings, heading + '_' + lang)
            except AttributeError:
                label = u''
            headings.update({
                heading: label,
            })
        return headings

    @memoize
    def _news_data(self):
        """Get the news items."""
        settings = self.registry_settings
        limit = getattr(settings, 'news_count', 5)
        state = getattr(settings, 'news_state', ('published', ))
        path = self.navigation_root_path
        return self.catalog(portal_type='News Item',
                            review_state=state,
                            path=path,
                            sort_on='Date',
                            sort_order='reverse',
                            sort_limit=limit)[:limit]

    @memoize
    def _events_data(self):
        """Get the event entries."""
        settings = self.registry_settings
        limit = getattr(settings, 'events_count', 5)
        state = getattr(settings, 'events_state', ('published', ))
        path = self.navigation_root_path
        return self.catalog(portal_type='Event',
                            review_state=state,
                            end={'query': DateTime(),
                                 'range': 'min'},
                            path=path,
                            sort_on='start',
                            sort_limit=limit)[:limit]

    @property
    def catalog(self):
        context = aq_inner(self.context)
        return getToolByName(context, 'portal_catalog')

    def update(self):
        """Update the view and collect the data."""
        registry = queryUtility(IRegistry)
        self.portal_state = self.context.unrestrictedTraverse(
            "@@plone_portal_state")
        self.navigation_root_path = self.portal_state.navigation_root_path()
        self.navigation_root_url = self.portal_state.navigation_root_url()
        self.registry_settings = registry.forInterface(IMLSCRComSettings,
                                                       check=False)
        lang = self.portal_state.language()
        self.headings = self._get_headings(lang)

    @property
    def news_items(self):
        """Return the news items."""
        return self._news_data()

    @property
    def news_available(self):
        """Check if news items are available."""
        return len(self.news_items) > 0

    @property
    def events_items(self):
        """Return the event entries."""
        return self._events_data()

    @property
    def events_available(self):
        """Check if event entries are available."""
        return len(self.events_items) > 0

    @property
    def articles(self):
        """Return the article items."""
        settings = self.registry_settings
        limit = getattr(settings, 'articles_count', 5)
        lang = self.portal_state.language()
        articles_url = getattr(settings, 'articles_url_' + lang)
        if articles_url is None:
            return
        path = '/'.join([self.navigation_root_path, articles_url])
        return self.catalog(path={'query': path, 'depth': 1},
                            sort_on='Date',
                            portal_type=['Document', 'Article', ],
                            sort_limit=limit)[:limit]

    @property
    def articles_available(self):
        """Check if articles are available."""
        return len(self.articles) > 0

    @property
    def news_section_available(self):
        return self.news_available or self.events_available or \
            self.articles_available

    @property
    def recent_listings(self):
        settings = self.registry_settings
        limit = getattr(settings, 'recent_listings_count', 5)
        # TODO: Get recent listings config from references content element
        # config = ...
        params = {
            'limit': limit,
            'offset': 0,
            'lang': self.portal_state.language(),
        }
        return recent_listings(params, batching=False)

    @property
    def recent_listings_available(self):
        return len(self.recent_listings) > 0

    @property
    def recent_listings_url(self):
        settings = self.registry_settings
        lang = self.portal_state.language()
        url = getattr(settings, 'recent_listings_url_' + lang, None)
        if url is None:
            url = ''
        return self.navigation_root_url + '/' + url
