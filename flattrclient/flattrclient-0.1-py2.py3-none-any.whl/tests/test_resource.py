from flattrclient.resource import Resource

def test_resource():
    r = Resource(None)

    res = repr(r)

    assert res == '<flattrclient.resource.Resource at %s>' % id(r)
