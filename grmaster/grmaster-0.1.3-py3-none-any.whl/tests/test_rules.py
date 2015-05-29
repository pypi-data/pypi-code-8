# -*- coding: utf-8 -*-

"""Tests for `grmaster.rules`."""

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

from grmaster import data
from grmaster.manager import Manager
from grmaster.rules import divide, add_english

STUDENTS_FILE = data.openfile('students.csv')

def test_divide():
    """Test internal function divide."""
    assert divide(50, 4) == [13, 13, 12, 12]
    assert divide(5, 6) == [1, 1, 1, 1, 1, 0]

class TestEnglishRule:

    """Test case for `grmaster.rules`."""

    manager = None

    def setup(self):
        """Init data from test set."""
        STUDENTS_FILE.seek(0)
        self.manager = Manager(STUDENTS_FILE)
        assert len(self.manager.assign_chain) == 0
        assert len(self.manager.rule_chain) == 0
        add_english(self.manager)
        assert len(self.manager.rule_chain) == 1
        assert len(self.manager.assign_chain) == 1



    def test_english_rule_can_study(self):
        """Test that student can study in some groups. Not all."""
        student = self.manager.students[0]
        assert any(self.manager.can_study(student, group)
                   for group in self.manager.group_ids)
        assert not all(self.manager.can_study(student, group)
                       for group in self.manager.group_ids)

    def test_english_assign_student(self):
        """We can add student in some group."""
        student = self.manager.students[0]
        for group in self.manager.group_ids:
            if self.manager.can_study(student, group):
                assert self.manager.assign_student(student, group)
            else:
                assert not self.manager.assign_student(student, group)

    def test_english_assign_everybody(self):
        """We can add all students."""
        for student in self.manager.students:
            for group in self.manager.group_ids:
                if self.manager.can_study(student, group):
                    self.manager.assign_student(student, group)
                    break
        for student in self.manager.students:
            assert self.manager.is_assigned(student)
