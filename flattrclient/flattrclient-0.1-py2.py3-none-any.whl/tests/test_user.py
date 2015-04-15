import sys
from flattrclient.user import User
from pytest import raises

# all fields of User are ro
def test_resource():
    u = User()

    assert u.resource == None

    u._resource = 'resource'
    assert u.resource == 'resource'

    # this is an read-only field
    with raises(AttributeError):
        u.resource = 'resource'

def test_link():
    u = User()

    assert u.link == None

    u._link = 'link'
    assert u.link == 'link'

    # this is an read-only field
    with raises(AttributeError):
        u.link = 'link'

def test_username():
    u = User()

    assert u.username == None

    u._username = 'username'
    assert u.username == 'username'

    # this is an read-only field
    with raises(AttributeError):
        u.username = 'username'

def test_url():
    u = User()

    assert u.url == None

    u._url = 'url'
    assert u.url == 'url'

    # this is an read-only field
    with raises(AttributeError):
        u.url = 'url'

def test_firstname():
    u = User()

    assert u.firstname == None

    u._firstname = 'firstname'
    assert u.firstname == 'firstname'

    # this is an read-only field
    with raises(AttributeError):
        u.firstname = 'firstname'

def test_lastname():
    u = User()

    assert u.lastname == None

    u._lastname = 'lastname'
    assert u.lastname == 'lastname'

    # this is an read-only field
    with raises(AttributeError):
        u.lastname = 'lastname'

def test_avatar():
    u = User()

    assert u.avatar == None

    u._avatar = 'avatar'
    assert u.avatar == 'avatar'

    # this is an read-only field
    with raises(AttributeError):
        u.avatar = 'avatar'

def test_about():
    u = User()

    assert u.about == None

    u._about = 'about'
    assert u.about == 'about'

    # this is an read-only field
    with raises(AttributeError):
        u.about = 'about'

def test_city():
    u = User()

    assert u.city == None

    u._city = 'city'
    assert u.city == 'city'

    # this is an read-only field
    with raises(AttributeError):
        u.city = 'city'

def test_country():
    u = User()

    assert u.country == None

    u._country = 'country'
    assert u.country == 'country'

    # this is an read-only field
    with raises(AttributeError):
        u.country = 'country'

def test_email():
    u = User()

    assert u.email == None

    u._email = 'email'
    assert u.email == 'email'

    # this is an read-only field
    with raises(AttributeError):
        u.email = 'email'

def test_registered_at():
    u = User()

    assert u.registered_at == None

    u._registered_at = 'registered_at'
    assert u.registered_at == 'registered_at'

    # this is an read-only field
    with raises(AttributeError):
        u.registered_at = 'registered_at'

def test_init():
    u = User(
        resource='f1_resource',
        link='f2_link',
        username='f3_username',
        url='f4_url',
        firstname='f5_firstname',
        lastname='f6_lastname',
        avatar='f7_avatar',
        about='f8_about',
        city='f9_city',
        country='f10_country',
        email='f11_email',
        registered_at='f12_registered_at'
        )

    assert u.resource == 'f1_resource'
    assert u.link == 'f2_link'
    assert u.username == 'f3_username'
    assert u.url == 'f4_url'
    assert u.firstname == 'f5_firstname'
    assert u.lastname == 'f6_lastname'
    assert u.avatar == 'f7_avatar'
    assert u.about == 'f8_about'
    assert u.city == 'f9_city'
    assert u.country == 'f10_country'
    assert u.email == 'f11_email'
    assert u.registered_at == 'f12_registered_at'
