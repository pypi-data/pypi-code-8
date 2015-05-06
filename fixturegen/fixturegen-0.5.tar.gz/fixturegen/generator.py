from pkg_resources import Requirement, resource_filename

from mako.template import Template
from sqlalchemy import MetaData, select, create_engine, text
from sqlalchemy.exc import ArgumentError
from fixturegen.exc import NoSuchTable, WrongDSN

_FIXTURE_TEMPLATE = 'fixturegen/templates/fixture.mako'


def sqlalchemy_data(table, dsn, limit=None, where=None, order_by=None):
    try:
        engine = create_engine(dsn)
    except ArgumentError:
        raise WrongDSN
    metadata = MetaData(bind=engine, reflect=True)
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


def generate(table, columns, rows, with_import=True, fixture_class_name=None):
    if not fixture_class_name:
        camel_case_table = table.replace('_', ' ').title().replace(' ', '')
        fixture_class_name = camel_case_table + 'Data'

    filename = resource_filename(Requirement.parse('fixturegen'),
                                 _FIXTURE_TEMPLATE)
    template = Template(filename=filename)
    return template.render(table=table, columns=columns,
                           rows=rows, with_import=with_import,
                           fixture_class_name=fixture_class_name)
