import datetime
import re

from sqlalchemy import util, sql
from sqlalchemy import types as sqltypes
from sqlalchemy.engine import default, reflection
from sqlalchemy.sql import compiler

RESERVED_WORDS = \
    set(
        # keywords
        'ALL AND AS AVG BETWEEN BITS BOTH BREAK BY CALL CASCADE CASE CAST '
        'CATCH COLLATE COLUMN CONSTRAINT CONTAINING CONTINUE COUNT '
        'CREATE CURRENT CURRENT_SCHEMA CURRENT_DATE CURRENT_TIME CURRENT_TIMESTAMP '
        'CURRENT_USER DEFAULT DELETE DESCRIBE DISTINCT DOMAIN ELSE END END_FOR END_IF '
        'END_PROCEDURE END_TRIGGER END_TRY END_WHILE ENUM ESCAPE '
        'EXECUTE EXISTS FALSE FETCH FOR FOREIGN FOR_UPDATE FROM FULL '
        'GENERATED GROUP HAVING IDENTITY IF INNER INOUT INSERT INTO IN '
        'IS JOIN KEY LEADING LEFT LIKE LIMIT LOGICAL_AND LOGICAL_NOT '
        'LOGICAL_OR MAX MIN NATIONAL NATURAL NCHAR NCLOB NEXT NEXT_VALUE '
        'NOT NOT_BETWEEN NOT_CONTAINING NOT_IN NOT_LIKE NOT_STARTING NOW NTEXT '
        'NULL NUMERIC NVARCHAR OCTETS OFF OFFSET ON ONLY ORDER OUT PRIMARY '
        'PROCEDURE REAL RECORD_BATCHING REFERENCES REGEXP RESTRICT RETURNS RETURN '
        'RIGHT ROLLBACK ROWS SECURITY SELECT SET SHOW SMALLDATETIME '
        'SMALLINT STARTING STRING_TYPE SUM THEN THROW TINYBLOB TINYINT '
        'TO TRAILING TRUE TRY UNION UNIQUE UNKNOWN UPDATE USING VAR VER '
        'WHEN WHERE WHILE WITH '
        # built-in functions
        'ABS ACOS ASIN ATAN2 ATAN BIT_LENGTH CAST CEILING CHARACTER_LENGTH '
        'COALESCE CONCAT CONVERT_TZ COS COT CURRENT_USER DATE DATE_ADD DATE_SUB '
        'DAYOFWEEK DAY DEGREES EXTRACT FLOOR GREATEST HOUR IFNULL LEAST LOCATE '
        'LOWER LTRIM MINUTE MOD MONTH MSLEEP NOW NULLIF OCTET_LENGTH PI POWER '
        'RADIANS RAND REPLACE ROUND RTRIM SECOND SIN SQRT SUBSTRING_INDEX '
        'SUBSTR TAN TRIM UPPER USER YEAR'.split()
    )


def print_list(*args):  # pragma: no cover
    if args is None:
        print("None list")
    if args is not None:
        for count, thing in enumerate(args):
            print('{0}. {1}'.format(count, thing))


def print_kwargs(**kwargs):  # pragma: no cover
    for key, value in kwargs.items():
        print("%s = %s" % (key, value))


def print_set(arg):  # pragma: no cover
    print(", ".join(str(e) for e in arg))


class _NuoDate(sqltypes.Date):
    def bind_processor(self, dialect):
        def process(value):
            if type(value) == datetime.date:
                return datetime.datetime(value.year, value.month, value.day)
            else:
                return value

        return process

    _reg = re.compile(r"(\d+)-(\d+)-(\d+)")

    def result_processor(self, dialect, coltype):
        def process(value):
            if isinstance(value, datetime.datetime):
                return value.date()
            elif isinstance(value, util.string_types):
                return datetime.date(*[
                    int(x or 0)
                    for x in self._reg.match(value).groups()
                    ])
            else:
                return value

        return process

    def literal_processor(self, dialect):
        def process(value):
            return "'%s'" % value

        return process


class _NuoTime(sqltypes.Time):
    def bind_processor(self, dialect):
        def process(value):
            if type(value) == datetime.date:
                return value.time()
            else:
                return value

        return process

    _reg = re.compile(r"(\d+):(\d+):(\d+)(?:\.(\d{0,6}))?")

    def result_processor(self, dialect, coltype):
        def process(value):
            if isinstance(value, datetime.datetime):
                return value.time()
            elif isinstance(value, util.string_types):
                return datetime.time(*[
                    int(x or 0)
                    for x in self._reg.match(value).groups()
                    ])
            else:
                return value

        return process

    def literal_processor(self, dialect):
        def process(value):
            return "'%s'" % value

        return process


class _NuoDateTime(sqltypes.DateTime):
    def literal_processor(self, dialect):
        def process(value):
            return "'%s'" % value

        return process


class NUMBER(sqltypes.Numeric):
    __visit_name__ = 'NUMBER'

    def __init__(self, precision=None, scale=None, asdecimal=None):
        # Precision and scale are fixed for NuoDB NUMBER types.
        super(NUMBER, self).__init__(
            precision=9, scale=0, asdecimal=asdecimal)


colspecs = {
    sqltypes.Date: _NuoDate,
    sqltypes.Time: _NuoTime,
    sqltypes.DateTime: _NuoDateTime,
}

ischema_names = {
    'BIGINT': sqltypes.BIGINT,
    'BINARY': sqltypes.BINARY,
    'BOOLEAN': sqltypes.BOOLEAN,
    'BLOB': sqltypes.BLOB,
    'BOOL': sqltypes.BOOLEAN,
    'CHAR': sqltypes.CHAR,
    'CLOB': sqltypes.CLOB,
    'DATE': sqltypes.DATE,
    'DATETIME': sqltypes.DATETIME,
    'DECIMAL': sqltypes.DECIMAL,
    'DOUBLE': sqltypes.FLOAT,
    'ENUM': sqltypes.Enum,
    'FLOAT': sqltypes.FLOAT,
    'INT': sqltypes.INTEGER,
    'INTEGER': sqltypes.INTEGER,
    'NCHAR': sqltypes.NCHAR,
    'NUMBER': NUMBER,
    'NUMERIC': sqltypes.NUMERIC,
    'SMALLINT': sqltypes.SMALLINT,
    'STRING': sqltypes.VARCHAR,
    'TEXT': sqltypes.TEXT,
    'TIME': sqltypes.TIME,
    'TIMESTAMP': sqltypes.DATETIME,
    'VARBINARY': sqltypes.VARBINARY,
    'VARCHAR': sqltypes.VARCHAR,
}


class NuoDBCompiler(compiler.SQLCompiler):
    def default_from(self):
        return " FROM DUAL"

    def render_literal_value(self, value, type_):
        if issubclass(type(value), datetime.date):
            return "'" + str(value) + "'"
        else:
            return super(NuoDBCompiler, self). \
                render_literal_value(value, type_)

    def limit_clause(self, select, **kw):
        if select._limit_clause is None and select._offset_clause is None:
            text = ''
        elif select._offset_clause is not None:
            if select._limit_clause is None:
                # no limit provided but offset is provided...
                text = ' \n LIMIT %s OFFSET %s' % (
                    "2147483647",
                    self.process(select._offset_clause, **kw))
            else:
                # both offset and limit are provided...
                text = ' \n LIMIT %s OFFSET %s' % (
                    self.process(select._limit_clause, **kw),
                    self.process(select._offset_clause, **kw))
        else:
            # no offset provided...
            text = ' \n LIMIT %s' % (self.process(select._limit_clause, **kw),)
        return text

    def visit_localtime_func(self, func, **kw):
        return 'CURRENT_TIME'

    def visit_localtimestamp_func(self, func, **kw):
        return 'CURRENT_TIMESTAMP'

    def visit_user_func(self, func, **kw):
        return 'CURRENT_USER'

    def visit_session_user_func(self, func, **kw):
        return 'CURRENT_USER'

    def visit_random_func(self, func, **kw):
        return 'rand%(expr)s'


class NuoDBIdentifierPreparer(compiler.IdentifierPreparer):
    reserved_words = set([x.lower() for x in RESERVED_WORDS])

    def __init__(self, dialect, server_ansiquotes=True, **kw):
        if not server_ansiquotes:
            quote = "`"
        else:
            quote = '"'
        super(NuoDBIdentifierPreparer, self).__init__(
            dialect,
            initial_quote=quote,
            escape_quote=quote)


class NuoDBTypeCompiler(compiler.GenericTypeCompiler):
    def visit_VARCHAR(self, type_, **kw):
        return "STRING" if type_.length in (None, 0) else \
            "VARCHAR(%(length)s)" % {'length': type_.length}

    def visit_enum(self, type_, **kw):
        if not type_.native_enum:
            return super(NuoDBTypeCompiler, self).visit_enum(type_)
        else:
            return self._visit_enumerated_values("ENUM", type_, type_.enums)

    def _visit_enumerated_values(self, name, type_, enumerated_values):
        # note, type_ will end up being a VARCHAR(5), not sure why
        # sql alchemy won't coerce to a ENUM when they are declared
        # as native, but here we go with a hack around this foolery...
        quoted_enums = []
        for e in enumerated_values:
            quoted_enums.append("'%s'" % e.replace("'", "''"))
        return "%s (%s)" % (name, ",".join(quoted_enums))

    def visit_NUMBER(self, type_, **kw):
        # NUMBER in NuoDB is special in that it takes
        # no precision or scale arguments.
        return 'NUMBER'


class NuoDBDDLCompiler(compiler.DDLCompiler):
    def get_column_specification(self, column, **kwargs):
        colspec = self.preparer.format_column(column) + " " + \
                  self.dialect.type_compiler.process(column.type,
                                                     type_expression=column)

        if column is column.table._autoincrement_column:
            colspec += " GENERATED BY DEFAULT AS IDENTITY"
        else:
            default_ = self.get_column_default_string(column)
            if default_ is not None:
                colspec += " DEFAULT " + default_

        if not column.nullable:
            colspec += " NOT NULL"
        return colspec

    def visit_create_sequence(self, create):
        text = "CREATE SEQUENCE %s" % \
               self.preparer.format_sequence(create.element)
        if create.element.start is not None:
            text += " START WITH %d" % create.element.start
        return text


class NuoDBExecutionContext(default.DefaultExecutionContext):
    def fire_sequence(self, seq, type_):
        return self._execute_scalar(
            (
                "SELECT NEXT VALUE FOR %s FROM DUAL" %
                self.dialect.identifier_preparer.format_sequence(seq)
            ), type_)


class NuoDBDialect(default.DefaultDialect):
    name = 'nuodb'

    colspecs = colspecs
    ischema_names = ischema_names
    type_compiler = NuoDBTypeCompiler
    statement_compiler = NuoDBCompiler
    preparer = NuoDBIdentifierPreparer
    ddl_compiler = NuoDBDDLCompiler
    execution_ctx_cls = NuoDBExecutionContext

    supports_sequences = True
    sequences_optional = False
    supports_default_values = True
    supports_native_enum = True
    supports_native_boolean = True
    supports_alter = True
    postfetch_lastrowid = False
    implicit_returning = False
    max_identifier_length = 128
    max_index_name_length = 128
    case_sensitive = False
    supports_native_decimal = True
    supports_empty_insert = False

    def normalize_name(self, name):
        if name is None or not name:
            return None
        if name.upper() == name and not \
                self.identifier_preparer._requires_quotes(name.lower()):
            return name.lower()
        else:
            return name

    def denormalize_name(self, name):
        if name is None:
            return None
        elif name.lower() == name and not \
                self.identifier_preparer._requires_quotes(name.lower()):
            name = name.upper()
        return name

    def _get_default_schema_name(self, connection):
        return self.normalize_name(
            connection.execute('SELECT CURRENT_SCHEMA FROM DUAL').scalar())

    def has_table(self, connection, table_name, schema=None):
        schema = self.denormalize_name(schema or self.default_schema_name)
        cursor = connection.execute(
            sql.text("SELECT tablename FROM system.tables "
                     "WHERE tablename = :table_name AND schema = :schema_name"),
            table_name=table_name,
            schema_name=schema)
        return bool(cursor.first())

    def has_schema(self, connection, schema):
        schema = self.denormalize_name(schema or self.default_schema_name)
        cursor = connection.execute(
            sql.text("SELECT schema FROM system.schemas "
                     "WHERE schema = :schema_name"),
            schema_name=schema)
        return cursor.first() is not None

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        cursor = connection.execute("SELECT schema FROM system.schemas ORDER BY schema")
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_temp_table_names(self, connection, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)
        cursor = connection.execute(
            sql.text("SELECT tablename FROM system.temptables"),
        )
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)
        cursor = connection.execute(
            sql.text("SELECT tablename FROM system.tables "
                     "WHERE type = 'TABLE' AND schema = :schema_name"),
            schema_name=schema)
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)
        cursor = connection.execute(
            sql.text("SELECT viewname FROM system.view_tables "
                     "WHERE viewschema = :schema_name"),
            schema_name=schema)
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_view_definition(self, connection, view_name, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)
        cursor = connection.execute(
            sql.text("SELECT viewdefinition FROM system.tables "
                     "WHERE type = 'VIEW' AND schema = :schema_name AND tablename = :table_name"
                     ),
            table_name=view_name,
            schema_name=schema)
        return cursor.scalar()

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):  # pragma: no cover
        schema = self.denormalize_name(schema or self.default_schema_name)
        # layout
        fk = {'name': None, 'constrained_columns': [], 'referred_schema': None, 'referred_table': None,
              'referred_columns': []}
        foreign_keys_info = []
        # todo
        return foreign_keys_info

    @reflection.cache
    def get_unique_constraints(self, connection, table_name, schema=None, **kw):  # pragma: no cover
        schema = self.denormalize_name(schema or self.default_schema_name)

        # TODO PROBLEM: Nuo splits temp tables away from ordinary tables, as
        # such this and other methods become rather complicated.

        # loads up the index names and unique flags...
        indexes = []
        cursor = connection.execute(
            sql.text("SELECT indexname "
                     "FROM system.indexes "
                     "WHERE indextype = 1 AND schema = :schema_name AND tablename = :table_name"
                     ),
            table_name=table_name,
            schema_name=schema)
        for (indexname,) in cursor:
            indexes.append(dict(name=self.normalize_name(indexname), column_names=[]))
        # print_list(indexes)

        # loads up the column names...
        for index in indexes:
            cursor = connection.execute(
                sql.text("SELECT field "
                         "FROM system.indexfields "
                         "WHERE schema = :schema_name AND tablename = :table_name AND indexname = :index_name "
                         "ORDER BY position"),
                index_name=index['name'],
                table_name=table_name,
                schema_name=schema)
            for (field,) in cursor:
                index['column_names'].append(field)

        # print "table: %s@%s" % (schema, table_name)
        # print_list(indexes)
        return indexes

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)

        # loads up the index names and unique flags...
        indexes = []
        cursor = connection.execute(
            sql.text("SELECT indexname, "
                     "CAST((indextype = 1) as boolean) AS isunique "
                     "FROM system.indexes "
                     "WHERE indextype >= 1 AND schema = :schema_name AND tablename = :table_name"),
            table_name=table_name,
            schema_name=schema)

        for (indexname, isunique,) in cursor:
            indexes.append(dict(name=self.normalize_name(indexname), column_names=[], unique=bool(isunique)))

        # loads up the column names...
        for index in indexes:
            cursor = connection.execute(
                sql.text("SELECT field "
                         "FROM system.indexfields "
                         "WHERE schema = :schema_name AND tablename = :table_name AND indexname = :index_name "
                         "ORDER BY position"),
                index_name=index['name'],
                table_name=table_name,
                schema_name=schema)
            for (field,) in cursor:
                index['column_names'].append(self.normalize_name(field))

        if len(indexes) == 0:
            # temp table support...
            cursor = connection.execute(
                sql.text("SELECT indexname, "
                         "CAST((indextype = 1) as boolean) AS isunique "
                         "FROM system.tempindexes "
                         "WHERE indextype >= 1 AND tablename = :table_name"),
                table_name=table_name,
                schema_name=schema)

            for (indexname, isunique,) in cursor:
                indexes.append(dict(name=self.normalize_name(indexname), column_names=[], unique=bool(isunique)))

            # loads up the column names...
            for index in indexes:
                cursor = connection.execute(
                    sql.text("SELECT field "
                             "FROM system.tempindexfields "
                             "WHERE tablename = :table_name AND indexname = :index_name "
                             "ORDER BY position"),
                    index_name=index['name'],
                    table_name=table_name,
                    schema_name=schema)
                for (field,) in cursor:
                    index['column_names'].append(self.normalize_name(field))

        # print_list(indexes)
        return indexes

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)
        cursor = connection.execute(
            sql.text("SELECT x.indexname, f.field "
                     "FROM system.indexfields AS f "
                     "INNER JOIN system.indexes AS x "
                     "ON x.indexname = f.indexname "
                     "WHERE x.indextype = 0 AND x.schema = :schema_name "
                     "AND x.schema = f.schema AND x.tablename = :table_name "
                     "AND x.tablename = f.tablename "
                     "ORDER BY position"),
            table_name=table_name,
            schema_name=schema)

        pk_constraints = {'constrained_columns': [], 'name': None}
        for (indexname, field,) in cursor:
            if pk_constraints['name'] is None:
                pk_constraints['name'] = indexname
            pk_constraints['constrained_columns'].append(self.normalize_name(field))

        return pk_constraints

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)

        columns = []

        cursor = connection.execute(
            sql.text(
                "SELECT field AS name, "
                "UPPER(datatypes.name) AS type, "
                "CAST(((flags & 1) ^ 1) as boolean) AS nullable, "
                "defaultvalue AS default, "
                "generator_sequence IS NOT NULL AS autoincrement, "
                "generator_sequence AS sequence, "
                "length, "
                "precision, "
                "scale, "
                "declared_type AS typename "
                "FROM system.fields "
                "INNER JOIN system.datatypes "
                "ON datatypes.id = datatype "
                "WHERE schema = :schema_name AND tablename = :table_name"
            ),  # todo order by position?
            table_name=table_name,
            schema_name=schema)

        for (name, type_, nullable, default_, autoincrement, sequence, length, precision, scale, typename) in cursor:
            columns.append(
                self._get_column_info(
                    self.normalize_name(name), type_, nullable, default_,
                    autoincrement, sequence, length, precision, scale, typename))

        if len(columns) == 0:
            # temp table support...
            cursor = connection.execute(
                sql.text(
                    "SELECT field AS name, "
                    "UPPER(datatypes.name) AS type, "
                    "CAST(((flags & 1) ^ 1) as boolean) AS nullable, "
                    "defaultvalue AS default, "
                    "generator_sequence IS NOT NULL AS autoincrement, "
                    "generator_sequence AS sequence, "
                    "length, "
                    "precision, "
                    "scale, "
                    "declared_type AS typename "
                    "FROM system.tempfields "
                    "INNER JOIN system.datatypes "
                    "ON datatypes.id = datatype "
                    "WHERE tablename = :table_name "
                ),  # todo order by position?
                table_name=table_name,
                schema_name=schema)
            for (
                    name, type_, nullable, default_, autoincrement, sequence, length, precision, scale,
                    typename) in cursor:
                columns.append(
                    self._get_column_info(
                        self.normalize_name(name), type_, nullable, default_,
                        autoincrement, sequence, length, precision, scale, typename))

        # print "table name: %s" % table_name
        return columns

    def _normalize_declared_type(self, typename):
        return typename.upper().split('(', 1)[0]

    def _get_column_info(self, name, type_, nullable, default_, autoincrement, sequence, length, precision, scale,
                         typename):
        coltype = None
        typename = self._normalize_declared_type(typename)
        if typename in ('INTEGER', 'BIGINT', 'NUMERIC', 'DECIMAL'):
            # adjust data types as nuo uses bigint as a storage data type
            # for several other data types, so we need to coerce them.
            coltype = typename
        coltype = self.ischema_names.get(typename, None)

        # If you see this sort of error:
        #
        #    sqlalchemy_nuodb/base.py:627: SAWarning: Did not recognize type 'TIMESTAMP'
        #       of column 'invoicedate' (type_, name))
        #
        # This means you need to add an alias for the unrecognized datatype to the
        # ischema_names mapping table.

        if sequence is None:
            sequence = dict()

        if coltype == 'NUMBER':
            coltype = NUMBER

        if coltype in (sqltypes.NUMERIC, sqltypes.DECIMAL, NUMBER):
            args = (precision, scale)
        elif coltype == sqltypes.FLOAT:
            args = (precision,)
        elif coltype in (sqltypes.CHAR, sqltypes.VARCHAR, sqltypes.NCHAR):
            args = (length,)
        else:
            args = ()

        kwargs = {}
        if coltype:
            coltype = coltype(*args, **kwargs)
        else:
            util.warn("Did not recognize type '%s' of column '%s'" %
                      (type_, name))
            coltype = sqltypes.NULLTYPE

        column_info = dict(name=name, type=coltype, nullable=bool(nullable),
                           default=default_, autoincrement=autoincrement)  # , sequence=sequence)
        # print "%s" % (column_info)
        return column_info

    def has_sequence(self, connection, sequence_name, schema=None):
        if schema is None:
            cursor = connection.execute(
                sql.text("SELECT sequencename FROM system.sequences "
                         "WHERE sequencename = :sequence_name AND schema = current_schema()"),
                sequence_name=sequence_name)
        else:
            cursor = connection.execute(
                sql.text("SELECT sequencename FROM system.sequences "
                         "WHERE sequencename = :sequence_name AND schema = :schema_name"),
                sequence_name=sequence_name,
                schema_name=schema)
        return bool(cursor.first())
