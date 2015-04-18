import sys
from flattrclient.flattrs import Flattr
from pytest import raises


def test_init():
    x = Flattr(

        thing='fff_thing',
        owner='fff_owner',
        created_at='fff_created_at'	)

    assert x.thing == 'fff_thing'
    assert x.owner == 'fff_owner'
    assert x.created_at == 'fff_created_at'

def test_thing():
    x = Flattr()

    assert x.thing == None

    x._thing = 'fff_thing'
    assert x.thing == 'fff_thing'

    with raises(AttributeError):
        x.thing = 'fff'


def test_owner():
    x = Flattr()

    assert x.owner == None

    x._owner = 'fff_owner'
    assert x.owner == 'fff_owner'

    with raises(AttributeError):
        x.owner = 'fff'


def test_created_at():
    x = Flattr()

    assert x.created_at == None

    x._created_at = 'fff_created_at'
    assert x.created_at == 'fff_created_at'

    with raises(AttributeError):
        x.created_at = 'fff'

