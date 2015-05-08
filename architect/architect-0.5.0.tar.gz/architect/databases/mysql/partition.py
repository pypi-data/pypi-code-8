"""
MySQL supports partitioning natively via PARTITION BY clause. Unfortunately
MySQL doesn't support dynamic sql in triggers or functions/procedures that
are called within triggers, so the only way to create partitions automatically
is to calculate everything at the python level, then to create needed sql
statements based on calculations and issue that statement into the database.
"""

from ..bases import BasePartition
from ..utilities import DateTime
from ...exceptions import (
    PartitionRangeSubtypeError,
    PartitionConstraintError,
    PartitionFunctionError
)


class Partition(BasePartition):
    def prepare(self):
        """
        Prepares table for partitioning by reconstructing table's primary key.
        """
        if self.column_name not in self.pks:
            self.database.execute("""
                ALTER TABLE {parent_table} DROP PRIMARY KEY, ADD PRIMARY KEY ({pk}, {column});
            """.format(pk=', '.join(pk for pk in self.pks), parent_table=self.table, column=self.column_name))

        return self.database.execute("""
            DROP PROCEDURE IF EXISTS {parent_table}_create_partition;

            DELIMITER $$
            CREATE PROCEDURE {parent_table}_create_partition(IN column_value VARCHAR(255))
            BEGIN
                DECLARE
                    tablename VARCHAR(255);
                    columntype VARCHAR(30);
                    {declarations}

                {common_variables}

                IF NOT EXISTS(
                    SELECT 1 FROM information_schema.partitions
                    WHERE table_name='{parent_table}' AND partition_name=tablename})
                THEN
                    SELECT data_type INTO columntype
                    FROM information_schema.columns
                    WHERE table_name = '{parent_table}' AND column_name = '{column}';

                    {creation_variables}

                    SET @sql := CONCAT(
                        'ALTER TABLE {parent_table} ADD PARTITION ('
                            {checks}
                        ');'
                    );

                    PREPARE stmt FROM @sql;
                    EXECUTE stmt;
                    DEALLOCATE PREPARE stmt;
                END IF;
            END $$
            DELIMITER ;
        """.format(parent_table=self.table))

    def exists(self):
        """
        Checks if partition exists. Not used in this backend because everything is done at the stored procedure level.
        """
        return False

    def create(self):
        """
        Creates new partition.
        """
        return self.database.execute("""
            CALL {parent_table}_create_partition({value});
        """).format(parent_table=self.table, value=self.column_value)

    def _get_definitions(self):
        """
        Returns needed definitions for chosen partition type/subtype.
        """
        raise NotImplementedError('Method "_get_definitions" not implemented in: {0}'.format(self.__class__.__name__))


class RangePartition(Partition):
    """
    Range partition type implementation.
    """
    def __init__(self, model, **meta):
        super(RangePartition, self).__init__(model, **meta)
        self.constraint = meta['constraint']
        self.subtype = meta['subtype']
        self.datetime = DateTime(self.column_value)

# SELECT '2015-04-17' + INTERVAL 1 DAY
# SELECT DATE_SUB('2015-04-05', INTERVAL WEEKDAY('2015-04-05') DAY) + INTERVAL 1 WEEK
# SELECT DATE_FORMAT('2015-04-17', '%Y-%m-01') + INTERVAL 1 MONTH
# SELECT DATE_FORMAT('2015-04-17', '%Y-01-01') + INTERVAL 1 YEAR
#
# select DATE_FORMAT('2015-04-20', 'y%Yw%v')

    def prepare(self):
        """
        Prepares table for partitioning by creating zero partition to speed up things due to
        the partitioning implementation in the early versions of MySQL database (see bug #49754)
        """
        super(RangePartition, self).prepare()
        print("""
            ALTER TABLE {parent_table} PARTITION BY RANGE (MONTH({column}))(
                PARTITION {pattern} VALUES LESS THAN (MONTH(DATE_FORMAT('2015-04-17', '%Y-%m-01') + INTERVAL 1 month))
            );
        """.format(
            parent_table=self.table,
            column=self.column_name,
            pattern=self._get_name(),
            function=self._get_function()
        ))

    def create(self):
        """
        Creates new partition.
        """
        return """
            PARTITION {child_table} VALUES LESS THAN ({function}('{period_end}') + {addition})
        """.format(
            child_table=self._get_name(),
            function=self._get_function(),
            period_end=self.datetime.get_period(self.constraint)[1],
            addition='86400' if self._get_column_type() == 'timestamp' else '1'
        )

    def _get_date_definitions(self):
        """
        Returns definitions for date partition subtype.
        """
        patterns = {
            'day': '"y"YYYY"d"DDD',
            'week': '"y"IYYY"w"IW',
            'month': '"y"YYYY"m"MM',
            'year': '"y"YYYY',
        }

        try:
            pattern = patterns[self.constraint]
        except KeyError:
            raise PartitionConstraintError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.constraint,
                allowed=patterns.keys())

        return {
            'formatters': {'pattern': pattern},
            'declarations': [],
            'variables': [
                "match := DATE_TRUNC('{constraint}', NEW.{{column}});",
                "tablename := '{{parent_table}}_' || TO_CHAR(NEW.{{column}}, '{pattern}');"
            ],
            'checks': [
                "'{{column}} >= ''' || match || ''' AND {{column}} < ''' || (match + INTERVAL '1 {constraint}') || ''''"
            ]
        }

    def _get_name(self):
        """
        Dynamically defines new partition name depending on the partition subtype.
        """
        try:
            return getattr(self, '_get_{0}_name'.format(self.subtype))()
        except AttributeError:
            import re
            expression = '_get_(\w+)_name'
            raise PartitionRangeSubtypeError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.subtype,
                allowed=[re.match(expression, c).group(1) for c in dir(self) if re.match(expression, c) is not None])

    def _get_date_name(self):
        """
        Defines name for a new partition for date partition subtype.
        """
        patterns = {
            'day': {'real': 'y%Yd%j', 'none': 'y0000d000'},
            'week': {'real': 'y%Yw%V', 'none': 'y0000w00'},
            'month': {'real': 'y%Ym%m', 'none': 'y0000m00'},
            'year': {'real': 'y%Y', 'none': 'y0000'},
        }

        try:
            if self.column_value is None:
                pattern = patterns[self.constraint]['none']
            else:
                pattern = self.column_value.strftime(patterns[self.constraint]['real'])
        except KeyError:
            raise PartitionConstraintError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=self.constraint,
                allowed=patterns.keys())

        return '{0}_{1}'.format(self.table, pattern)

    def _get_function(self):
        """
        Returns correct partition function depending on the MySQL column type.
        """
        functions = {
            'date': 'TO_DAYS',
            'datetime': 'TO_DAYS',
            'timestamp': 'UNIX_TIMESTAMP',
        }

        column_type = self._get_column_type()

        try:
            return functions[column_type]
        except KeyError:
            raise PartitionFunctionError(
                model=self.model.__name__,
                dialect=self.dialect,
                current=column_type,
                allowed=functions.keys())

    def _get_column_type(self):
        """
        Returns real database column type.
        """
        return self.database.select_one("""
            SELECT data_type
            FROM information_schema.columns
            WHERE table_name = '{parent_table}' AND column_name = '{column}';
        """.format(parent_table=self.table, column=self.column_name))
