''' Klarna API

utility functions
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

# python3k campatibility
from __future__ import print_function
import sys
if sys.version_info >= (3,):
    import xmlrpc.client as xmlrpc
    from html.entities import name2codepoint
    basestring = str
else:
    import htmlentitydefs
    import xmlrpclib as xmlrpc
    basestring = basestring

__all__ = ('xmlrpc', 'basestring', 'check_type', 'kstr', 'Tag')


def check_type(field, v, types, tag=None):
    ''' Raises TypeError unless v is a instance of any of the provided types '''

    if not isinstance(v, types):
        raise TypeError("%s not an %s (%s %r)" %
            (field, ' or '.join([t.__name__ for t in types]), type(v), v))

    if tag is not None:
        if isinstance(v, Tag) and not isinstance(v, tag):
            raise TypeError("Tagged value %r not of expected type %s (was %s)" %
                (v, tag, type(v)))

    return v


class Tag(str):
    ''' Used as base class for str subclasses used by Klarna API '''
    def __new__(cls, tostr, klarna=None):
        o = str.__new__(cls, tostr)
        o.klarna = klarna
        return o


if sys.version_info >= (3,):
    kstr = str
else:
    __sys_encoding = sys.getdefaultencoding()
    if __sys_encoding == 'ascii':
        # ascii is a mostly useless default, let's assume utf-8
        # as it's sane a superset of ascii
        __sys_encoding = 'utf-8'

    def kstr(s):
        if isinstance(s, str):
            s = s.decode(__sys_encoding)
        if isinstance(s, unicode):
            return s.encode('iso-8859-1')
        return str(s)
