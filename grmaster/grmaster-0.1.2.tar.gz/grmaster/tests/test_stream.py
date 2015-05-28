# -*- coding: utf-8 -*-

"""Tests for `grmaster.Stream`."""

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

from grmaster.stream import Stream


class TestStream:

    """Tests for grmaster.Stream."""

    stream = None

    def setup(self):
        """Just init."""
        self.stream = Stream(set() for i in range(3))
        self.stream[0] |= {1, 2, 3}
        self.stream[1] |= {4, 5, 6}

    def test_stream_repr(self):
        """repr(Stream()) == Stream([])."""
        stream_repr = repr(self.stream)
        assert stream_repr == 'Stream([{1, 2, 3}, {4, 5, 6}, set()])'

    def test_stream_get_assigned(self):
        """Result is set."""
        assert self.stream.get_assigned() == {1, 2, 3, 4, 5, 6}
        self.stream[2] |= {4, 5, 7}
        assert self.stream.get_assigned() == {1, 2, 3, 4, 5, 6, 7}

    def test_stream_get_assigned_count(self):
        """Result is size of set."""
        assert self.stream.get_assigned_count() == 6
        self.stream[2] |= {4, 5, 7}
        assert self.stream.get_assigned_count() == 7

    def test_stream_contains(self):
        """`a in stream` test."""
        assert 1 in self.stream
        assert 2 in self.stream
        assert 3 in self.stream
        assert 4 in self.stream
        assert 5 in self.stream
        assert 6 in self.stream
        assert 7 not in self.stream
        assert 8 not in self.stream
        assert 9 not in self.stream
        assert 10 not in self.stream
