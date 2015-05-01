import sqlalchemy
import pandas as pd
import h5py
import glob
import pandas.io.sql
from cStringIO import StringIO
from datetime import datetime


class PgSQLDatabase(pandas.io.sql.SQLDatabase):
    # FIXME Schema is pulled from Meta object, shouldn't actually be part of signature!
    def to_sql(self, frame, name, if_exists='fail', index=True,
               index_label=None, schema=None, chunksize=None, dtype=None, pk=None):
        """
        Write records stored in a DataFrame to a SQL database.

        Parameters
        ----------
        frame : DataFrame
        name : string
            Name of SQL table
        if_exists : {'fail', 'replace', 'append'}, default 'fail'
            - fail: If table exists, do nothing.
            - replace: If table exists, drop it, recreate it, and insert data.
            - append: If table exists, insert data. Create if does not exist.
        index : boolean, default True
            Write DataFrame index as a column
        index_label : string or sequence, default None
            Column label for index column(s). If None is given (default) and
            `index` is True, then the index names are used.
            A sequence should be given if the DataFrame uses MultiIndex.
        schema : string, default None
            Name of SQL schema in database to write to (if database flavor
            supports this). If specified, this overwrites the default
            schema of the SQLDatabase object.
        chunksize : int, default None
            If not None, then rows will be written in batches of this size at a
            time.  If None, all rows will be written at once.
        dtype : dict of column name to SQL type, default None
            Optional specifying the datatype for columns. The SQL type should
            be a SQLAlchemy type.
        pk: name of column(s) to set as primary keys
        """
        if dtype is not None:
            import sqlalchemy.sql.type_api as type_api

            for col, my_type in dtype.items():
                if not issubclass(my_type, type_api.TypeEngine):
                    raise ValueError('The type of %s is not a SQLAlchemy '
                                     'type ' % col)

        table = pandas.io.sql.SQLTable(name, self, frame=frame, index=index,
                                       if_exists=if_exists, index_label=index_label,
                                       schema=self.meta.schema, dtype=dtype)
        table.create()
        if pk is not None:
            if isinstance(pk, str):
                pks = pk
            else:
                pks = ", ".join(pk)
            sql = "ALTER TABLE {schema_name}.{table_name} ADD PRIMARY KEY ({pks})".format(schema_name=self.meta.schema, table_name=name, pks=pks)
            self.execute(sql)

        # Some tricks needed here:
        # Need to explicitly keep reference to connection
        # Need to "open" temp file seperately in write and read mode
        # Otherwise data does not get loaded
        conn = self.engine.raw_connection()
        f = StringIO()
        with conn.cursor() as cur:
            frame.to_csv(f, index=index)
            f.seek(0)

            sql = "COPY {schema_name}.{table_name} FROM STDIN WITH (FORMAT CSV, HEADER TRUE)".format(
                schema_name=self.meta.schema, table_name=name)
            cur.copy_expert(sql, f)
        conn.commit()

        # check for potentially case sensitivity issues (GH7815)
        self.meta.reflect()
        if name not in self.engine.table_names(schema=schema or self.meta.schema):
            import warnings
            warnings.warn("The provided table name '{0}' is not found exactly "
                          "as such in the database after writing the table, "
                          "possibly due to case sensitivity issues. Consider "
                          "using lower case table names.".format(name), UserWarning)


def order(frame,var):
    varlist =[w for w in frame.columns if w not in var]
    frame = frame[var+varlist]
    return frame


class ExperimentsSQL(object):
    def __init__(self, fname_glob):
        self.fname_glob = fname_glob
        self.h5fs = [h5py.File(fname, mode='r')
                     for fname in glob.glob(fname_glob)]

        self.engine = sqlalchemy.create_engine('postgresql://@localhost/temp', echo=False)
        pgdb = PgSQLDatabase(self.engine, meta=sqlalchemy.MetaData(self.engine, schema='public'))

        exp_grs = [(fid, eid, exp_gr)
                   for fid, h5file in enumerate(self.h5fs)
                   for eid, exp_gr in enumerate(h5file.values())
                   if exp_gr.attrs.get('_is_experiment', False)]
        experiments = pd.DataFrame([
            {'fid': fid, 'eid': eid, 'name': gr.attrs['name'], 'time_start': datetime.fromtimestamp(gr.attrs['time_sec'])}
            for fid, eid, gr in exp_grs
        ])
        experiments = order(experiments, ['fid', 'eid', 'name'])
        experiments.to_sql('experiments', self.engine, if_exists='replace', index=False)

        step_grs = [(fid, eid, step_gr.attrs['ind'], step_gr)
                    for fid, eid, exp_gr in exp_grs
                    for step_gr in exp_gr.values()]
        steps = pd.DataFrame([
            {
                'fid': fid,
                'eid': eid,
                'sid': sid,
                'name': gr.attrs['name'],
                'args': '{%s}' % ','.join(gr.attrs['args_names']),
                'results': '{%s}' % ','.join(gr.attrs['results_names']),
                'code': gr.attrs['code'],
                'completed_cnt': gr['scalars'].attrs['written_cnt'],
            }
            for fid, eid, sid, gr in step_grs
        ])
        steps = order(steps, ['fid', 'eid', 'sid', 'name'])
        steps.to_sql('steps', self.engine, if_exists='replace', index=False)

        scalars = pd.DataFrame([
            dict({'fid': fid, 'eid': eid, 'sid': sid, 'rid': run_id}.items() +
                [(k, v)
                 for k, v in zip(gr['scalars'].dtype.names, scalar_row)
                 if not isinstance(v, h5py.Reference)]
            )
            for fid, eid, sid, gr in step_grs
            for run_id, scalar_row in enumerate(gr['scalars'])
        ])
        scalars = order(scalars, ['fid', 'eid', 'sid', 'rid'])
        scalars.to_sql('scalars', self.engine, if_exists='replace', index=False)

        df_names = {k
            for fid, eid, sid, gr in step_grs
            for k, (v, _) in gr['scalars'].dtype.fields.items()
            if v.kind == 'O'
        }
        for df_name in df_names:
            df = pd.DataFrame([
                dict(
                    {'fid': fid, 'eid': eid, 'sid': sid, 'rid': run_id}.items() +
                    zip(df.dtype.names, df_row)
                )
                for fid, eid, sid, gr in step_grs
                for ind in [gr.attrs['ind']]
                for scalars in [gr['scalars']]
                for run_id, scalar_row in enumerate(scalars[...])
                for df in [gr[scalar_row[df_name]]]
                for df_row in df[...]
            ])
            df = order(df, ['fid', 'eid', 'sid', 'rid'])
            pgdb.to_sql(df, df_name, if_exists='replace', index=False)

    def close(self):
        pass

    def pd(self, query):
        return pd.read_sql(query, self.engine)
