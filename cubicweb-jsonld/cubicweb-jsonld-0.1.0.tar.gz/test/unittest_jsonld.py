import unittest
from functools import partial

from cubicweb.devtools.testlib import CubicWebTC, JsonValidator
from cubicweb.entities import AnyEntity
from cubicweb.web.views.urlrewrite import SimpleReqRewriter


class MyGroupImpl(AnyEntity):
    """custom CWGroup entity class to be able to test jsonld exports"""
    __regid__ = 'CWGroup'

    def dc_title(self):
        return u'the dc title'

    def dc_long_title(self):
        return u'the dc long title'

    def dc_description(self, format='text/plain'):
        return u'the dc description'


CubicWebTC.content_type_validators['application/ld+json'] = JsonValidator


class JsonLDTests(CubicWebTC):

    def setUp(self):
        super(JsonLDTests, self).setUp()
        self.config.appid = 'myapp'
        self.vreg['etypes'].clear_caches()

    def _attrdef_url(self, req, etype, attrname):
        attr_eid = req.execute(
            """Any X WHERE X is CWAttribute, X from_entity E,
                           E name %(en)s, X relation_type R, R name %(rn)s
            """, {'en': etype, 'rn': attrname})[0][0]
        return req.build_url('CWAttribute/{0}'.format(attr_eid))

    def test_cwuser_jsonld(self):
        with self.admin_access.web_request() as req:
            rset = req.execute('Any X WHERE X is CWEType, X name "CWUser"')
            url = req.build_url
            attr_url = partial(self._attrdef_url, req, 'CWUser')
            with open('cwuser.jsonld', 'w') as f:
                import json
                json.dump(self.view('jsonld', rset, req=req), f)
            self.assertEqual(self.view('jsonld', rset, req=req), {
                '@context': {
                    # metadata
                    u'creation_date': {
                        u'@id': url('CWRType/creation_date'),
                        u'@type': u'xsd:dateTime'
                    },
                    u'modification_date': {
                        u'@id': url('CWRType/modification_date'),
                        u'@type': u'xsd:dateTime'
                    },
                    u'cwuri': {
                        u'@id': url('CWRType/cwuri'),
                        u'@type': u'@id'
                    },
                    u'eid': {
                        u'@id': url('CWRType/eid'),
                        u'@type': u'xsd:integer'
                    },
                    u'firstname': {
                        u'@id': attr_url('firstname'),
                        u'@type': u'xsd:string'
                    },
                    u'last_login_time': {
                        u'@id': attr_url('last_login_time'),
                        u'@type': u'xsd:dateTime'
                    },
                    u'login': {
                        u'@id': attr_url('login'),
                        u'@type': u'xsd:string'
                    },
                    u'surname': {
                        u'@id': attr_url('surname'),
                        u'@type': u'xsd:string'
                    },
                    u'upassword': {
                        u'@id': attr_url('upassword'),
                        u'@type': u'xsd:byte'
                    },
                }
            })


    def test_cwetype_jsonld_url(self):
        with self.admin_access.web_request() as req:
            rewriter = SimpleReqRewriter(req)
            rewriter.rewrite(req, '/CWUser.jsonld')
            self.assertEqual(req.form['vid'], 'jsonld')
            self.assertEqual(req.form['rql'], 'Any X WHERE X is CWEType, X name "CWUser"')


    def test_rset_jsonld(self):
        with self.admin_access.web_request() as req:
            rset = req.execute('Any G,GN ORDERBY GN WHERE G is CWGroup, G name GN')
            jsonld = self.view('jsonld', rset, req=req)
            self.assertEqual(jsonld['@context'], {
                u'xsd': u'http://www.w3.org/2001/XMLSchema#',
                u'cw': u'http://ns.cubicweb.org/cubicweb/0.0/',
                u'dcterms': u'http://purl.org/dc/terms/',
                u'myapp': u'http://testing.fr/cubicweb/CWEType/',
            })
            self.assertEqual(jsonld['cw:head'], {
                'rql': 'Any G,GN ORDERBY GN WHERE G is CWGroup, G name GN',
                'limit': None,
                'vars': ['G', 'GN'],
            })
            self.assertEqual(len(jsonld['cw:results']), len(rset))
            self.assertTrue(all(len(row) == 2 for row in jsonld['cw:results']))
            url = req.build_url
            guests = rset.get_entity(0, 0)
            managers = rset.get_entity(1, 0)
            self.assertEqual(jsonld['cw:results'][:2], [
                [{u'@context': url('CWGroup.jsonld'),
                  u'@type': u'myapp:CWGroup',
                  u'creation_date': guests.creation_date.strftime('%Y/%m/%d %H:%M:%S'),
                  u'cw:long_title': u'guests',
                  u'cwuri': url(guests.eid),
                  u'dcterms:description': u'',
                  u'dcterms:title': u'guests',
                  u'modification_date': guests.modification_date.strftime('%Y/%m/%d %H:%M:%S'),
                  u'name': u'guests'},
                 {u'@type': u'xsd:string',
                  u'@value': u'guests'}],
                [{u'@context': url('CWGroup.jsonld'),
                  u'@type': u'myapp:CWGroup',
                  u'creation_date': managers.creation_date.strftime('%Y/%m/%d %H:%M:%S'),
                  u'cw:long_title': u'managers',
                  u'cwuri': url(managers.eid),
                  u'dcterms:description': u'',
                  u'dcterms:title': u'managers',
                  u'modification_date': managers.modification_date.strftime('%Y/%m/%d %H:%M:%S'),
                  u'name': u'managers'},
                 {u'@type': u'xsd:string',
                  u'@value': u'managers'}],
            ])


    def test_rset_jsonld_head_limit(self):
        with self.admin_access.web_request() as req:
            rset = req.execute('Any G,GN LIMIT 1 WHERE G is CWGroup, G name GN')
            jsonld = self.view('jsonld', rset, req=req)
            self.assertEqual(jsonld['cw:head'], {
                'rql': 'Any G,GN LIMIT 1 WHERE G is CWGroup, G name GN',
                'limit': 1,
                'vars': ['G', 'GN'],
            })

    def test_rset_jsonld_dc_properties(self):
        with self.admin_access.web_request() as req:
            # register custom implementation to check that dc methods are
            # actually used
            self.vreg.register(MyGroupImpl)
            rset = req.execute('Any G WHERE G is CWGroup, G name "managers"')
            jsonld_value = self.view('jsonld', rset, req=req)['cw:results'][0][0]
            self.assertEqual(jsonld_value['dcterms:title'],
                             u'the dc title')
            self.assertEqual(jsonld_value['cw:long_title'],
                             u'the dc long title')
            self.assertEqual(jsonld_value['dcterms:description'],
                             u'the dc description')



if __name__ == '__main__':
    unittest.main()
