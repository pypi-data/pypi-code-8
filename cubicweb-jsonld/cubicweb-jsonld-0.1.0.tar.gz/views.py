# -*- coding: utf-8 -*-
# copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""
``jsonld`` view implementation for standard resultsets and CW entity types.

Add a ``/<CWEType>.jsonld`` url that provides a jsonld context for instances
of that entity type.
"""

__docformat__ = "restructuredtext en"
_ = unicode


from cubicweb.predicates import is_instance, one_line_rset, any_rset
from cubicweb.view import AnyRsetView, EntityView
from cubicweb.web.views import urlrewrite
from cubicweb.web.views.json import JsonMixIn
from cubicweb.web.views.owl import OWL_TYPE_MAP


class RsetJsonLDView(JsonMixIn, AnyRsetView):
    """jsonld view for any rset

    The output format is inspired by the sparql-results-json one,
    it contains 2 sections:

    - ``head`` with metadata such as RQL variable names or
      RQL limit,

    - ``results`` for the actual resultset data

    "final" cells are serialized as {@value, @type} objects::

      {"@type": "xsd:integer", "@value": 42}

    "entity" cells are serialized as {@context, attrs} objects::

      {
        "@context": "http://my-app.org/MyEtype.jsonld",
        "attr1": "value1",
        "attr2": "value2",
        ...
      }

    """
    __regid__ = 'jsonld'
    __select__ = any_rset()
    title = _('json-ld export')
    content_type = 'application/ld+json'

    def context(self):
        """return general context for the resultset

        Include standard prefixes (e.g. "xsd", "dcterms")
        """
        appid = self._cw.vreg.config.appid
        ctx = {
            'xsd': 'http://www.w3.org/2001/XMLSchema#',
            'cw': 'http://ns.cubicweb.org/cubicweb/0.0/',
            'dcterms': 'http://purl.org/dc/terms/',
        }
        ctx[appid] = self._cw.build_url('CWEType/')
        return ctx


    def call(self):
        data = []
        appid = self._cw.vreg.config.appid
        for rowidx, (rowdescr, row) in enumerate(zip(self.cw_rset.description,
                                                     self.cw_rset.rows)):
            rowdata = []
            for colidx, (celldescr, cell) in enumerate(zip(rowdescr, row)):
                if celldescr is None:
                    rowdata.append({'@type': None, '@value': None})
                elif self._cw.vreg.schema.eschema(celldescr).final:
                    rowdata.append({'@type': OWL_TYPE_MAP[celldescr],
                                    '@value': cell})
                else:
                    entity = self.cw_rset.get_entity(rowidx, colidx)
                    entity.complete()  # fetch all attributes
                    edata = {
                        '@context': self._cw.build_url('{0}.jsonld'.format(entity.cw_etype)),
                        'dcterms:title': entity.dc_title(),
                        'cw:long_title': entity.dc_long_title(),
                        'dcterms:description': entity.dc_description(),
                        '@type': '{0}:{1}'.format(appid, entity.cw_etype),
                    }
                    edata.update(entity.cw_attr_cache.items())
                    rowdata.append(edata)
            data.append(rowdata)
        rqlst = self.cw_rset.syntax_tree()
        self.wdata({
            # context
            '@context': self.context(),
            # head
            'cw:head': {
                'vars': [var.name for var in rqlst.children[0].selection],
                'limit': rqlst.limit,
                'rql': rqlst.as_string(),
                },
            # resultset
            'cw:results': data,
        })


class CWETypeJsonLDView(JsonMixIn, EntityView):
    """jsonld view for an entity type

    The output format is a json-ld context::

        {
            "@context": {
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "creation_date": {
                  "@id": "https://my-app.org/CWRType/creation_date",
                  "@type": "xsd:dateTime"
                },
                ... other metadata ...
                "attr1": {
                  "@id": "https://my-app.org/CWAttribute/278",
                  "@type": "xsd:string"
                },
                ... other attributes ...
            }
        }
    """
    __regid__ = 'jsonld'
    __select__ = (EntityView.__select__ & one_line_rset() &
                  is_instance('CWEType'))
    title = _('json-ld export')
    content_type = 'application/ld+json'

    def context(self, etype):
        ctx = {
            'cwuri': {
                '@id': self._cw.build_url('CWRType/cwuri'),
                '@type': '@id',
            },
            'eid': {
                # NOTE: this URI doesn't resolve
                '@id': self._cw.build_url('CWRType/eid'),
                '@type': 'xsd:integer',
            },
            'creation_date': {
                '@id': self._cw.build_url('CWRType/creation_date'),
                '@type': 'xsd:dateTime',
            },
            'modification_date': {
                '@id': self._cw.build_url('CWRType/modification_date'),
                '@type': 'xsd:dateTime',
            },
        }
        eschema = self._cw.vreg.schema.eschema(etype)
        for attrschema, destschema in eschema.attribute_definitions():
            if attrschema.meta:
                continue  # metadata are already defined in the global context
            ctx[attrschema.type] = {
                '@id': self.attrdef_uri(etype, attrschema.type),
                '@type': OWL_TYPE_MAP[destschema.type],
                }
        return ctx


    def attrdef_uri(self, etype, attr):
        """return the uri of the ``CWAttribute`` corresponding to
        ``<etype>.<attr>``
        """
        rset = self._cw.execute(
            'Any X WHERE X is CWAttribute, X relation_type RT, '
            'RT name %(rn)s, X from_entity ET, ET name %(et)s',
            {'rn': attr, 'et': etype})
        if rset:
            return self._cw.build_url('CWAttribute/{0}'.format(rset[0][0]))
        else:
            return None


    def call(self):
        etype = self.cw_rset.get_entity(0, 0).name
        self.wdata({'@context': self.context(etype)})


# add /{cwetype}.jsonld urls to cubicweb
urlrewrite.SimpleReqRewriter.rules.append(
    (urlrewrite.rgx(r'/(\w+).jsonld$'),
     dict(rql=r'Any X WHERE X is CWEType, X name "\1"',
          vid='jsonld'))
)
