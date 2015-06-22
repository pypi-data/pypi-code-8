
#
# WebHeroes-Utils -- Web Heroes Inc. python utility module
#
# Copyright (c) 2015, Web Heroes Inc..
#
# WebHeroes-Utils is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.  See the LICENSE file at the top of the source tree.
#
# WebHeroes-Utils is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#

__author__                      = "Matthew Brisebois"
__email__                       = "matthew@webheroes.ca"
__copyright__                   = "Copyright (c) 2015 Web Heroes Inc."
__license__                     = "Dual License: GPLv3 (or later) and Commercial (see LICENSE)"

__all__				= ["handle", "shutdown"]

import signal

shutdown		= False

def term_signalled(*args):
    global shutdown
    shutdown		= True

default_handlers	= {
    signal.SIGTERM: term_signalled,
}

def handle(sig, callback=None):
    if not hasattr(signal, sig):
        return False
    sig			= getattr(signal, sig)
    if callback is None:
        if sig in default_handlers:
            signal.signal( sig, default_handlers[sig])
        else:
            return False
    else:
        signal.signal( sig, callback)
