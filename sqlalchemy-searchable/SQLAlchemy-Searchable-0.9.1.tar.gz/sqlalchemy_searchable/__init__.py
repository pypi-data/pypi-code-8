import re
from itertools import chain

import sqlalchemy as sa
from pyparsing import ParseException
from sqlalchemy import event
from sqlalchemy.schema import DDL
from sqlalchemy_utils import TSVectorType

from .parser import SearchQueryParser
from .vectorizers import Vectorizer

__version__ = '0.9.1'


parser = SearchQueryParser()
vectorizer = Vectorizer()


def parse_search_query(query, parser=parser):
    query = query.strip()
    # Convert hyphens between words to spaces but leave all hyphens which are
    # at the beginning of the word (negation operator)
    query = re.sub(r'(?i)(?<=[^\s|^])-(?=[^\s])', ' ', query)

    parts = query.split()
    parts = [
        parser.remove_special_chars(part).strip() for part in parts if part
    ]
    query = ' '.join(parts)
    if not query:
        return u''
    try:
        return parser.parse(query)
    except ParseException:
        return u''


class SearchQueryMixin(object):
    def search(self, search_query, vector=None, regconfig=None, sort=False):
        """
        Search given query with full text search.

        :param search_query: the search query
        :param vector: search vector to use
        :param regconfig: postgresql regconfig to be used
        :param sort: order results by relevance (quality of hit)
        """
        return search(
            self,
            search_query,
            vector=vector,
            regconfig=regconfig,
            sort=sort
        )


def inspect_search_vectors(entity):
    return [
        getattr(entity, key).property.columns[0]
        for key, column
        in sa.inspect(entity).columns.items()
        if isinstance(column.type, TSVectorType)
    ]


def search(query, search_query, vector=None, regconfig=None, sort=False):
    """
    Search given query with full text search.

    :param search_query: the search query
    :param vector: search vector to use
    :param regconfig: postgresql regconfig to be used
    :param sort: order results by relevance (quality of hit)
    """
    if not search_query:
        return query

    search_query = parse_search_query(search_query)
    if not search_query:
        return query

    if vector is None:
        entity = query._entities[0].entity_zero.class_
        search_vectors = inspect_search_vectors(entity)
        vector = search_vectors[0]

    kwargs = {}
    if regconfig is not None:
        kwargs['postgresql_regconfig'] = regconfig

    query = query.filter(vector.match(search_query, **kwargs))
    if sort:
        query = query.order_by(
            sa.desc(
                sa.func.ts_rank_cd(
                    vector,
                    sa.func.to_tsquery(search_query)
                )
            )
        )

    return query.params(term=search_query)


def quote_identifier(identifier):
    """Adds double quotes to given identifier. Since PostgreSQL is the only
    supported dialect we don't need dialect specific stuff here"""
    return '"%s"' % identifier


class SQLConstruct(object):
    def __init__(
        self,
        tsvector_column,
        conn=None,
        indexed_columns=None,
        options=None
    ):
        self.table = tsvector_column.table
        self.tsvector_column = tsvector_column
        self.conn = conn
        self.options = self.init_options(options)
        if indexed_columns:
            self.indexed_columns = list(indexed_columns)
        else:
            self.indexed_columns = list(self.tsvector_column.type.columns)
        self.params = {}

    def init_options(self, options=None):
        if not options:
            options = {}
        for key, value in SearchManager.default_options.items():
            try:
                option = self.tsvector_column.type.options[key]
            except (KeyError, AttributeError):
                option = value
            options.setdefault(key, option)
        return options

    @property
    def table_name(self):
        if self.table.schema:
            return '%s."%s"' % (self.table.schema, self.table.name)
        else:
            return '"' + self.table.name + '"'

    @property
    def search_function_name(self):
        return self.options['search_trigger_function_name'].format(
            table=self.table.name,
            column=self.tsvector_column.name
        )

    @property
    def search_trigger_name(self):
        return self.options['search_trigger_name'].format(
            table=self.table.name,
            column=self.tsvector_column.name
        )

    def format_column(self, column):
        value = sa.text('NEW.{column}'.format(column=column.name))
        try:
            vectorizer_func = vectorizer[column]
        except KeyError:
            pass
        else:
            value = vectorizer_func(value)
        value = sa.func.coalesce(value, sa.text("''"))

        if self.options['remove_symbols']:
            value = sa.func.regexp_replace(
                value,
                sa.text("'[{0}]'".format(self.options['remove_symbols'])),
                sa.text("' '"),
                sa.text("'g'")
            )
        return value

    @property
    def search_function_args(self):
        args = (
            (
                self.format_column(getattr(self.table.c, column_name)),
                sa.text("' '")
            )
            for column_name in self.indexed_columns
        )
        compiled = sa.func.concat(*chain(*args)).compile(self.conn)
        self.params = compiled.params
        return compiled


class CreateSearchFunctionSQL(SQLConstruct):
    def __str__(self):
        return (
            """CREATE FUNCTION
                {search_trigger_function_name}() RETURNS TRIGGER AS $$
            BEGIN
                NEW.{search_vector_name} = to_tsvector(
                    {arguments}
                );
                RETURN NEW;
            END
            $$ LANGUAGE 'plpgsql';
            """
        ).format(
            search_trigger_function_name=self.search_function_name,
            search_vector_name=self.tsvector_column.name,
            arguments="'%s', %s" % (
                self.options['regconfig'],
                self.search_function_args
            )
        )


class CreateSearchTriggerSQL(SQLConstruct):
    @property
    def search_trigger_function_with_trigger_args(self):
        if self.options['remove_symbols']:
            return self.search_function_name + '()'
        return 'tsvector_update_trigger({arguments})'.format(
            arguments=', '.join(
                [
                    self.tsvector_column.name,
                    "'%s'" % self.options['regconfig']
                ] +
                self.indexed_columns
            )
        )

    def __str__(self):
        return (
            "CREATE TRIGGER {search_trigger_name}"
            " BEFORE UPDATE OR INSERT ON {table}"
            " FOR EACH ROW EXECUTE PROCEDURE"
            " {procedure_ddl}"
            .format(
                search_trigger_name=self.search_trigger_name,
                table=self.table_name,
                procedure_ddl=(
                    self.search_trigger_function_with_trigger_args
                )
            )
        )


class DropSearchFunctionSQL(SQLConstruct):
    def __str__(self):
        return 'DROP FUNCTION IF EXISTS %s()' % self.search_function_name


class DropSearchTriggerSQL(SQLConstruct):
    def __str__(self):
        return 'DROP TRIGGER IF EXISTS %s ON %s' % (
            self.search_trigger_name,
            self.table_name
        )


class SearchManager():
    default_options = {
        'remove_symbols': '-@.',
        'search_trigger_name': '{table}_{column}_trigger',
        'search_trigger_function_name': '{table}_{column}_update',
        'regconfig': 'pg_catalog.english'
    }

    def __init__(self, options={}):
        self.options = self.default_options
        self.options.update(options)
        self.processed_columns = []
        self.classes = set()

    def option(self, column, name):
        try:
            return column.type.options[name]
        except (AttributeError, KeyError):
            return self.options[name]

    def search_function_ddl(self, column):
        def after_create(target, connection, **kw):
            clause = CreateSearchFunctionSQL(column, conn=connection)
            connection.execute(str(clause), **clause.params)
        return after_create

    def search_trigger_ddl(self, column):
        """
        Returns the ddl for creating an automatically updated search trigger.

        :param column: TSVectorType typed SQLAlchemy column object
        """
        return DDL(str(CreateSearchTriggerSQL(column)))

    def inspect_columns(self, cls):
        """
        Inspects all searchable columns for given class.

        :param cls: SQLAlchemy declarative class
        """
        return [
            column for column in cls.__table__.c
            if isinstance(column.type, TSVectorType)
        ]

    def append_index(self, cls, column):
        if not hasattr(cls, '__table_args__') or cls.__table_args__ is None:
            cls.__table_args__ = []
        cls.__table_args__ = list(cls.__table_args__).append(
            sa.Index(
                '_'.join(('ix', column.table.name, column.name)),
                column,
                postgresql_using='gin'
            )
        )

    def process_mapper(self, mapper, cls):
        columns = self.inspect_columns(cls)
        for column in columns:
            if column in self.processed_columns:
                continue

            self.append_index(cls, column)

            self.processed_columns.append(column)

    def attach_ddl_listeners(self):
        for column in self.processed_columns:
            # This sets up the trigger that keeps the tsvector column up to
            # date.
            if column.type.columns:
                table = column.table
                if self.option(column, 'remove_symbols'):
                    event.listen(
                        table,
                        'after_create',
                        self.search_function_ddl(column)
                    )
                    event.listen(
                        table,
                        'after_drop',
                        DDL(str(DropSearchFunctionSQL(column)))
                    )
                event.listen(
                    table,
                    'after_create',
                    self.search_trigger_ddl(column)
                )


search_manager = SearchManager()


def sync_trigger(
    conn,
    table_name,
    tsvector_column,
    indexed_columns,
    metadata=None,
    options=None
):
    """
    Synchronizes search trigger and trigger function for given table and given
    search index column. Internally this function executes the following SQL
    queries:

    * Drops search trigger for given table (if it exists)
    * Drops search function for given table (if it exists)
    * Creates search function for given table
    * Creates search trigger for given table
    * Updates all rows for given search vector by running a column=column
      update query for given table.


    Example::

        from sqlalchemy_searchable import sync_trigger


        sync_trigger(
            conn,
            'article',
            'search_vector',
            ['name', 'content']
        )


    This function is especially useful when working with alembic migrations.
    In the following example we add a content column to article table and then
    sync the trigger to contain this new column. ::


        from alembic import op
        from sqlalchemy_searchable import sync_trigger


        def upgrade():
            conn = op.get_bind()
            op.add_column('article', sa.Column('content', sa.Text))

            sync_trigger(conn, 'article', 'search_vector', ['name', 'content'])

        # ... same for downgrade


    If you are using vectorizers you need to initialize them in your migration
    file and pass them to this function. ::


        import sqlalchemy as sa
        from alembic import op
        from sqlalchemy.dialects.postgresql import HSTORE
        from sqlalchemy_searchable import sync_trigger, vectorizer


        def upgrade():
            vectorizer.clear()

            conn = op.get_bind()
            op.add_column('article', sa.Column('name_translations', sa.Text))

            metadata = sa.MetaData(bind=conn)
            articles = sa.Table('article', metadata, autoload=True)

            @vectorizer(article.c.content)
            def hstore_vectorizer(column):
                return sa.cast(sa.func.avals(column), sa.Text)

            op.add_column('article', sa.Column('name_translations', sa.Text))
            sync_trigger(
                conn,
                'article',
                'search_vector',
                ['name_translations', 'content'],
                metadata=metadata
            )

        # ... same for downgrade

    :param conn: SQLAlchemy Connection object
    :param table_name: name of the table to apply search trigger syncing
    :param tsvector_column:
        TSVector typed column which is used as the search index column
    :param indexed_columns:
        Full text indexed column names as a list
    :param metadata:
        Optional SQLAlchemy metadata object that is being used for autoloaded
        Table. If None is given then new MetaData object is initialized within
        this function.
    :param options: Dictionary of configuration options
    """
    if metadata is None:
        metadata = sa.MetaData()
    table = sa.Table(
        table_name,
        metadata,
        autoload=True,
        autoload_with=conn
    )
    params = dict(
        tsvector_column=getattr(table.c, tsvector_column),
        indexed_columns=indexed_columns,
        options=options,
        conn=conn
    )
    classes = [
        DropSearchTriggerSQL,
        DropSearchFunctionSQL,
        CreateSearchFunctionSQL,
        CreateSearchTriggerSQL,
    ]
    for class_ in classes:
        sql = class_(**params)
        conn.execute(str(sql), **sql.params)
    update_sql = table.update().values(
        {indexed_columns[0]: sa.text(indexed_columns[0])}
    )
    conn.execute(update_sql)


def make_searchable(
    mapper=sa.orm.mapper,
    manager=search_manager,
    options={}
):
    manager.options.update(options)
    event.listen(
        mapper, 'instrument_class', manager.process_mapper
    )
    event.listen(
        mapper, 'after_configured', manager.attach_ddl_listeners
    )
