from __future__ import absolute_import
from functools import partial
from pkg_resources import Requirement, resource_filename
import re

from mako.template import Template
from sqlalchemy import MetaData, select, create_engine, text
from sqlalchemy.exc import ArgumentError

from fixturegen.exc import (
    NoSuchTable,
    WrongDSN,
    WrongNamingColumn,
    NonValidRowClassName
)

_FIXTURE_TEMPLATE = 'fixturegen/templates/fixture.mako'

valid_class_name_re = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


def sqlalchemy_data(table, dsn, limit=None, where=None, order_by=None):
    try:
        engine = create_engine(dsn)
    except ArgumentError:
        raise WrongDSN
    metadata = MetaData()
    metadata.reflect(bind=engine)
    try:
        mapped_table = metadata.tables[table]
    except KeyError:
        raise NoSuchTable
    query = select(mapped_table.columns)
    if where:
        query = query.where(whereclause=text(where))
    if order_by:
        query = query.order_by(text(order_by))
    if limit:
        query = query.limit(limit)
    columns = [column.name for column in mapped_table.columns]
    rows = engine.execute(query).fetchall()
    return table, tuple(columns), tuple(rows)


def get_row_class_name(row, table_name, naming_column_ids):
    class_name = '{0}_{1}'.format(table_name, '_'
                                  .join((str(row[i]).replace('-', '_')
                                        for i in naming_column_ids)))
    if valid_class_name_re.match(class_name):
        return class_name
    raise NonValidRowClassName(class_name)


def generate(table, columns, rows, with_import=True,
             fixture_class_name=None, row_naming_columns=None):
    if not row_naming_columns:
        try:
            naming_column_ids = [columns.index('id')]
        except ValueError:
            raise WrongNamingColumn()
    else:
        try:
            naming_column_ids = [columns.index(column_name)
                                 for column_name in row_naming_columns]
        except ValueError:
            raise WrongNamingColumn()

    row_class_name = partial(get_row_class_name, table_name=table,
                             naming_column_ids=naming_column_ids)

    if not fixture_class_name:
        camel_case_table = table.replace('_', ' ').title().replace(' ', '')
        fixture_class_name = camel_case_table + 'Data'

    filename = resource_filename(Requirement.parse('fixturegen'),
                                 _FIXTURE_TEMPLATE)
    template = Template(filename=filename)
    return template.render(table=table, columns=columns,
                           rows=rows, with_import=with_import,
                           fixture_class_name=fixture_class_name,
                           row_class_name=row_class_name)
