from .exception import NoQuery
from .util import build_field_structure, build_keyword_structure, build_list_structure


# (args->kwargs, kwargs)
# becomes: {field={args->kwargs + kwargs} + extra kwargs}
FIELD_QUERIES = {
    'term': (('value',), ('boost',)),
    'terms': (({'value': []},), ('boost',)),
    'match': (('query',), None),
    'range': (None, ('gte', 'gt', 'lte', 'lt',))
}

# (args->kwargs, kwargs)
# becomes: {args->kwargs + kwargs + extra kwargs}
KEYWORD_QUERIES = {
    'nested': (('path',), ({'query': '_query'},)),
    'query_string': (('query',), ({'fields': []},)),
    'missing': (('field'), None),
    'multi_match': (({'fields': []}, 'query'), None),
    'query': (({'query': '_query'}), None),
    'bool': (None, ({('must', 'must_not', 'should'): ['_query']},)),
    'more_like_this': (None, ({'fields': []},)),
    'filtered': (None, ({'query': '_query', 'filter': '_filter'}))
}

# (list-type)
# becomes: []
LIST_QUERIES = {
    'or_': '_filter'
}

class MetaQuery(type):
    def __getattr__(cls, name):
        if name in FIELD_QUERIES:
            structure = build_field_structure()
        elif name in KEYWORD_QUERIES:
            structure = build_keyword_structure()
        elif name in LIST_QUERIES:
            structure = build_list_structure()
        else:
            raise NoQuery()

        return structure


class Query(object):
    __metaclass__ = MetaQuery

    structure = None


print Query.term('field', 'value')
