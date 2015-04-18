# -*- coding: utf-8 -*-
import flattrclient.base
import sys

class Resource(flattrclient.base.BaseApi):
    def __repr_helper__(self):
        return 'at %s' % id(self)

    def __repr__(self):
        """ repr must return str, no matter if python2 or 3.
        So converting unicodes to str. """
        res = self.__repr_helper__()
        if sys.version_info.major < 3:
            if isinstance(res, unicode):
                res = res.encode('utf-8')
        return '<%s.%s %s>' % (self.__class__.__module__,
                               self.__class__.__name__,
                               res)
