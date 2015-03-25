# Copyright (C) 2015 Barry A. Warsaw
#
# This file is part of world
#
# world is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, version 3 of the License.
#
# world is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# world.  If not, see <http://www.gnu.org/licenses/>.

"""Test main."""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'TestMain',
    ]


import sys
import unittest
import worldlib

from io import StringIO
from functools import partial
from worldlib.__main__ import main

try:
    # Python 3
    from unittest.mock import patch
except ImportError:
    # Python 2
    from mock import patch
try:
    # Python 3
    from contextlib import ExitStack
except ImportError:
    # Python 2
    from contextlib2 import ExitStack


def argv(*args):
    args = list(args)
    args.insert(0, 'argv0')
    return patch('worldlib.__main__.sys.argv', args)


class TestMain(unittest.TestCase):
    """Test the command line."""

    def setUp(self):
        super(TestMain, self).setUp()
        self._resources = ExitStack()
        self._stdout = StringIO()
        self._stderr = StringIO()
        # Patch argparse's stderr to capture its error messages.
        self._resources.enter_context(
            patch('argparse._sys.stderr', self._stderr))
        # Patch sys.stdout.write() since that's how argparse's version action
        # works.
        self._resources.enter_context(
            patch('argparse._sys.stdout', self._stdout))
        # Capture print output.
        try:
            # Python 3
            self._resources.enter_context(
                patch('builtins.print', partial(print, file=self._stdout)))
        except ImportError:
            # Python 2
            self._resources.enter_context(
                patch('__builtin__.print', partial(print, file=self._stdout)))

    def tearDown(self):
        self._resources.close()
        super(TestMain, self).tearDown()

    def _output(self, which=None):
        # Return stdout/stderr, stripped of its trailing newline.
        if which is None:
            which = self._stdout
        output = which.getvalue()
        self.assertEqual(output[-1], '\n')
        return output[:-1]

    def test_version(self):
        self._resources.enter_context(argv('--version'))
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        # In Python 2, the version string gets written to stderr; in Python 3
        # it gets written to stdout.
        if sys.version_info < (3,):
            stream = self._stderr
        else:
            stream = self._stdout
        self.assertEqual(self._output(stream),
                         'world {}'.format(worldlib.__version__))

    def test_main(self):
        self._resources.enter_context(argv('de'))
        # We also have to capture stderr.
        main()
        self.assertEqual(self._output(), 'de originates from GERMANY')

    def test_main_unknown_code(self):
        self._resources.enter_context(argv('xx'))
        main()
        self.assertEqual(self._output(), 'Where in the world is xx?')

    def test_reverse(self):
        self._resources.enter_context(argv('-r', 'Germany'))
        main()
        self.assertMultiLineEqual(self._stdout.getvalue(), """\
Matches for "Germany":
  de: GERMANY
""")

    def test_multiple_reverse_matches(self):
        self._resources.enter_context(argv('-r', 'united'))
        main()
        self.assertMultiLineEqual(self._stdout.getvalue(), """\
Matches for "united":
  ae: UNITED ARAB EMIRATES
  gb: UNITED KINGDOM
  tz: TANZANIA, UNITED REPUBLIC OF
  uk: United Kingdom (common practice)
  um: UNITED STATES MINOR OUTLYING ISLANDS
  us: UNITED STATES
""")

    def test_no_reverse_match(self):
        self._resources.enter_context(argv('-r', 'freedonia'))
        main()
        self.assertEqual(self._output(), 'Where in the world is freedonia?')

    def test_multiple_reverse_searches(self):
        self._resources.enter_context(argv('-r', 'canada', 'mexico'))
        main()
        self.assertMultiLineEqual(self._stdout.getvalue(), """\
Matches for "canada":
  ca: CANADA

Matches for "mexico":
  mx: MEXICO
""")

    def test_all(self):
        self._resources.enter_context(argv('--all'))
        main()
        # Rather than test the entire output, just test the first and last.
        output = self._stdout.getvalue().splitlines()
        self.assertEqual(output[1].strip(), 'ad: ANDORRA')
        self.assertEqual(output[-1].strip(), 'xxx   : adult entertainment')

    def test_refresh(self):
        # ISO has pulled the free version of the country codes.
        self._resources.enter_context(argv('--refresh'))
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
