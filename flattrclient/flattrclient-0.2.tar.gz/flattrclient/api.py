# -*- coding: utf-8 -*-
import six
import requests
import flattrclient
import flattrclient.user
import flattrclient.things
import flattrclient.flattrs
import flattrclient.subscriptions
import flattrclient.base
import flattrclient.search

def get(auth_token):
    """ Returns an `flattrclient.api.FlattrApi` object, initialized with a
    session object of `requests.session.Session`.
    """
    session = requests.Session()
    session.headers.update({'Accept': 'application/json',
        'Authorization': 'Bearer %s' % auth_token})
    return FlattrApi(session)

class ThingApi(flattrclient.base.BaseApi):

    _endpoint = 'rest/v2/things'

    def new(self, *args, **kwargs):
        """Returns new `flattrclient.things.Thing`, connected to the session.
        For parameters have a look at `flattrclient.things.Thing`."""
        return flattrclient.things.Thing(session=self._session, **kwargs)

    @flattrclient.result(flattrclient.things.Thing)
    @flattrclient.get('/')
    def get(self, *args):
        """Get one or more thing.
        Pass as much thing ids as parameter as you need to.
        Returns either one thing, or a generator of things.

        :param *args: Really. It will be ','.join(args)'ed."""
        return ','.join(args)

    @flattrclient.result(flattrclient.things.Thing)
    @flattrclient.get('/lookup')
    def lookup(self, url):
        """Check if a thing exists.
        Returns one thing.

        :param url: Lookup a thing for this url
        """
        return {'url': url}

    @flattrclient.result(flattrclient.search.SearchResult)
    @flattrclient.get('/search')
    def search(self, query=None, url=None, tags=None, language=None,
        category=None, user=None, sort=None, page=None, count=None, full=False):
        """Search a thing

        :param query: (Optional) - string Free text search string
        :param url: (Optional) - string Filter by url
        :param tags: (Optional) - string Filter by tags, see syntax below
        :param language: (Optional) - string Filter by language. If you wan't to search more than one language you can separate them with a , (comma).
        :param category: (Optional) - string Filter by category. If you wan't to search more than one category you can separate them with a , (comma).
        :param user: (Optional) - string Filter by username
        :param sort: (Optional) - string Sort by trend, flattrs (all time), flattrs_month, flattrs_week, flattrs_day or relevance (default)
        :param page: (Optional) - integer The result page to show
        :param count: (Optional) - integer Number of items per page
        :param full: ( Optional ) - Receive full user object instead of small
        """
        q = flattrclient._get_query_dict(query=query, url=url, tags=tags,
                language=language, category=category, user=user, sort=sort,
                page=page, count=count, full=full)
        return q

class UsersApi(flattrclient.base.BaseApi):

    _endpoint = 'rest/v2/users'

    def __call__(self, username):
        """Returns user object, only containing username.
        No api-call happens here.

        :param username: Make a `flattrclient.user.User` with this username."""
        return flattrclient.user.User(session=self._session, username=username)

    @flattrclient.result(flattrclient.user.User)
    @flattrclient.get('/')
    def get(self, username):
        """Get the flattr user.

        :param username: Get the user from flattr."""
        return username

class AuthenticatedApi(flattrclient.base.BaseApi):

    _endpoint = 'rest/v2/user'

    @flattrclient.result(flattrclient.flattrs.Flattr)
    @flattrclient.get('/flattrs')
    def get_flattrs(self, count=None, page=None, full=None):
        """ Get all flattrs all flattrs, the authenticated user did so far.
        http://developers.flattr.net/api/resources/flattrs/#list-the-authenticated-users-flattrs

        :param count: (Optional) - Count elements in a batch. Default 30.
        :param page: (Optional) - Get page X of the result set.
        :param full: (Optional) - Get the all owner fields.
        """
        return flattrclient._get_query_dict(count=count, page=page, full=full)

    @flattrclient.result(flattrclient.things.Thing)
    @flattrclient.get('/things')
    def get_things(self, count=None, page=None, full=None):
        """ Get all things of the authenticated user.
        http://developers.flattr.net/api/resources/things/#list-a-authenticated-users-things

        :param count: (Optional) - Count elements in a batch. Default 30.
        :param page: (Optional) - Get page X of the result set.
        :param full: (Optional) - Get the all owner fields.
        """
        return flattrclient._get_query_dict(count=count, page=page, full=full)

    @flattrclient.result(flattrclient.subscriptions.Subscription)
    @flattrclient.get('/subscriptions')
    def get_subscriptions(self):
        """ Get all subscriptions of the authenticated user.
        http://developers.flattr.net/api/resources/subscriptions/#list-subscriptions
        """
        return {}

    @flattrclient.just_json
    @flattrclient.get('/activities',
            additional_headers={'Accept': 'application/stream+json'})
    def get_activities(self, type=None):
        """ Get all activities os the authenticated user.
        http://developers.flattr.net/api/resources/activities/#list-a-authenticated-users-activities

        :param type: (Optional) - Can be set to incoming or outgoing, default: outgoing
        """
        return flattrclient._get_query_dict(type=type)

class FlattrApi(flattrclient.base.BaseApi):

    def __init__(self, session):
        """Set the session.
        Initializes sub apis.

        :param session: `requests.session.Session` to use.
        """
        super(FlattrApi, self).__init__(session)
        self.things = ThingApi(session)
        self.users = UsersApi(session)
        self.authenticated = AuthenticatedApi(session)
