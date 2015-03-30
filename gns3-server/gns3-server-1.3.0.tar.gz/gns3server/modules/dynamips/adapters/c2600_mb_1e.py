# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .adapter import Adapter


class C2600_MB_1E(Adapter):

    """
    Integrated 1 port Ethernet adapter for the c2600 platform.
    """

    def __init__(self):
        Adapter.__init__(self, interfaces=1, wics=3)

    def __str__(self):

        return "C2600-MB-1E"

    def removable(self):

        return False
