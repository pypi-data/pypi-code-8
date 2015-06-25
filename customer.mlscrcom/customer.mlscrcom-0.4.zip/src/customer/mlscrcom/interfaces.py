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
"""Interface definitions."""

# zope imports
from zope import schema
from zope.interface import Interface

# local imports
from customer.mlscrcom.i18n import _


class IMLSCRComSettings(Interface):
    """Registry settings for customer.mlscrcom.

    This describes records stored in the configuration registry and obtainable
    via plone.registry.
    """

    show_listing_search = schema.Bool(
        default=True,
        required=True,
        title=_(
            u"label_show_listing_search",
            default=u"Show listing search on Frontpage",
        ),
    )

    show_listing_quick_search = schema.Bool(
        default=True,
        required=True,
        title=_(
            u"label_show_listing_quick_search",
            default=u"Show listing quick search",
        ),
    )

    heading_agent_locator_en = schema.TextLine(
        default=u"Agent Locator",
        required=True,
        title=_(
            u"label_heading_agent_locator_en",
            default=u"Heading 'Agent Locator' (English)",
        ),
    )

    heading_agent_locator_es = schema.TextLine(
        default=u"Localizador de Agente",
        required=True,
        title=_(
            u"label_heading_agent_locator_es",
            default=u"Heading 'Agent Locator' (Spanish)",
        ),
    )

    heading_articles_en = schema.TextLine(
        default=u"Articles",
        required=True,
        title=_(
            u"label_heading_articles_en",
            default=u"Heading 'Articles' (English)"
        ),
    )

    heading_articles_es = schema.TextLine(
        default=u"Artículos",
        required=True,
        title=_(
            u"label_heading_articles_es",
            default=u"Heading 'Articles' (Spanish)"
        ),
    )

    heading_news_events_en = schema.TextLine(
        default=u"News & Events",
        required=True,
        title=_(
            u"label_heading_news_events_en",
            default=u"Heading 'News & Events' (English)",
        ),
    )

    heading_news_events_es = schema.TextLine(
        default=u"Noticias y Eventos",
        required=True,
        title=_(
            u"label_heading_news_events_es",
            default=u"Heading 'News & Events' (Spanish)",
        ),
    )

    heading_offering_seekings_en = schema.TextLine(
        default=u"Offering / Seeking Requests",
        required=True,
        title=_(
            u"label_heading_offering_seekings_en",
            default=u"Heading 'Offering / Seeking Requests' (English)",
        ),
    )

    heading_offering_seekings_es = schema.TextLine(
        default=u"Ofreciendo / Buscando",
        required=True,
        title=_(
            u"label_heading_offering_seekings_es",
            default=u"Heading 'Offering / Seeking Requests' (Spanish)",
        ),
    )

    heading_latest_listings_en = schema.TextLine(
        default=u"Latest Listings",
        required=True,
        title=_(
            u"label_heading_latest_listings_en",
            default=u"Heading 'Latest Listings' (English)",
        ),
    )

    heading_latest_listings_es = schema.TextLine(
        default=u"Ultimas Listados",
        required=True,
        title=_(
            u"label_heading_latest_listings_es",
            default=u"Heading 'Latest Listings' (Spanish)",
        ),
    )

    news_count = schema.Int(
        default=5,
        required=True,
        title=_(
            u"label_news_count",
            default=u"Number of News Items to display",
        ),
    )

    news_state = schema.Tuple(
        default=('published', ),
        required=True,
        title=_(
            u"label_news_state",
            default=u"News Items Workflow state",
        ),
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.WorkflowStates",
        ),
    )

    events_count = schema.Int(
        default=5,
        required=True,
        title=_(
            u"label_events_count",
            default=u"Number of Events to display",
        ),
    )

    events_state = schema.Tuple(
        default=('published', ),
        required=True,
        title=_(
            u"label_events_state",
            default=u"Events Workflow state",
        ),
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.WorkflowStates",
        ),
    )

    articles_count = schema.Int(
        default=5,
        required=True,
        title=_(
            u"label_articles_count",
            default=u"Number of Articles to display",
        ),
    )

    articles_url_en = schema.TextLine(
        required=False,
        title=_(
            u"label_articles_url_en",
            default=u"'Articles' URL (English)",
        ),
    )

    articles_url_es = schema.TextLine(
        required=False,
        title=_(
            u"label_articles_url_es",
            default=u"'Articles' URL (Spanish)",
        ),
    )

    recent_listings_count = schema.Int(
        default=5,
        required=True,
        title=_(
            u"label_recent_listings_count",
            default=u"Number of 'Latest Listings' to display",
        ),
    )

    recent_listings_url_en = schema.TextLine(
        required=False,
        title=_(
            u"label_recent_listings_url_en",
            default=u"'Recent Listings' URL (English)",
        ),
    )

    recent_listings_url_es = schema.TextLine(
        required=False,
        title=_(
            u"label_recent_listings_url_es",
            default=u"'Recent Listings' URL (Spanish)",
        ),
    )

    listing_search_url_en = schema.TextLine(
        required=True,
        title=_(
            u"label_listing_search_url_en",
            default=u"'Listing Search' URL (English)",
        ),
    )

    listing_search_url_es = schema.TextLine(
        required=True,
        title=_(
            u"label_listing_search_url_es",
            default=u"'Listing Search' URL (Spanish)",
        ),
    )
