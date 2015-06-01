#######################################################################
# Tests for managesieve3 module.
#
# Copyright 2015 True Blade Systems, Inc.
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
#
# Notes:
#  When moving to a newer version of unittest, check that the exceptions
# being caught have the expected text in them.
#
########################################################################

from managesieve3 import Managesieve

import sys
import copy
import unittest
import collections
import unicodedata

_PY2 = sys.version_info[0] == 2
_PY3 = sys.version_info[0] == 3

class TestManagesieve3(unittest.TestCase):
    pass

class TestAll(unittest.TestCase):
    def test_all(self):
        import managesieve3

        # check that __all__ in the module contains everything that should be
        #  public, and only those symbols
        all = set(managesieve3.__all__)

        # check that things in __all__ only appear once
        self.assertEqual(len(all), len(managesieve3.__all__),
                         'some symbols appear more than once in __all__')

        # get the list of public symbols
        found = set(name for name in dir(managesieve3) if not name.startswith('_'))

        # make sure it matches __all__
        self.assertEqual(all, found)



unittest.main()
