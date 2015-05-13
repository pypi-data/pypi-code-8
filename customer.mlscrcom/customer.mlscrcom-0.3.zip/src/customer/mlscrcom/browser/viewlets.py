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
"""Custom viewlets for customer.mlscrcom."""

# zope imports
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets.common import ViewletBase
from plone.directives import form
from plone.registry.interfaces import IRegistry
from plone.z3cform import z2
from z3c.form import button, field
from z3c.form.browser import checkbox
from z3c.form.interfaces import IFormLayer
from zope import schema
from zope.component import getMultiAdapter, queryUtility
from zope.interface import Interface, alsoProvides

# starting from 0.6.0 version plone.z3cform has IWrappedForm interface
try:
    from plone.z3cform.interfaces import IWrappedForm
    HAS_WRAPPED_FORM = True
except ImportError:
    HAS_WRAPPED_FORM = False

# local imports
from customer.mlscrcom.browser.interfaces import IFrontPage
from customer.mlscrcom.i18n import _
from customer.mlscrcom.interfaces import IMLSCRComSettings


class IListingSearchForm(Interface):
    """Listing search form schema definition."""

    location_state = schema.Choice(
        required=False,
        title=_(
            u'label_listing_search_location',
            default=u'Location',
        ),
        source='plone.mls.listing.LocationStates'
    )

    listing_type = schema.Tuple(
        default=('rs', 'rl', 'cs', 'cl', 'll', ),
        required=False,
        title=_(
            u"label_listing_search_listing_type",
            default=u"Listing Type",
        ),
        value_type=schema.Choice(
            source='plone.mls.listing.ListingTypes'
        ),
    )

    price_min = schema.Int(
        required=False,
        title=_(
            u'label_listing_search_price_min',
            default=u'Price',
        ),
    )

    price_max = schema.Int(
        required=False,
        title=u'-',
    )


class ListingSearchForm(form.Form):
    """Listing Search Form."""
    fields = field.Fields(IListingSearchForm)
    fields['listing_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    ignoreContext = True
    method = 'get'

    @property
    def action(self):
        """See interfaces.IInputForm"""
        p_state = self.context.unrestrictedTraverse("@@plone_portal_state")
        navigation_root_url = p_state.navigation_root_url()
        static_search_url_en = 'search-properties'
        static_search_url_es = 'busqueda-de-propiedad'

        lang = p_state.language()
        if lang == 'es':
            return navigation_root_url + '/' + static_search_url_es

        return navigation_root_url + '/' + static_search_url_en
        # return static_search_url_en + '/@@view' +url

    @button.buttonAndHandler(_(u"Search"), name='search')
    def handle_search(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return


class ListingSearchViewlet(ViewletBase):
    """Listing Search Viewlet."""
    index = ViewPageTemplateFile('templates/listing-search-viewlet.pt')
    link_stepone = {'en': 'search-properties', 'es': 'busqueda-de-propiedad'}
    link_steptwo = {'en': '', 'es': ''}
    link_stepthree = {'en': '', 'es': ''}
    link_stepfour = {'en': '', 'es': ''}

    @property
    def available(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IMLSCRComSettings, check=False)
        if not getattr(settings, 'show_listing_search', True):
            return False

        view = getMultiAdapter((self.context, self.request),
                               name=self.context_state.view_template_id())
        return IFrontPage.providedBy(view)

    def update(self):
        super(ListingSearchViewlet, self).update()
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.lang = self.portal_state.language()

        if INavigationRoot.providedBy(self.context_state.canonical_object()):
            z2.switch_on(self, request_layer=IFormLayer)
            self.form = ListingSearchForm(aq_inner(self.context), self.request)
            if HAS_WRAPPED_FORM:
                alsoProvides(self.form, IWrappedForm)
            self.form.update()

    @property
    def stepone(self):
        return self.portal_state.navigation_root_url() + '/' + \
            self.link_stepone[self.lang]

    @property
    def steptwo(self):
        return self.portal_state.navigation_root_url() + '/' + \
            self.link_steptwo[self.lang]

    @property
    def stepthree(self):
        return self.portal_state.navigation_root_url() + '/' + \
            self.link_stepthree[self.lang]

    @property
    def stepfour(self):
        return self.portal_state.navigation_root_url() + '/' + \
            self.link_stepfour[self.lang]


class ListingQuickSearchViewlet(ViewletBase):
    """Listing Quick Search Viewlet."""
    index = ViewPageTemplateFile('templates/listing-quick-search-viewlet.pt')

    @property
    def available(self):
        # Currently not available
        return False

        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IMLSCRComSettings, check=False)
        if not getattr(settings, 'show_listing_quick_search', True):
            return False
