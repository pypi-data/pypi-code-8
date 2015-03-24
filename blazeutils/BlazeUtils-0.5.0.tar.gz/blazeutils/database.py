# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import warnings

warnings.warn('blazeutils.database is deprecated and will be removed in the future',
              DeprecationWarning,
              stacklevel=2)

# Pagination
from werkzeug import cached_property


# from Werkzeug Shorty example
class Pagination(object):

    def __init__(self, query, per_page, page, endpoint):
        self.query = query
        self.per_page = per_page
        self.page = page
        self.endpoint = endpoint

    @cached_property
    def count(self):
        return self.query.count()

    @cached_property
    def entries(self):
        return self.query.offset((self.page - 1) * self.per_page) \
                         .limit(self.per_page).all()

    has_previous = property(lambda x: x.page > 1)
    has_next = property(lambda x: x.page < x.pages)
    previous = property(lambda x: x.page - 1)
    next = property(lambda x: x.page + 1)
    pages = property(lambda x: max(0, x.count - 1) // x.per_page + 1)
