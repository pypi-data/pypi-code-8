# -*- coding: utf-8 -*-

"""Tests for `grmaster.Manager`."""

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

STUDENTS_FILE = data.openfile('students.csv')

def test_manager_init():
    """Test if manager creates normally."""
    STUDENTS_FILE.seek(0)
    manager = Manager(STUDENTS_FILE)
    assert isinstance(manager, Manager)
    assert [len(stream) for stream in manager.streams] == [6, 6, 6]


class TestManager:

    """Tests for grmaster.Manager."""

    manager = None

    def setup(self):
        """Just setup manager."""
        STUDENTS_FILE.seek(0)
        self.manager = Manager(STUDENTS_FILE)
        self.manager.streams[1][3] |= {1, 2, 3}

    def test_manager_is_assigned(self):
        """Constant method."""
        assert self.manager.is_assigned(1)
        assert self.manager.is_assigned(2)
        assert self.manager.is_assigned(3)
        assert not self.manager.is_assigned(4)
        assert not self.manager.is_assigned(5)

    def test_manager_get_assigned(self):
        """Return set."""
        assert isinstance(self.manager.get_assigned(), set)
        assert self.manager.get_assigned() == {1, 2, 3}
        self.manager.streams[1][4] |= {1, 2, 4}
        assert self.manager.get_assigned() == {1, 2, 3, 4}

    def test_manager_get_assigned_count(self):
        """Return size of set."""
        assert isinstance(self.manager.get_assigned_count(), int)
        assert self.manager.get_assigned_count() == 3
        self.manager.streams[1][4] |= {1, 2, 4}
        assert self.manager.get_assigned_count() == 4
