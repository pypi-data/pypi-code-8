# -*- coding: utf-8 -*-
"""
    party.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import re

from pyes.query import QueryStringQuery, BoolQuery
from trytond.pool import Pool, PoolMeta

__metaclass__ = PoolMeta
__all__ = ['Party', 'Address']

ZIP_RE = re.compile(r'(\d{5})')


class Party:
    __name__ = "party.party"

    def elastic_search_json(self):
        """
        Return a JSON serializable dictionary
        """
        return {
            'id': self.id,
            'name': self.rec_name,
            'code': self.code,
            'addresses': [{
                'full_address': address.full_address
            } for address in self.addresses],
            'contact_mechanisms': [{
                'type': mech.type,
                'value': mech.value,
            } for mech in self.contact_mechanisms],
        }

    @classmethod
    def search_name(cls, search_phrase, limit=100, fields=None):
        """
        Search on elasticsearch server for the given search phrase
        """
        config = Pool().get('elasticsearch.configuration')(1)

        # Create connection with elastic server
        conn = config.get_es_connection(timeout=5)

        if conn is None:
            return []

        search_phrase = search_phrase.replace('%', '')

        # Search the query string in all fields
        query = BoolQuery(
            should=[
                QueryStringQuery(search_phrase, default_field='name'),
                QueryStringQuery(search_phrase, default_field='name.partial'),
                QueryStringQuery(search_phrase, default_field='name.metaphone'),
            ]
        )

        # Handle the zip codes specially
        zip_codes = ZIP_RE.findall(search_phrase)
        if filter(None, zip_codes):
            query.add_should(
                QueryStringQuery(
                    ' '.join(zip_codes),
                    default_field='addresses.full_address', boost=4
                )
            )

        # TODO: Handle fields
        return conn.search(
            query,
            doc_types=[config.make_type_name('party.party')],
            size=limit
        )

    @classmethod
    def search(
            cls, domain, offset=0, limit=None, order=None, count=False,
            query=False):
        """
        Plug elastic search in to efficiently search queries which meet the
        full text search criteria.
        """
        logger = Pool().get('elasticsearch.configuration').get_logger()

        if not domain:
            return super(Party, cls).search(
                domain, offset, limit, order, count
            )

        for clause in domain:
            if clause and clause[0] != 'rec_name':
                return super(Party, cls).search(
                    domain, offset, limit, order, count, query,
                )
        else:
            # gets executed only if the search is for records with
            # rec_name only. This cannot be implemented on search_rec_name
            # because a query on the GTK client for "tom sawyer" would
            # return a two clause domain and search_rec_name will get
            # called twice
            search_phrase = ' '.join([c[2] for c in filter(None, domain)])
            results = cls.browse([
                r.id for r in
                cls.search_name(search_phrase, limit=limit, fields=["id"])
            ])
            if not results:
                logger.info(
                    "Search for %s resulted in no results" % search_phrase
                )
                # If the server returned nothing, we might as well
                # fallback on trytond
                results = super(Party, cls).search(
                    domain, offset, limit, order, count, query,
                )
                logger.info(
                    "Search for %s resulted in tryton yielded: %d results" % (
                        search_phrase, len(results)
                    )
                )
            return results


class Address:
    __name__ = "party.address"

    @classmethod
    def create(cls, vlist):
        """
        Create a record in elastic search on create for address
        :param vlist: List of dictionaries of fields with values
        """
        IndexBacklog = Pool().get('elasticsearch.index_backlog')

        addresses = super(Address, cls).create(vlist)
        IndexBacklog.create_from_records([a.party for a in addresses])
        return addresses

    @classmethod
    def write(cls, addresses, values, *args):
        """
        Create a record in elastic search on write for the address
        """
        IndexBacklog = Pool().get('elasticsearch.index_backlog')
        rv = super(Address, cls).write(addresses, values, *args)
        IndexBacklog.create_from_records([a.party for a in addresses])
        return rv
