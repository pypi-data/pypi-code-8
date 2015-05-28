# -*- coding: utf-8 -*-

"""Stream is a list of groups."""

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


class Stream(list):

    """Stream is a list of groups."""

    def __repr__(self):
        """Return repr(self)."""
        return 'Stream(' + super().__repr__() + ')'

    def __contains__(self, student):
        """Return student in self."""
        return any(student in group for group in self)

    def get_assigned(self):
        """Get set of all assigned students."""
        result = set()
        for group in self:
            result |= group
        return result

    def get_assigned_count(self):
        """Return count of assigned students."""
        return len(self.get_assigned())
