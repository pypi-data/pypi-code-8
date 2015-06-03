''' Klarna API - checkout - checkouthtml

baseclass for checkout extensions
'''

# Copyright 2015 Klarna AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..error import KlarnaException


class CheckoutHTML(object):
    def get_session_id(self, eid):
        ''' Creates a session used for e.g client identification and fraud
            prevention.

            The returned string consist of 40 characters 0-9 computed as follows:
            * the first 30 is time padded with random numbers
            * the last 10 is the eid zero-padded
        '''

        import time
        import random

        eid = '%010d' % eid
        sid = str(time.time()).replace('.', '')
        # Get random int between minumum and maximum int represented
        # with remaining chars
        min = 10 ** (30 - len(sid) - 1)
        max = 10 ** (30 - len(sid)) - 1
        rand = str(random.randint(min, max))

        return '%s%s%s' % (sid, rand, eid)

    def to_html(self, uri):
        raise KlarnaException("to_html not implemented by CheckoutHTML subclass")

    def clear(self, uri):
        raise KlarnaException("clear not implemented by CheckoutHTML subclass")
