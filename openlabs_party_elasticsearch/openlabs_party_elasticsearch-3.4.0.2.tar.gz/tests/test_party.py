# -*- coding: utf-8 -*-
"""
    test_party.py

    TestParty

    :copyright: (c) 2014-2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import time
import unittest

import trytond.tests.test_tryton
from trytond.tests.test_tryton import DB_NAME, USER, CONTEXT, POOL
from trytond.transaction import Transaction

from trytond.config import config
# Add elastic search test configuration
config.add_section('elastic_search')
config.set('elastic_search', 'server_uri', "localhost:9200")


class TestParty(unittest.TestCase):
    """
    Test Party
    """

    def setUp(self):
        trytond.tests.test_tryton.install_module('party_elasticsearch')
        self.Party = POOL.get('party.party')
        self.IndexBacklog = POOL.get('elasticsearch.index_backlog')
        self.ElasticDocumentType = POOL.get('elasticsearch.document.type')
        self.ElasticConfig = POOL.get('elasticsearch.configuration')

    def update_mapping(self):
        """
        Update mapping.
        """
        party_doc, = self.ElasticDocumentType.search([
            ('model.model', '=', 'party.party')
        ])
        self.ElasticConfig.update_settings([self.ElasticConfig(1)])
        self.ElasticDocumentType.update_mapping([party_doc])

    def create_parties(self):
        return self.Party.create([
            {
                'name': 'User 1',
                'code': '11',
                'addresses': [
                    ('create', [{
                        'name': 'User 1',
                        'city': 'California',
                    }])
                ],
            },
            {
                'name': 'User 2',
                'code': '21',
                'addresses': [
                    ('create', [{
                        'name': 'User 2',
                        'city': 'Maine',
                    }])
                ],
            }
        ])

    def test_0010_test_party_indexing(self):
        """
        Tests indexing on creation and updation of party
        """
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.update_mapping()
            Address = POOL.get('party.address')
            Country = POOL.get('country.country')

            party, = self.Party.create([{
                'name': 'Bruce Wayne',
            }])
            self.assertEqual(self.IndexBacklog.search([], count=True), 1)
            # Clear backlog list
            self.IndexBacklog.delete(self.IndexBacklog.search([]))
            self.assertEqual(self.IndexBacklog.search([], count=True), 0)

            # Update the party address
            country, = Country.create([{
                'name': 'United States',
                'code': 'US',
            }])
            address, = Address.create([{
                'name': 'Bruce Wayne',
                'city': 'Gotham',
                'party': party.id,
            }])
            self.assertEqual(self.IndexBacklog.search([], count=True), 1)

            # Update the party address
            Address.write([address], {
                'name': 'Bruce Wayne',
                'city': 'Gotham',
            })
            self.assertEqual(self.IndexBacklog.search([], count=True), 1)

            # Create 2 parties
            party1, party2 = self.create_parties()

            # Update index on Elastic-Search server
            self.IndexBacklog.update_index()
            time.sleep(2)

    def test_0020_test_party_search(self):
        """
        Test the search logic
        """
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.update_mapping()
            # Create 5 parties
            self.Party.create([
                {
                    'name': 'Sharoon Thomas',
                },
                {
                    'name': 'Prakash Pandey',
                },
                {
                    'name': 'Tarun Bhardwaj',
                },
                {
                    'name': 'Rituparna Panda',
                },
                {
                    'name': 'Gaurav Butola',
                },
            ])

            # Test cases for search
            results = self.Party.search([])
            self.assertEqual(len(results), 5)

            results = self.Party.search([('rec_name', 'ilike', '%thomas%')])
            self.assertEqual(len(results), 1)
            self.assert_(results[0].id)

            result1 = self.Party.search([
                ('rec_name', 'ilike', '%thomas%'),
                ('rec_name', 'ilike', '%haroon%'),
            ])
            self.assertEqual(len(result1), 1)
            self.assert_(result1[0].id)

            result1 = self.Party.search([('name', 'ilike', '%thomas%')])
            self.assertEqual(len(result1), 1)
            self.assert_(result1[0].id)

            self.Party.search_name('thomas 12345')

            # Remove elastic search configuration and search again, it
            # should not blow up
            config.remove_section('elastic_search')
            result1 = self.Party.search([('rec_name', 'ilike', '%thomas%')])
            self.assertEqual(len(result1), 1)


def suite():
    "Define suite"
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestParty)
    )
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
