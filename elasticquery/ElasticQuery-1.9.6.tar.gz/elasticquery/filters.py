FILTERS = (
)


class MetaFilter(type):
    def __getattr__(self, name):
        pass

class Filter(object):
    __metaclass__ = MetaFilter
