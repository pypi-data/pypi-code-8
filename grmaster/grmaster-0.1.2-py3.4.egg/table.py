# -*- coding: utf-8 -*-

"""Immutable table with header."""

#   grmaster - tool for dividing students into groups
#   Copyright (C) 2015  Lutov V. S. <vslutov@yandex.ru>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import tempfile

def _from_csv_str(csv_str):
    """Convert from csv string with header."""
    temp_file = tempfile.SpooledTemporaryFile(10 ** 6, 'w+')  # Max is 1 MB
    temp_file.write(csv_str)
    temp_file.seek(0)
    table = Table.from_csv_file(temp_file)
    temp_file.close()
    return table

def _from_csv_file(input_file):
    """Read csv file with header."""
    opened = False
    if isinstance(input_file, str):
        opened = True
        input_file = open(input_file, 'r')
    table = Table(csv.reader(input_file))
    if opened:
        input_file.close()
    return table

def is_empty(line):
    """Empty csv line."""
    return [''] * len(line) == list(line)

def next_or_empty(reader):
    """Return empty array if reader has ended."""
    try:
        return next(reader)
    except StopIteration:
        return []

class Table:

    """
    Immutable table with header.

    >>> users = Table((('Name', 'Surname', 'City'),
    ...                ('Alex', 'Brown', 'Moscow'),
    ...                ('Ed', 'Wood', 'Hollywood')))
    >>> users.header
    ('Name', 'Surname', 'City')
    >>> users[0]
    ('Alex', 'Brown', 'Moscow')
    """

    from_csv_str = _from_csv_str
    from_csv_file = _from_csv_file

    def __init__(self, input_table):
        """Initialize self.  See help(type(self)) for accurate signature."""
        table = []
        for row in input_table:
            if is_empty(row):
                break
            else:
                table.append(tuple(row))

        self.header = table[0]
        while self.header[-1] == '':
            self.header = self.header[:-1]
        width = len(self.header)

        self.body = tuple(row[:width] for row in table[1:])

    def __str__(self):
        """Return str(self)."""
        width = len(self.header)
        column_lens = [len(head) for head in self.header]

        for row in self:
            for i in range(width):
                column_lens[i] = max(column_lens[i], len(str(row[i])))

        def row_to_string(row):
            """Convert table row to string."""
            def item(i):
                """Nice looking."""
                return str(row[i]).ljust(column_lens[i])
            return '| ' + ' | '.join(item(i) for i in range(width)) + ' |'

        header = row_to_string(self.header)
        body = '\n'.join(row_to_string(row) for row in self)
        return header + '\n' + '-' * len(header) + '\n' + body

    def __repr__(self):
        """Return repr(self)."""
        tuple_repr = repr((self.header,) + tuple(self))
        return type(self).__name__ + '(' + tuple_repr + ')'

    def __getitem__(self, key):
        """Return self[key]."""
        if isinstance(key, int):
            return self.body[key]
        else:  # type(key) is slice
            return type(self)((self.header,) + self.body[key])

    def __len__(self):
        """Return len(self)."""
        return len(self.body)

    def __eq__(self, other):
        """Return self == other."""
        return repr(self) == repr(other)

    def split_by_column(self, index):
        """Return a tuple of tables."""
        cases = set(row[index] for row in self)
        result = []
        for case in cases:
            rows = tuple(row for row in self if row[index] == case)
            result.append(Table((self.header,) + rows))

        return result

    def split_by_header(self, header):
        """Return a tuple of tables."""
        return self.split_by_column(self.header.index(header))

    def to_csv(self):
        """Convert table to csv."""
        def row_to_csv(row):
            """Convert row to csv."""
            return ','.join(row)
        return (row_to_csv(self.header) + '\n' +
                '\n'.join(row_to_csv(row) for row in self))

    def get_by_column(self, column, value):
        """Return first row in table with specific value."""
        for row in self:
            if row[column] == value:
                return row
