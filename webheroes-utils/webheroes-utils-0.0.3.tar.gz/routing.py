
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

__all__				= ["Routing"]

import re

from .		import logging

log		= logging.getLogger('routing')
log.setLevel(logging.ERROR)
    
class Routing(object):

    def __init__(self):
        self._paths	= {}
        self._default	= lambda **kw: None
        self.check_fn	= None

    def paths(self, prefix=None):
        paths		= self._paths.keys()
        if prefix is not None:
            paths	= [re.sub("^{0}".format(prefix), "", path) for path in paths]
        return paths

    def when(self, route, fn, **kw):
        route, segs	= self.prep_path(route)
        self._paths[route] = {
            "segments": segs,
            "callback": fn,
            "route": route,
            "kwargs": kw,
        }

    def otherwise(self, fn):
        self._default	= fn

    def check(self, fn):
        self.check_fn	= fn

    def prep_path(self, path):
        path		= path.strip('/')
        k		= '/%s' % (path,)
        return k, path.split('/')

    def run(self, path, **kw):
        path		= path.rstrip('/')
        route		= self.best_route(path)
        if route is None:
            response	= self._default(**kw)
        else:
            params	= self.get_params(path, route['route'])
            kw.update(route['kwargs'])
            kw.update(params)

            ok		= True
            msg		= None
            if self.check_fn is not None:
                ok,msg		= self.check_fn( route['route'], request=path, **kw )
            if ok is True:
                response	= route['callback'](**kw)
            else:
                response	= {
                    "error": "Permission Denied",
                    "message": msg,
                }
        return response

    def best_route(self, path):
        path, segs	= self.prep_path(path)
        best_match	= None
        log.debug("getting: %s", path)
        for p in self._paths.values():
            match_count		= 0
            for i, seg in enumerate( p['segments'] ):
                if seg.startswith(':'):
                    match_count = i+1
                elif i >= len(segs) or seg != segs[i]:
                    break
                else:
                    match_count = i+1
            
            log.debug("path: %s, match_count: %s", p['route'], match_count)
            if match_count == len(p['segments']) and (
                    best_match is None or best_match[0] < match_count ):
                best_match	= (match_count, p)
                log.debug("best_match: %s", best_match)
        return best_match[1] if best_match is not None else None

    def get_params(self, path, route):
        log.debug("using path: %s", path)
        n		= len( path.split('/') )
        route		= '/'.join( route.split('/')[:n] )
        log.debug("using route: %s", route)
        keys		= re.findall(':([a-zA-Z_]+)', route)
        match		= re.sub(':[a-zA-Z_]+', '([^/]*)', route)
        log.debug("match found: %s", match)
        values		= re.findall(match, path)
        log.debug("keys  found: %s", keys)
        log.debug("vals  found: %s", values)
        if len(values) and type( values[0] ) is tuple:
            values	= values[0]
        
        return dict( zip( keys, values ) )

