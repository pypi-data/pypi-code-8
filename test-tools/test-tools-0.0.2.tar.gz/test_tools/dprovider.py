# -*- coding: utf-8 -*-
#
# Copyright 2015 Yuriy Gavenchuk aka murminathor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from functools import update_wrapper
from collections import Iterable


__author__ = 'y.gavenchuk aka murminathor'
__all__ = ['data_provider', ]


def _get_data_source(data_set_source):
    if callable(data_set_source):
        data_source = data_set_source()
    elif isinstance(data_set_source, Iterable):
        data_source = data_set_source
    else:
        raise TypeError(
            "The '{0}' is unsupported type of data set source!".format(
                type(data_set_source)
            )
        )

    if not data_source:
        raise ValueError("There's no data in current data set!")

    return data_source


def data_provider(data_set_source):
    """
        Data provider decorator, allows another callable to provide the data
        for the test. If data_set_source is empty or (if callable) return
        empty sequence will be raise ValueError exception

        :param collections.Iterable | callable data_set_source: data source

        :raises: TypeError|ValueError
    """

    def test_decorator(fn):
        # next if statement added 'cause MagicMock in python2 raises
        # AttributeError.
        # See https://code.google.com/p/mock/issues/detail?id=67
        if not hasattr(fn, '__name__'):
            setattr(fn, '__name__', str(fn))

        def repl(self, *args):
            # The setUp method has been called already.
            # And the tearDown cannot be called after last iteration
            # The next code solves this contradiction
            def _set_up():
                """
                Replace local setUp function to the original TestCase's
                instance
                """
                repl._setUp = self.setUp

            def _tear_down():
                """
                Replace local tearDown function to the original TestCase's
                instance
                """
                repl._tearDown = self.tearDown

            repl._setUp = _set_up
            repl._tearDown = _tear_down

            data_source = _get_data_source(data_set_source)
            step = 0
            for i in data_source:
                repl._tearDown()
                repl._setUp()

                try:
                    fn(self, *i)
                    step += 1
                except AssertionError:
                    msg_tpl = "Step #{step}. Assertion error caught with " \
                              "data set {data_set}"
                    print(msg_tpl.format(step=step, data_set=i))
                    raise

        return update_wrapper(repl, fn)
    return test_decorator
