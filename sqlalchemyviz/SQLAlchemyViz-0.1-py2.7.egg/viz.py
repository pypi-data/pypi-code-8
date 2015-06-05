# -*- coding: utf-8 -*-
# Copyright (C) 2015 Sebastian Eckweiler
#
# This module is part of SQLAlchemyViz and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import unicode_literals
"""
Module containing the graph building logic.
"""

import itertools
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


from sqlalchemy import (MetaData, ForeignKeyConstraint,
                        UniqueConstraint, PrimaryKeyConstraint,
                        Index, CheckConstraint)

import pydot
from pydot import Node, Edge, Dot

ONE = '1'
ONE_TO_N = '1-n'
ZERO_TO_N = '0-n'
ZERO_TO_ONE = '0-1'


default_config = {'cell_align': 'left',
                  'table_border': '0',
                  'table_cellborder': '0',
                  'table_cellspacing': '0',
                  'table_bgcolor': 'azure2',
                  'node_shape': 'box',
                  'node_margin': '0,0',
                  'graph_bgcolor': 'transparent',
                  'graph_orientation': 'portrait',
                  'edge_dir': 'both',
                  'edge_len': '3'}

arrowstyles = {ONE: "noneteetee",
               ZERO_TO_ONE: "noneteeodot",
               ZERO_TO_N: "crowodot",
               ONE_TO_N: "crowtee"}


column_fmt = '%(name)s : %(type)s'

_valid_configs = dict(graph=pydot.GRAPH_ATTRIBUTES.copy(),
                      edge=pydot.EDGE_ATTRIBUTES.copy(),
                      node=pydot.NODE_ATTRIBUTES.copy(),
                      table={"align", "bgcolor", "border", "cellborder",
                             "cellpadding", "cellspacing", "color",
                             "columns", "fixedsize", "gradientangle",
                             "height", "href", "id", "port", "rows",
                             "sides", "style", "target", "title",
                             "tooltip", "valign", "width"},
                      cell={"align", "balign", "bgcolor", "border",
                            "cellpadding", "cellspacing", "color",
                            "colspan", "fixedsize", "gradientangle",
                            "height", "href", "id", "port", "rowspan",
                            "sides", "style", "target", "title", "tooltip",
                            "valign", "width"})
# all
_valid_configs[None] = (_valid_configs['graph'] |
                        _valid_configs['edge'] |
                        _valid_configs['table'] |
                        _valid_configs['cell'] |
                        _valid_configs['node'])

class ERDiagram(object):

    _prefixes = {ForeignKeyConstraint: 'FK',
                 PrimaryKeyConstraint: 'PK',
                 Index: 'IX',
                 CheckConstraint: 'CK',
                 UniqueConstraint: 'UQ'}

    _COLS = '4'

    def __init__(self, meta, **kwargs):
        """

        :param MetaData meta: MetaData describing the schema
        :return:
        """

        self.meta = meta
        self.graph = None
        self.use_pytypes = False
        self.sort_columns = kwargs.pop('sort_columns', True)
        self._config = default_config.copy()

        if kwargs:
            raise ValueError('Unknown options: %s' %
                             (',' % ['%r' for key in kwargs]))

    def update_config(self, config):
        self._config.update(config)

    def create_diagram(self):

        self.graph = Dot(splines='ortho',
                         overlap='scale',
                         **self._get_config('graph'))

        tables = list(self.meta.sorted_tables)
        for t in tables:
            self._create_node(t)

        for t in tables:
            self._create_edges(t)

    # noinspection PyShadowingBuiltins
    def write(self, path, prog='neato', format=None):

        if not self.graph:
            self.create_diagram()

        if not format:
            _, format = os.path.splitext(path)
            if format.startswith('.'):
                format = format[1:]

        self.graph.write(path, prog, format)

    def _get_config(self, prefix):

        c = dict()
        for prefix_key, value in self._config.items():
            prefix_key = prefix_key.lower()

            if '_' in prefix_key:
                pfx, key = prefix_key.split('_', 1)
            else:
                pfx, key = None, prefix_key

            if pfx not in _valid_configs:
                valid = str(filter(None, _valid_configs))
                raise ValueError('"%s" is not a valid configuration group. '
                                 'Must be one of %s.' %
                                 (pfx, valid))

            if key not in _valid_configs[pfx]:
                valid = str(sorted(_valid_configs[pfx]))
                raise ValueError('"%s" is not a valid configuration key. '
                                 'Valid ones are: %s.' %
                                 (key, valid))

            if pfx is None or pfx == prefix:
                c[key] = value
        return c

    def _create_node(self, table):

        t = self._make_table()
        header = ET.Element('B')
        header.text = table.name
        self._make_cell(t, header,
                        border='1', sides='b',
                        colspan=self._COLS)

        cols = table.columns
        if self.sort_columns:
            cols = sorted(cols, key=lambda c: c.name)

        for col in cols:
            r = self._make_row(t)
            attrs = self._column_attrs(col)

            flag = ""
            if attrs["primary"]:
                flag += "P"
            else:
                if attrs["unique"]:
                    flag += "U"
                if attrs["foreign"]:
                    flag += "F"
            if not flag:
                flag = " "

            if attrs["nullable"]:
                nullable = ' '
            else:
                nullable = '*'

            self._make_cell(r, flag)
            self._make_cell(r, nullable)
            self._make_cell(r, '%(name)s' % attrs)
            self._make_cell(r, '%(type)s' % attrs)

        # sort constraints by type:
        order = {PrimaryKeyConstraint: 0,
                 ForeignKeyConstraint: 1,
                 UniqueConstraint: 2,
                 CheckConstraint: 3,
                 Index: 4}

        constraints = sorted(table.constraints,
                             key=lambda c: order[type(c)])
        const_and_index = itertools.chain(constraints,
                                          table.indexes)

        for i, c_or_idx in enumerate(const_and_index):
            if isinstance(c_or_idx, CheckConstraint):
                continue

            if c_or_idx.name:
                s = '%s' % c_or_idx.name
            else:
                s = '(%s)' % ','.join(col.name for col in c_or_idx.columns)

            opts = dict(border='0' if i else '1',
                        sides='' if i else 't',
                        colspan='2')

            r = self._make_row(t)
            self._make_cell(r, self._prefixes[type(c_or_idx)], **opts)
            self._make_cell(r, s, **opts)

        node = Node(table.name,
                    label='<%s>' % ET.tostring(t, method='html'),
                    **self._get_config('node'))
        self.graph.add_node(node)

    def _column_attrs(self, col):

        if self.use_pytypes:
            type_name = col.type.python_type.__name__
        else:
            type_name = unicode(col.type)
        col_props = {"name": col.name,
                     "type": type_name,
                     "unique": False,
                     "nullable": col.nullable,
                     "primary": col.primary_key,
                     "foreign": bool(col.foreign_keys)}

        flags = []
        if col.primary_key:
            flags.append('P')

        unique = any(col.name in cstr.columns
                     for cstr in col.table.constraints
                     if isinstance(cstr, UniqueConstraint)
                     and len(cstr.columns) == 1)

        if unique or col.unique:
            col_props["unique"] = unique or col.unique

        return col_props

    def _create_edges(self, table):

        for edge in self._get_edges(table):
            self.graph.add_edge(edge)

    def _get_edges(self, table):

        unique_cols = set(tuple(c.columns)
                          for c in table.constraints
                          if isinstance(c, (UniqueConstraint,
                                            PrimaryKeyConstraint)))

        edge_attributes = self._get_config('edge')
        for constraint in table.constraints:
            if not isinstance(constraint, ForeignKeyConstraint):
                continue

            # foreign table:
            ref_table = constraint.elements[0].column.table
            nullable = any(c.nullable for c in constraint.columns)
            unique = tuple(constraint.columns) in unique_cols

            # is also a primary key?
            primary_key = any(c.primary_key for c in constraint.columns)

            n_tail = ZERO_TO_ONE if nullable else ONE
            n_head = ONE if unique else ONE_TO_N
            style = 'solid' if primary_key else 'dashed'

            edge_attributes['arrowtail'] = arrowstyles[n_tail]
            edge_attributes['arrowhead'] = arrowstyles[n_head]
            edge_attributes['style'] = style
            yield Edge(table.name, ref_table.name,
                       **edge_attributes)

    def _make_table(self):
        return ET.Element('TABLE', **self._get_config('table'))

    def _make_row(self, parent):
        return ET.SubElement(parent, 'TR')

    def _make_cell(self, parent, contents='', **kwargs):

        if parent.tag == 'TABLE':
            parent = self._make_row(parent)

        attrib = self._get_config('cell').copy()
        attrib.update(kwargs)
        c = ET.SubElement(parent, 'TD', **attrib)
        if ET.iselement(contents):
            c.append(contents)
        else:
            c.text = contents
        return c


def dump_diagram(meta, path, diagram_opts=None, prog='neato', format=None, **kwargs):

    dia = ERDiagram(meta, **kwargs)
    if diagram_opts:
        dia.update_config(diagram_opts)

    dia.write(path, prog, format)
    print 'Wrote %s.' % path
