
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

__all__				= ["set", "parse"]

import Cookie
    
def set(key, value, host=None):
    sc				= Cookie.SimpleCookie()
    sc[key]			= value
    if host:
        sc[key]['domain']	= host
    sc[key]['path']		= "/"
    sc[key]['expires']	= -1 if value in [None, False, "", "__delete__"] else (60*60*24*365)
    return str(sc[key]).split(':', 1)[1].strip()

def parse(cookie_str):
    return {k:v.value for k,v in Cookie.BaseCookie(cookie_str).items()}
