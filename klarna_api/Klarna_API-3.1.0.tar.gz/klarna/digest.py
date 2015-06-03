''' Klarna API - Digest

helper for digest calculation done by the core api
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

__all__ = ('get_digest',)

import sys
import hashlib
from base64 import b64encode


# Find a good hash algorithm
for m in ('sha512', 'sha256', 'md5'):
    try:
        default_method = getattr(hashlib, m)
        break
    except AttributeError:
        pass
else:
    raise Exception('Found no suitable hash algorithm')


# DEPRECATED
def md5b64(s):
    ''' Returns the md5 hash of s as a base64 encoded string (deprecated) '''
    return get_digest(s, hashlib.md5)


def get_digest(s, method=default_method):
    if sys.version_info >= (3,):
        s = s.encode('iso8859-1')
    else:
        if isinstance(s, unicode):
            s = s.encode('iso8859-1')
    return b64encode(method(s).digest()).decode('ascii')
