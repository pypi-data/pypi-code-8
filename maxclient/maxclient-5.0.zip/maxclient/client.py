from hashlib import sha1
import requests
import json
from resources import RESOURCES as ROUTES
import getpass

DEFAULT_MAX_SERVER = 'http://localhost:8081'
DEFAULT_OAUTH_SERVER = 'https://oauth.upcnet.es'
DEFAULT_HUB_SERVER = 'https://hub.ulearn.upcnet.es'
DEFAULT_SCOPE = 'widgetcli'
DEFAULT_GRANT_TYPE = 'password'
DEFAULT_CLIENT_ID = 'MAX'


def get_max_info(max_url):
    try:
        response = requests.get('{}/info'.format(max_url), verify=False)
    except requests.exceptions.ConnectionError:
        raise RequestError(0, "Server {} did not respond. Is this a valid max url?".format(max_url))

    if response.status_code == 502:
        raise RequestError(502, "Server {} responded with 502. Is max running?".format(max_url))
    if response.status_code == 500:
        raise RequestError(500, "Server {} failed with 500 Internal Error".format(max_url))

    elif response.status_code == 200:
        return response.json()


def get_hub_info(hub_url):
    """
        Returns domains list and information from the given hub
    """
    try:
        response = requests.get('{}/info'.format(hub_url), verify=False)
    except requests.exceptions.ConnectionError:
        raise RequestError(0, "Server {} did not respond. Is this a valid hub url?".format(hub_url))

    if response.status_code == 502:
        raise RequestError(502, "Server {} responded with 502. Is hub running?".format(hub_url))
    if response.status_code == 500:
        raise RequestError(500, "Server {} failed with 500 Internal Error".format(hub_url))
    elif response.status_code == 200:
        hub_info = response.json()
        return hub_info

    return {}


def get_max_url_from_hub_domain(hub_url, domain):
    """
        Determines the max server corresponding to the given domain
        based on the information of the given hub
    """
    hub_info = get_hub_info(hub_url)
    default_maxserver = hub_info.get('default_maxserver_url', None)

    # If domain is defined, get the maxserver url
    if domain in hub_info.get('domains', {}):
        return hub_info['domains'][domain]['max_server_url']

    # If domain is not defined and we have a default
    elif default_maxserver:
        return '{}/{}'.format(default_maxserver, domain)

    # We have neither of domain or default defined
    else:
        raise Exception("There's no domain {} on {}".format(domain, hub_url))


class RequestError(Exception):
    """
    """
    def __init__(self, code, *args, **kwargs):
        super(RequestError, self).__init__(*args, **kwargs)
        self.code = code

BAD_PWD_MSG = """
Bad username or password.
   Oauth server = {}
   Max Server = {}"""


class BadUsernameOrPasswordError(Exception):
    def __init__(self, oauthserver, maxserver, username, password, *args, **kwargs):
        self.username = username
        self.password = password

        super(BadUsernameOrPasswordError, self).__init__(
            BAD_PWD_MSG.format(oauthserver, maxserver),
            *args,
            **kwargs
        )


class BaseClient(object):
    def __init__(self,
                 url=DEFAULT_MAX_SERVER,
                 oauth_server=None,
                 actor=None,
                 auth_method='oauth2',
                 expand_underscores=True,
                 scope=DEFAULT_SCOPE,
                 grant_type=DEFAULT_GRANT_TYPE,
                 client_id=DEFAULT_CLIENT_ID,
                 **kwargs):
        """
        """
        # Strip ending slashes, as all routes begin with a slash
        self.expand_underscores = expand_underscores
        self.url = url.rstrip('/')
        self.__oauth_server__ = oauth_server
        self.setActor(actor)
        self.auth_method = auth_method
        self.scope = scope
        self.grant_type = grant_type
        self.client_id = client_id
        self.metadata = {}
        self.__server_info__ = None

    @classmethod
    def from_hub_domain(cls, domain, hub=DEFAULT_HUB_SERVER, *args, **kwargs):
        max_server_url = get_max_url_from_hub_domain(hub, domain)
        # We have a max url, let's check if its good
        try:
            client = cls(max_server_url, *args, **kwargs)
        except RequestError as exc:
            if exc.code == 0:
                raise Exception("No maxserver found on {}".format(max_server_url))
            else:
                raise exc

        return client

    @property
    def oauth_server(self):
        if self.__oauth_server__ is None:
            self.__oauth_server__ = self.server_info['max.oauth_server']
        return self.__oauth_server__.rstrip('/')

    @property
    def server_info(self):
        if self.__server_info__ is None:
            self.__server_info__ = get_max_info(self.url)
        return self.__server_info__

    def login(self, username=None, password=None):
        if username is None:
            username = raw_input("Username: ")
        if password is None:
            message = 'Password for {}: '.format(username)
            password = getpass.getpass(message)

        self.setActor(username)
        return self.getToken(username, password)

    def getToken(self, username, password):
        # Set password to None if evaluates to False
        password = password if password else None

        payload = {"grant_type": self.grant_type,
                   "client_id": self.client_id,
                   "scope": self.scope,
                   "username": username,
                   "password": password
                   }

        req = requests.post('{0}/token'.format(self.oauth_server), data=payload, verify=False)

        response = json.loads(req.text)
        if req.status_code == 200:
            token = response.get("access_token", None)
            if token:
                self.setToken(token)
            elif response.get("oauth_token", None):
            # Fallback to legacy oauth server
                self.setToken(response.get("oauth_token"))
            else:
                raise AttributeError('No token found in response')
            return self.token
        else:
            raise BadUsernameOrPasswordError(
                oauthserver=self.oauth_server,
                maxserver=self.url,
                username=username,
                password=password
            )

    def getActor(self):
        return self.actor.get('username', '')

    def setActor(self, actor, type='person'):
        self.actor = actor and dict(objectType='person', username=actor) or None

    def setToken(self, oauth2_token):
        """
        """
        self.token = oauth2_token

    def setBasicAuth(self, username, password):
        """
        """
        self.ba_username = username
        self.ba_password = password

    def OAuth2AuthHeaders(self):
        """
        """
        headers = {
            'X-Oauth-Token': str(self.token),
            'X-Oauth-Username': str(self.actor['username']),
            'X-Oauth-Scope': str(self.scope),
        }
        return headers

    def BasicAuthHeaders(self):
        """
        """
        auth = (self.ba_username, self.ba_password)
        return auth


class MaxClient(BaseClient):

    def HEAD(self, route, qs=''):
        """
        """
        headers = {}
        resource_uri = '%s%s' % (self.url, route)
        if qs:
            resource_uri = '%s?%s' % (resource_uri, qs)
        if self.auth_method == 'oauth2':
            headers.update(self.OAuth2AuthHeaders())
            req = requests.head(resource_uri, headers=headers, verify=False)
        elif self.auth_method == 'basic':
            req = requests.head(resource_uri, auth=self.BasicAuthHeaders(), verify=False)
        else:
            raise

        isOk = req.status_code == 200
        if isOk:
            response = int(req.headers.get('X-totalItems', '0'))
        else:
            print req.status_code
            response = ''
        return (isOk, req.status_code, response)

    def GET(self, route, qs=''):
        """
        """
        headers = {}
        resource_uri = '%s%s' % (self.url, route)
        if qs:
            resource_uri = '%s?%s' % (resource_uri, qs)
        if self.auth_method == 'oauth2':
            headers.update(self.OAuth2AuthHeaders())
            req = requests.get(resource_uri, headers=headers, verify=False)
        elif self.auth_method == 'basic':
            req = requests.get(resource_uri, auth=self.BasicAuthHeaders(), verify=False)
        else:
            raise

        isOk = req.status_code == 200
        isJson = 'application/json' in req.headers.get('content-type', '')
        if isOk:
            response = json.loads(req.content) if isJson else None
        else:
            print 'GET {} - {} - {}'.format(req.status_code, req.content, route)
            response = ''
        return (isOk, req.status_code, response)

    def POST(self, route, query={}, upload_file=None):
        """
        """
        headers = {}
        resource_uri = '%s%s' % (self.url, route)
        json_query = json.dumps(query)

        if upload_file:
            headers.update(self.OAuth2AuthHeaders())
            files = {'file': ('avatar.png', upload_file)}
            req = requests.post(resource_uri, headers=headers, files=files, verify=False)
        else:
            if self.auth_method == 'oauth2':
                headers.update(self.OAuth2AuthHeaders())
                headers.update({'content-type': 'application/json'})
                req = requests.post(resource_uri, data=json_query, headers=headers, verify=False)
            elif self.auth_method == 'basic':
                req = requests.post(resource_uri, data=json_query, auth=self.BasicAuthHeaders(), verify=False)
            else:
                raise

        isOk = req.status_code in [200, 201] and req.status_code or False
        isJson = 'application/json' in req.headers.get('content-type', '')
        if isOk:
            response = json.loads(req.content) if isJson else None
        else:
            print 'POST {} - {} - {}'.format(req.status_code, req.content, route)
            response = req.content

        return (isOk, req.status_code, response)

    def PUT(self, route, query={}):
        """
        """
        headers = {}
        resource_uri = '%s%s' % (self.url, route)
        json_query = json.dumps(query)

        if self.auth_method == 'oauth2':
            headers.update(self.OAuth2AuthHeaders())
            req = requests.put(resource_uri, data=json_query, headers=headers, verify=False)
        elif self.auth_method == 'basic':
            req = requests.put(resource_uri, data=json_query, auth=self.BasicAuthHeaders(), verify=False)
        else:
            raise

        isOk = req.status_code in [200, 201] and req.status_code or False
        isJson = 'application/json' in req.headers.get('content-type', '')
        if isOk:
            response = json.loads(req.content) if isJson else None
        else:
            print 'PUT {} - {} - {}'.format(req.status_code, req.content, route)
            response = ''

        return (isOk, req.status_code, response)

    def DELETE(self, route, query={}):
        """
        """
        headers = {}
        resource_uri = '%s%s' % (self.url, route)
        json_query = json.dumps(query)

        if self.auth_method == 'oauth2':
            headers.update(self.OAuth2AuthHeaders())
            headers.update({'content-type': 'application/json'})
            req = requests.delete(resource_uri, data=json_query, headers=headers, verify=False)
        elif self.auth_method == 'basic':
            req = requests.delete(resource_uri, data=json_query, auth=self.BasicAuthHeaders(), verify=False)
        else:
            raise

        isOk = req.status_code in [204] and req.status_code or False
        isJson = 'application/json' in req.headers.get('content-type', '')
        if isOk:
            response = json.loads(req.content) if isJson else None
        else:
            print 'DELETE {} - {} - {}'.format(req.status_code, req.content, route)
            response = req.content

        return (isOk, req.status_code, response)

    ###########################
    # USERS
    ###########################

    def getUser(self, username=None):
        """
        """
        route = ROUTES['user']['route']
        rest_params = dict(username=username is not None and username or self.actor['username'])

        (success, code, response) = self.GET(route.format(**rest_params))
        return response

    def addUser(self, username, **kwargs):
        """
        """
        route = ROUTES['user']['route']

        query = {}
        rest_params = dict(username=username)
        valid_properties = ['displayName']
        query = dict([(k, v) for k, v in kwargs.items() if k in valid_properties])

        return self.POST(route.format(**rest_params), query)

    def modifyUser(self, username, properties):
        """
        """
        route = ROUTES['user']['route']

        query = properties
        rest_params = dict(username=username)

        return self.PUT(route.format(**rest_params), query)

    def modifyContext(self, url, properties):
        """
        """
        route = ROUTES['context']['route']

        query = properties
        context_hash = sha1(url).hexdigest()
        rest_params = dict(hash=context_hash)

        return self.PUT(route.format(**rest_params), query)

    def add_tags_to_context(self, url, tags):
        """
        """
        route = ROUTES['context_tags']['route']

        query = tags
        context_hash = sha1(url).hexdigest()
        rest_params = dict(hash=context_hash)

        return self.PUT(route.format(**rest_params), query)

    def remove_tag_from_context(self, url, tag):
        """
        """
        route = ROUTES['context_tag']['route']

        query = {}
        context_hash = sha1(url).hexdigest()
        rest_params = dict(hash=context_hash, tag=tag)

        return self.DELETE(route.format(**rest_params), query)

    def postAvatar(self, username, image):
        """
        """
        route = ROUTES['avatar']['route']
        rest_params = dict(username=username)

        return self.POST(route.format(**rest_params), upload_file=image)

    ###########################
    # ACTIVITIES
    ###########################

    def addActivity(self, content, otype='note', contexts=[], generator=None, username=None):
        """
        """
        route = ROUTES['user_activities']['route']
        query = dict(object=dict(objectType=otype,
                                 content=content,
                                 ),
                     )
        if contexts:
            query['contexts'] = []
            for context in contexts:
                query['contexts'].append(dict(url=context, objectType='context'))

        if generator:
            query['generator'] = generator

        rest_params = dict(username=username is not None and username or self.actor['username'])

        (success, code, response) = self.POST(route.format(**rest_params), query)
        return (success, code, response)

    def add_activity_as_context(self, content, url, otype='note', generator=None):
        """
        """
        route = ROUTES['context_activities']['route']
        query = dict(object=dict(objectType=otype,
                                 content=content,
                                 ),
                     )

        if generator:
            query['generator'] = generator

        context_hash = sha1(url).hexdigest()
        rest_params = dict(hash=context_hash)

        (success, code, response) = self.POST(route.format(**rest_params), query)
        return (success, code, response)

    def getActivity(self, activity):
        """
        """
        route = ROUTES['activity']['route']
        rest_params = dict(activity=activity)
        (success, code, response) = self.GET(route.format(**rest_params))
        return response

    def getUserTimeline(self):
        """
        """
        route = ROUTES['timeline']['route']
        rest_params = dict(username=self.actor['username'])
        (success, code, response) = self.GET(route.format(**rest_params))
        return response

    def getContextActivities(self, context, count=False):
        """ Return the activities given a context
        """
        route = ROUTES['context_activities']['route']
        rest_params = dict(hash=context)

        params = {}
        if context:
            params['qs'] = 'context={}'.format(context)

        if count:
            (success, code, response) = self.HEAD(route.format(**rest_params), **params)
        else:
            (success, code, response) = self.GET(route.format(**rest_params), **params)
        return response

    def getUserActivities(self, context=None, count=False, username=None):
        """ Return all the user activities under a specific context or globally
            if not specified.

            It can be invoked as admin, if an username of the actor is supplied.
        """
        route = ROUTES['user_activities']['route']
        rest_params = dict(username=username if username is not None else self.actor['username'])

        params = {}
        if context:
            params['qs'] = 'context={}'.format(context)

        if count:
            (success, code, response) = self.HEAD(route.format(**rest_params), **params)
        else:
            (success, code, response) = self.GET(route.format(**rest_params), **params)
        return response

    def getTimelineLastAuthors(self, limit=None):
        """
        """
        route = ROUTES['timeline_authors']['route']
        rest_params = dict(username=self.actor['username'])

        params = {}
        if limit:
            params['qs'] = 'limit={}'.format(limit)

        (success, code, response) = self.GET(route.format(**rest_params), **params)
        return response

    def getContextLastAuthors(self, context, limit=None):
        """
        """
        route = ROUTES['context_activities_authors']['route']
        rest_params = dict(hash=context)

        params = {}
        if limit:
            params['qs'] = 'limit={}'.format(limit)

        (success, code, response) = self.GET(route.format(**rest_params), **params)
        return response

    def getAllActivities(self, count=False):
        """ Stats only endpoint, return the aggregation of all user activities """
        route = ROUTES['activities']['route']

        if count:
            (success, code, response) = self.HEAD(route)
        else:
            (success, code, response) = self.GET(route)
        return response

    def getAllComments(self, count=False):
        """ Stats only endpoint, return the aggregation of all user activities """
        route = ROUTES['comments']['route']

        if count:
            (success, code, response) = self.HEAD(route)
        else:
            (success, code, response) = self.GET(route)
        return response

    ###########################
    # COMMENTS
    ###########################

    def addComment(self, content, activity, otype='comment'):
        """
        """
        route = ROUTES['comments']['route']
        query = dict(actor=self.actor,
                     object=dict(objectType=otype,
                                 content=content,
                                 ),
                     )
        rest_params = dict(activity=activity)
        (success, code, response) = self.POST(route.format(**rest_params), query)
        return response

    def getComments(self, activity):
        """
        """
        route = ROUTES['comments']['route']
        rest_params = dict(activity=activity)
        (success, code, response) = self.GET(route.format(**rest_params))

    ###########################
    # SUBSCRIPTIONS & CONTEXTS
    ###########################

    def addContext(self, param_value, displayName, permissions=None, context_type='context', param_name='url'):
        """
        """
        route = ROUTES['contexts']['route']

        query = {param_name: param_value,
                 'objectType': context_type,
                 'displayName': displayName,
                 'permissions': permissions
                 }

        if permissions:
            query['permissions'].update(permissions)

        (success, code, response) = self.POST(route, query)
        return response

    def get_context(self, url):
        """
        """
        route = ROUTES['context']['route']

        context_hash = sha1(url).hexdigest()
        rest_params = dict(hash=context_hash)

        (success, code, response) = self.GET(route.format(**rest_params))
        return response

    def deleteContext(self, url):
        """
        """
        route = ROUTES['context']['route']

        context_hash = sha1(url).hexdigest()
        rest_params = dict(hash=context_hash)

        (success, code, response) = self.DELETE(route.format(**rest_params))
        return response

    def subscribe(self, url, otype='context', username=None):
        """
        """
        route = ROUTES['subscriptions']['route']

        query = dict(object=dict(objectType=otype,
                                 url=url,
                                 ),
                     )
        rest_params = dict(username=username is not None and username or self.actor['username'])

        (success, code, response) = self.POST(route.format(**rest_params), query)
        return response

    def unsubscribe(self, url, otype='context', username=None):
        """ Takes directly the url and calculate the hash
        """
        route = ROUTES['subscription']['route']
        context_hash = sha1(url).hexdigest()

        rest_params = dict(username=username if username is not None else self.actor['username'],
                           hash=context_hash)

        (success, code, response) = self.DELETE(route.format(**rest_params))
        return response

    def subscribed_to_context(self, url):
        """
        """
        route = ROUTES['context_subscriptions']['route']
        context_hash = sha1(url).hexdigest()

        rest_params = dict(hash=context_hash)

        (success, code, response) = self.GET(route.format(**rest_params))
        return response

    def subscribed(self):
        """
        """
        route = ROUTES['subscriptions']['route']

        rest_params = dict(username=self.actor['username'])

        (success, code, response) = self.GET(route.format(**rest_params))
        return response

    def grant_permission(self, url, username=None, permission='read'):
        """
        """
        route = ROUTES['context_user_permission']['route']
        context_hash = sha1(url).hexdigest()

        rest_params = dict(username=username is not None and username or self.actor['username'],
                           hash=context_hash,
                           permission=permission)

        (success, code, response) = self.PUT(route.format(**rest_params))
        return response

    def revoke_permission(self, url, username=None, permission='write'):
        """
        """
        route = ROUTES['context_user_permission']['route']
        context_hash = sha1(url).hexdigest()

        rest_params = dict(username=username is not None and username or self.actor['username'],
                           hash=context_hash,
                           permission=permission)

        (success, code, response) = self.DELETE(route.format(**rest_params))
        return response

    ###########################
    # Conversations
    ###########################

    def pushtokens_by_conversation(self, conversation_id):
        """
        """
        route = ROUTES['pushtokens']['route']

        rest_params = dict(id=conversation_id)

        (success, code, response) = self.GET(route.format(**rest_params))
        return (success, code, response)

    ###########################
    # Examples
    ###########################

    def examplePOSTCall(self, username):
        """
        """
        route = ROUTES['']['route']

        query = {}
        rest_params = dict(username=username)

        (success, code, response) = self.POST(route.format(**rest_params), query)
        return response

    def exampleGETCall(self, param1, param2):
        """
        """
        route = ROUTES['']['route']
        rest_params = dict(Param1=param1)
        (success, code, response) = self.GET(route.format(**rest_params))
        return response

    # def follow(self,username,oid,otype='person'):
    #     """
    #     """

    # def unfollow(self,username,oid,otype='person'):
    #     """
    #     """

    ###########################
    # ADMIN
    ###########################

    def getUsers(self):
        """
        """
        route = ROUTES['users']['route']
        (success, code, response) = self.GET(route)
        return response

    def getActivities(self):
        """
        """
        route = ROUTES['activities']['route']
        (success, code, response) = self.GET(route)
        return response

    def getContexts(self):
        """
        """
        route = ROUTES['contexts']['route']
        (success, code, response) = self.GET(route)
        return response

    def getSecurity(self):
        route = ROUTES['admin_security']['route']
        resource_uri = '%s%s' % (self.url, route)
        req = requests.get(resource_uri, verify=False)
        isOk = req.status_code == 200
        isJson = 'application/json' in req.headers.get('content-type', '')
        if isOk:
            response = isJson and json.loads(req.content) or None
        return response

    def grant_security_role(self, user, role):
        route = ROUTES['admin_security_role_user']['route']
        rest_params = dict(user=user, role=role)
        (success, code, response) = self.POST(route.format(**rest_params))
        return response

    def revoke_security_role(self, user, role):
        route = ROUTES['admin_security_role_user']['route']
        rest_params = dict(user=user, role=role)
        (success, code, response) = self.DELETE(route.format(**rest_params))
        return response
