import types
import pytest
from flattrclient.search import SearchResult

def test_search():
    res = SearchResult(total_items=100, items=30, page=1,
            things=[{'id': 1, 'title': u'Hello'}], ignore='me')

    assert res.total_items == 100
    assert res.items == 30
    assert res.page == 1
    assert isinstance(res.things, types.GeneratorType)
    with pytest.raises(AttributeError):
        res._ignore

    things = list(res.things)
    assert len(things) == 1

    assert things[0].id == 1
    assert things[0].title == 'Hello'
