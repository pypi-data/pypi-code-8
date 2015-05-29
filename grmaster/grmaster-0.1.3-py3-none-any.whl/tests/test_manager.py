# -*- coding: utf-8 -*-

"""Tests for `grmaster.Manager`."""

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
from grmaster.manager import Manager, get_item, set_item

def test_get_item():
    """Full test."""
    arr = [[1, 2], [3, 4]]
    assert get_item(arr, [0, 0]) == 1
    assert get_item(arr, [0, 1]) == 2
    assert get_item(arr, [1, 0]) == 3
    assert get_item(arr, [1, 1]) == 4
    assert get_item(arr, [0]) == [1, 2]
    assert get_item(arr, [1]) == [3, 4]

def test_set_item():
    """Small test."""
    arr = [[1, 2], [3, 4]]
    set_item(arr, [0, 0], 5)
    assert arr == [[5, 2], [3, 4]]
    set_item(arr, [0, 1], 5)
    assert arr == [[5, 5], [3, 4]]
    set_item(arr, [1, 0], 5)
    assert arr == [[5, 5], [5, 4]]
    set_item(arr, [1, 1], 5)
    assert arr == [[5, 5], [5, 5]]

class TestManager:

    """Tests for grmaster.Manager."""

    manager = None
    student = None

    def setup(self):
        """Just setup manager."""
        with data.openfile('students.csv') as student_file:
            self.manager = Manager(student_file)
        assert isinstance(self.manager, Manager)
        self.student = self.manager.students[0]

    def test_manager_can_study(self):
        """Everybody can study everywhere."""
        assert all(self.manager.can_study(self.student, group)
                   for group in self.manager.group_ids)

    def test_manager_assign_student(self):
        """Constant method."""
        self.manager.assign_student(self.student, [0, 0])
        assert self.manager.is_assigned(self.student)
        assert self.manager.result_groups[0] == [0, 0]

    def test_manager_is_assigned(self):
        """After assignation."""
        assert not self.manager.is_assigned(self.student)
        self.manager.assign_student(self.student, [0, 0])
        assert self.manager.is_assigned(self.student)

    def test_manager_assign_all(self):
        """We can assign everyone."""
        self.manager.assign_all()
        for student in self.manager.students:
            assert self.manager.is_assigned(student)
