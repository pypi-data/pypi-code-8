"""
Convert a Python string to its native type.

The reason this module exists because there is a need to handle arguments with
the syntax `--opt KEY=VAL` where `KEY` will be used as a keyword argument
somewhere and `VAL` is expected to be a native Python type.

This module was built with click in mind, which is an excellent CLI framework.
See the examples on GitHub for more info.
    https://github.com/geowurster/str2type/tree/master/examples/

The following types are supported:

    - float
    - int
    - str
    - None
    - True
    - False
    - JSON

Example:

    >>> import str2type
    >>> result = str2type.str2type('1.23')
    >>> print(result)
    1.23
    >>> type(result)
    float
"""


import warnings

from .core import str2type
try:  # pragma no cover
    from .deprecated import click_callback_key_val_dict
except ImportError:  # pragma no cover
    warnings.warn(
        'Cannot import `str2type.click_callback_key_val_dict()` - click must be imported '
        'first.  This will be removed before v1.0 and has already been migrated to '
        '`str2type.ext.click_cb_val_dict()`', FutureWarning, stacklevel=2
    )
    click_callback_key_val_dict = None

try:  # pragma no cover
    from .deprecated import click_callback
except ImportError:  # pragma no cover
    warnings.warn(
        'Cannot import `str2type.click_callback()` - click must be imported first.  This '
        'be removed before v1.0 and has already been migrated to '
        '`str2type.ext.click_cb()`', FutureWarning, stacklevel=2
    )
    click_callback = None


__all__ = ['str2type', 'click_callback_key_val_dict', 'click_callback']


__version__ = "0.4.1"
__author__ = "Kevin Wurster"
__email__ = "wursterk@gmail.com"
__source__ = "https://github.com/geowurster/str2type"
__license__ = """
New BSD License

Copyright (c) 2014-2015, Kevin D. Wurster
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* The names of its contributors may not be used to endorse or promote products
  derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
