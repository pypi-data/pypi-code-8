# This file is part of the Ubuntu Continuous Integration test tools
#
# Copyright 2015 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
import contextlib
import unittest
import sys


@contextlib.contextmanager
def catching_errors(test, result):
    """Wrap test execution catching exceptions.

    KeyboardInterrupt is re-raised, other exceptions are sent to 'result' as
    errors.

    :note: This looks like a convoluted way to call result.addError() (and it
        is) but it neatly implements the use case.
    """
    try:
        yield
    except KeyboardInterrupt:
        raise
    except:
        result.addError(test, sys.exc_info())
    return


class TestSuite(unittest.TestSuite):
    """A test suite providing setUp/addCleanup.

    ``setUp`` is called before the tests are run. If it fails, tests are not
    run. Added cleanups are always called whether or not a test or setUp
    failed.
    """

    # We fake the TestCase API (or mock the implementation details that
    # leak). It's a cheap price to be able to re-use result.addError() and all
    # good bits that comes with it.
    failureException = AssertionError

    def __init__(self, *args, **kwargs):
        super(TestSuite, self).__init__(*args, **kwargs)
        self._cleanups = []

    def id(self):
        cls = self.__class__
        # We need a unique name in case the same suite class is used several
        # times hence the id().
        return '{}.{}({:x})'.format(cls.__module__, cls.__name__, id(self))

    def run(self, result, debug=False):
        setup_done = False
        with catching_errors(self, result):
            self.setUp()
            setup_done = True
        try:
            if setup_done:
                super(TestSuite, self).run(result, debug)
        finally:
            while self._cleanups:
                cleanup, args, kwargs = self._cleanups.pop()
                with catching_errors(self, result):
                    cleanup(*args, **kwargs)

    def setUp(self):
        """Setup the test suite fixture before running it."""
        pass

    def addCleanup(self, function, *args, **kwargs):
        """Add a cleanup function to be called after running.

        Functions added with addCleanup will be called in reverse order of
        adding after running the tests, or after setUp if setUp raises an
        exception.

        If a function added with addCleanup raises an exception, the error will
        be recorded as a test suite error, and the next cleanup will then be
        run.

        Cleanup functions are always called before a test suite finishes
        running, even if setUp is aborted by an exception.
        """
        self._cleanups.append((function, args, kwargs))

    def doCleanups(self, result):
        """Execute all cleanup functions."""
        ok = True
        while self._cleanups:
            function, args, kwargs = self._cleanups.pop(-1)
            try:
                function(*args, **kwargs)
            except KeyboardInterrupt:
                raise
            except:
                ok = False
                result.addError(self, sys.exc_info())
        return ok
