from flattrclient import api
import flattrclient.base
import flattrclient.things
import flattrclient.flattrs
import flattrclient.subscriptions
import pytest
import requests

def test_get():
    x = api.get('FAKE_TOKEN')

    assert isinstance(x, api.FlattrApi)
    assert x._session.headers['Authorization'] == 'Bearer FAKE_TOKEN'

    assert x._session.headers['Accept'] == 'application/json'

def test_BaseApi():
    #with raises(TypeError):
    #    flattr_api = api.BaseApi('')

    session = requests.Session()
    flattr_api = flattrclient.base.BaseApi(session)

    assert flattr_api._session == session

    old_api_url = flattr_api._api_url
    flattr_api._api_url = None
    with pytest.raises(AssertionError):
        flattr_api._get_url()

    flattr_api._api_url = old_api_url
    with pytest.raises(AssertionError):
        flattr_api._get_url()

    flattr_api._endpoint = 'endpoint'
    res = flattr_api._get_url()
    assert res == 'https://api.flattr.com/endpoint'

    with pytest.raises(NotImplementedError):
        flattr_api.new()

def test_FlattrApi_new():
    session = requests.Session()
    flattr_api = api.ThingApi(session)

    assert flattr_api._session == session

    res = flattr_api.new(id=1, title=u'Hello World')
    assert isinstance(res, flattrclient.things.Thing)
    assert res._session == session
    assert res.id == 1
    assert res.title == 'Hello World'

def test_FlattrApi():
    session = requests.Session()
    flattr_api = api.FlattrApi(session)

    assert hasattr(flattr_api, 'things')
    assert hasattr(flattr_api, 'users')
    assert hasattr(flattr_api, 'authenticated')

    assert flattr_api.things._session == session
    assert flattr_api.users._session == session
    assert flattr_api.authenticated._session == session

class FakeResource(object):

    def __init__(self, url, params, status_code=200):
        self.params = params
        self.url = url
        # need this!! since magick is checking for 200
        self.status_code = status_code

class FakeThing(FakeResource):

    def json(self):
        return {'url': self.url,
                'link': self.params}

class FakeSubscription(FakeResource):

    def json(self):
        return {'created_at': self.url,
                'started_at': self.params}

class FakeFlattr(FakeResource):

    def json(self):
        return {'created_at': self.url,
                'owner': self.params}

class FakeSession(object):

    def __init__(self, ret_cls, status_code=200):
        self.status_code = status_code
        self.ret_cls = ret_cls
        self.headers = {'Accept': 'application/json'}

    def get(self, url, params, headers={}):
        return self.ret_cls(url, params)

@pytest.fixture
def fake_session_cls():
    return FakeSession

@pytest.fixture
def fake_thing_cls():
    return FakeThing

@pytest.fixture
def fake_subscription_cls():
    return FakeSubscription

@pytest.fixture
def fake_flattr_cls():
    return FakeFlattr

def test_authentivated_api_things(fake_session_cls, fake_thing_cls):
    flattr_api = api.AuthenticatedApi(session=fake_session_cls(fake_thing_cls))

    res = flattr_api.get_things()
    assert isinstance(res, flattrclient.things.Thing)

    assert res.url == u'https://api.flattr.com/rest/v2/user/things'
    assert res.link == {}

    res = flattr_api.get_things(count=30, page=1, full=True)

    assert res.link == {'count': 30,
                        'page': 1,
                        'full': True}

def test_authentivated_api_subscriptions(fake_session_cls, fake_subscription_cls):
    flattr_api = api.AuthenticatedApi(session=fake_session_cls(fake_subscription_cls))

    res = flattr_api.get_subscriptions()
    assert isinstance(res, flattrclient.subscriptions.Subscription)

    assert res.created_at == 'https://api.flattr.com/rest/v2/user/subscriptions'
    assert res.started_at == {}

    with pytest.raises(TypeError):
        flattr_api.get_subscriptions(True)

def test_authentivated_api_flattrs(fake_session_cls, fake_flattr_cls):
    flattr_api = api.AuthenticatedApi(session=fake_session_cls(fake_flattr_cls))

    res = flattr_api.get_flattrs()
    assert isinstance(res, flattrclient.flattrs.Flattr)

    assert res.created_at == 'https://api.flattr.com/rest/v2/user/flattrs'
    assert res.owner == {}

    res = flattr_api.get_flattrs(count=30, page=1, full=True)

    assert res.owner == {'count': 30,
                         'page': 1,
                         'full': True}

def test_authentivated_api_activities(fake_session_cls, fake_thing_cls):
    flattr_api = api.AuthenticatedApi(session=fake_session_cls(fake_thing_cls))

    res = flattr_api.get_activities()
    assert isinstance(res, dict)

    assert res['url'] == 'https://api.flattr.com/rest/v2/user/activities'
    assert res['link'] == {}

    res = flattr_api.get_activities(type='incoming')

    assert res['link'] == {'type': 'incoming'}
