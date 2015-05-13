# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2012 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AS IS AND ANY EXPRESSED OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
###############################################################################
"""Test Registry for customer.mlscrcom."""

# python imports
import unittest2 as unittest

# zope imports
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

# local imports
from customer.mlscrcom.interfaces import IMLSCRComSettings
from customer.mlscrcom.testing import CUSTOMER_MLSCRCOM_INTEGRATION_TESTING


class TestMLSCRComRegistry(unittest.TestCase):
    """Registry Test Case for customer.mlscrcom."""
    layer = CUSTOMER_MLSCRCOM_INTEGRATION_TESTING

    def test_registry_registered(self):
        """Test that the settings are registered correctly."""
        registry = getUtility(IRegistry)
        self.assertTrue(registry.forInterface(IMLSCRComSettings))

    def test_registry_show_listing_search(self):
        """Test for the 'show_listing_search' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'show_listing_search'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, True)

    def test_registry_show_listing_quick_search(self):
        """Test for the 'show_listing_quick_search' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'show_listing_quick_search'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, False)

    def test_registry_heading_agent_locator_en(self):
        """Test for the 'heading_agent_locator_en' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'heading_agent_locator_en'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, u'Agent Locator')

    def test_registry_heading_agent_locator_es(self):
        """Test for the 'heading_agent_locator_es' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'heading_agent_locator_es'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value,
                          u'Localizador de Agente')

    def test_registry_heading_articles_en(self):
        """Test for the 'heading_articles_en' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'heading_articles_en'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, u'Articles')

    def test_registry_heading_articles_es(self):
        """Test for the 'heading_articles_es' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'heading_articles_es'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, u'Artículos')

    def test_registry_heading_news_events_en(self):
        """Test for the 'heading_news_events_en' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'heading_news_events_en'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, u'News & Events')

    def test_registry_heading_news_events_es(self):
        """Test for the 'heading_news_events_es' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'heading_news_events_es'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value,
                          u'Noticias y Eventos')

    def test_registry_heading_offering_seekings_en(self):
        """Test for the 'heading_offering_seekings_en' key and default value"""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'heading_offering_seekings_en'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value,
                          u'Offering / Seeking Requests')

    def test_registry_heading_offering_seekings_es(self):
        """Test for the 'heading_offering_seekings_es' key and default value"""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'heading_offering_seekings_es'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value,
                          u'Ofreciendo / Buscando')

    def test_registry_heading_latest_listings_en(self):
        """Test for the 'heading_latest_listings_en' key and default value"""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'heading_latest_listings_en'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, u'Latest Listings')

    def test_registry_heading_latest_listings_es(self):
        """Test for the 'heading_latest_listings_es' key and default value"""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'heading_latest_listings_es'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, u'Ultimos Listados')

    def test_registry_news_count(self):
        """Test for the 'news_count' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.news_count'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, 3)

    def test_registry_news_state(self):
        """Test for the 'news_state' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.news_state'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, ('published', ))

    def test_registry_events_count(self):
        """Test for the 'events_count' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.events_count'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, 3)

    def test_registry_events_state(self):
        """Test for the 'events_state' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.events_state'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, ('published', ))

    def test_registry_articles_count(self):
        """Test for the 'articles_count' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.articles_count'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, 8)

    def test_registry_articles_url_en(self):
        """Test for the 'articles_url_en' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.articles_url_en'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, 'articles')

    def test_registry_articles_url_es(self):
        """Test for the 'articles_url_es' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.articles_url_es'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, 'articulos')

    def test_registry_recent_listings_count(self):
        """Test for the 'recent_listings_count' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'recent_listings_count'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, 5)

    def test_registry_recent_listings_url_en(self):
        """Test for the 'recent_listings_url_en' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'recent_listings_url_en'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, 'recent-listings')

    def test_registry_recent_listings_url_es(self):
        """Test for the 'recent_listings_url_es' key and default value."""
        registry = getUtility(IRegistry)
        key = 'customer.mlscrcom.interfaces.IMLSCRComSettings.' \
              'recent_listings_url_es'
        self.assertTrue(key in registry.records.keys())
        self.assertEquals(registry.records.get(key).value, 'ultimas-listados')
