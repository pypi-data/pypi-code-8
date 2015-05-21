from __future__ import absolute_import
import unittest
import tornado.testing
import os
import json
try:
    import mock
except ImportError:
    noMock = True

from ..db import Reader, NotFound
from ..rest import Application

@unittest.skipIf('noMock' in locals(), 'no mock module installed')
class RestDummyDbServer(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        mockdb = mock.Mock(Reader)
        return Application(mockdb)

    def test_invalid_pair(self):
        self._app.db.get_matches_between_genomes.side_effect = NotFound
        res = self.fetch('/api/matches/3/4')
        self.assertEqual(res.error.code, 404, "invalid genome pairs should result in 404 errors")


class RestTestDbServer(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        db = Reader(os.path.join(os.path.dirname(__file__), "TestDb.h5"))
        self.dbfilehandle = db._fh
        from ..settings import settings
        return Application(db, test=True, **settings)

    def test_retrieve_genomelist(self):
        res = self.fetch('/api/genomes/')
        self.assertEqual(res.code, 200)
        payload = json.loads(res.body)
        gs = self.dbfilehandle.get_node('/Genomes/Summaries').col('NCBITaxonId').tolist()
        self.assertEqual(len(payload), len(gs), u"wrong number of genomes")
        self.assertEqual([z['NCBITaxonId'] for z in payload], gs, u"Taxonomy ids don't match")

    def test_retrieve_sequences(self):
        gs = self.dbfilehandle.get_node('/Genomes/Summaries').read(0, 1)
        res = self.fetch('/api/genomes/{}'.format(gs[0]['NCBITaxonId']))
        self.assertEqual(res.code, 200)
        payload = json.loads(res.body)
        self.assertEqual(len(payload), gs[0]['TotEntries'])

    def test_invalid_genome(self):
        gs = self.dbfilehandle.get_node('/Genomes/Summaries').read(0, 1)
        res = self.fetch('/api/genomes/{}'.format(gs[0]['NCBITaxonId']+1))
        self.assertEqual(res.code, 404)

    def test_with_complex_accept_header(self):
        res = self.fetch('/', headers={"accept": "text/html,application/xhtml+xml,"
                                                 "application/xml;q=0.9,*/*;q=0.8"})
        self.assertEqual(res.code, 200)

    def tearDown(self):
        self.dbfilehandle.close()



if __name__ == '__main__':
    unittest.main()
