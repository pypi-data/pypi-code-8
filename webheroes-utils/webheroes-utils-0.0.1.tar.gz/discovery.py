
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

__all__				= ["get_docker_ip"]

import os, netifaces

def get_docker_ip(dname=None):
    if dname is None:
        return netifaces.ifaddresses('eth0')[2][0]['addr']
    else:
        fname	= "/host/var/addr/{0}.ip".format(dname)
    if os.path.isfile(fname):
        with open(fname, "r") as f:
            return f.read().rstrip()
    else:
        raise Exception("No file exists at {0}".format(fname))
