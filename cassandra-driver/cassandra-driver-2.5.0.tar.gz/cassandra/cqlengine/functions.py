# Copyright 2015 DataStax, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime

from cassandra.cqlengine import UnicodeMixin, ValidationError


class QueryValue(UnicodeMixin):
    """
    Base class for query filter values. Subclasses of these classes can
    be passed into .filter() keyword args
    """

    format_string = '%({})s'

    def __init__(self, value):
        self.value = value
        self.context_id = None

    def __unicode__(self):
        return self.format_string.format(self.context_id)

    def set_context_id(self, ctx_id):
        self.context_id = ctx_id

    def get_context_size(self):
        return 1

    def update_context(self, ctx):
        ctx[str(self.context_id)] = self.value


class BaseQueryFunction(QueryValue):
    """
    Base class for filtering functions. Subclasses of these classes can
    be passed into .filter() and will be translated into CQL functions in
    the resulting query
    """
    pass


class MinTimeUUID(BaseQueryFunction):
    """
    return a fake timeuuid corresponding to the smallest possible timeuuid for the given timestamp

    http://cassandra.apache.org/doc/cql3/CQL.html#timeuuidFun
    """

    format_string = 'MinTimeUUID(%({})s)'

    def __init__(self, value):
        """
        :param value: the time to create a maximum time uuid from
        :type value: datetime
        """
        if not isinstance(value, datetime):
            raise ValidationError('datetime instance is required')
        super(MinTimeUUID, self).__init__(value)

    def to_database(self, val):
        epoch = datetime(1970, 1, 1, tzinfo=val.tzinfo)
        offset = epoch.tzinfo.utcoffset(epoch).total_seconds() if epoch.tzinfo else 0
        return int(((val - epoch).total_seconds() - offset) * 1000)

    def update_context(self, ctx):
        ctx[str(self.context_id)] = self.to_database(self.value)


class MaxTimeUUID(BaseQueryFunction):
    """
    return a fake timeuuid corresponding to the largest possible timeuuid for the given timestamp

    http://cassandra.apache.org/doc/cql3/CQL.html#timeuuidFun
    """

    format_string = 'MaxTimeUUID(%({})s)'

    def __init__(self, value):
        """
        :param value: the time to create a minimum time uuid from
        :type value: datetime
        """
        if not isinstance(value, datetime):
            raise ValidationError('datetime instance is required')
        super(MaxTimeUUID, self).__init__(value)

    def to_database(self, val):
        epoch = datetime(1970, 1, 1, tzinfo=val.tzinfo)
        offset = epoch.tzinfo.utcoffset(epoch).total_seconds() if epoch.tzinfo else 0
        return int(((val - epoch).total_seconds() - offset) * 1000)

    def update_context(self, ctx):
        ctx[str(self.context_id)] = self.to_database(self.value)


class Token(BaseQueryFunction):
    """
    compute the token for a given partition key

    http://cassandra.apache.org/doc/cql3/CQL.html#tokenFun
    """

    def __init__(self, *values):
        if len(values) == 1 and isinstance(values[0], (list, tuple)):
            values = values[0]
        super(Token, self).__init__(values)
        self._columns = None

    def set_columns(self, columns):
        self._columns = columns

    def get_context_size(self):
        return len(self.value)

    def __unicode__(self):
        token_args = ', '.join('%({})s'.format(self.context_id + i) for i in range(self.get_context_size()))
        return "token({})".format(token_args)

    def update_context(self, ctx):
        for i, (col, val) in enumerate(zip(self._columns, self.value)):
            ctx[str(self.context_id + i)] = col.to_database(val)
