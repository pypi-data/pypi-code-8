# -*- coding: utf-8 -*-

"""Tests for `grmaster.rules`."""

#   group-master - tool for dividing students into groups
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

from grmaster import data
from grmaster.manager import Manager
from grmaster.rules import divide
from grmaster.rules import english_rule

STUDENTS_FILE = data.openfile('students.csv')

def test_divide():
    """Test internal function divide."""
    elems = set(range(10))
    division = divide(elems, 4)
    assert isinstance(division, list)
    assert len(division) == 4
    assert isinstance(division[0], set)
    assert isinstance(division[1], set)
    assert isinstance(division[2], set)
    assert isinstance(division[3], set)
    assert division[0] | division[1] | division[2] | division[3] == elems
    assert len(division[0]) == 3
    assert len(division[1]) == 3
    assert len(division[2]) == 2
    assert len(division[3]) == 2

class TestRules:

    """Test case for `grmaster.rules`."""

    manager = None

    def setup(self):
        """Init data from test set."""
        STUDENTS_FILE.seek(0)
        self.manager = Manager(STUDENTS_FILE)

    def test_rules_english_rule(self):
        """Test case for `english_rule`."""
        english_rule(self.manager)
        assert self.manager.get_assigned_count() == len(self.manager.students)

        english_index = self.manager.students.header.index('Английский')
        for stream in self.manager.streams:
            for group in stream:
                levels = len(set(student[english_index] for student in group))
                assert 1 <= levels <= 2
