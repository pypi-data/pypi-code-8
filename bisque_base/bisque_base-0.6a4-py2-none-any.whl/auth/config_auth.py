#
import logging
from zope.interface import implementer
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated
#from bq.auth.mex_authorization import MexAuthAuthenticationPolicy
#from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authentication import SessionAuthenticationPolicy

#from pyramid.authentication import Allow
#from pyramid.authentication import Authenticated
#from pyramid.authentication import Everyone
from pyramid.authentication import IAuthenticationPolicy
from pyramid.authentication import CallbackAuthenticationPolicy

from pyramid_authstack import AuthenticationStackPolicy


log = logging.getLogger ('bq.auth')

#################
#
class BisqueRoot(object):
    """Bisque root factory object for traversal

    This object is used current to define broad classes of permissions instead of object level acls
    """
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, Authenticated, 'edit'),
               (Allow, 'auth:who2', 'edit'),
               (Allow, 'auth:saved', 'edit'),
               (Allow, 'auth:session', 'edit'),
               (Allow, 'auth:mex', 'edit')
               ]


    def __init__(self, request):
        pass


@implementer(IAuthenticationPolicy)
class BisqueSavePolicy(CallbackAuthenticationPolicy):
    def __init__(self, callback=None):
        self.callback = callback

    def unauthenticated_userid(self, request):
        user_id = getattr(request,  'user_id', None)
        log.debug ("ID = %s", user_id)
        return user_id

    def effective_principals(self, request):
        return getattr(request,  'user_id', None)

    def remember(self, request, principal, **kw):
        request.user_id = principal
        return []

    def forget(self, request):
        request.user_id = None
        return []

def config_auth(config):
    def verify_user (identity, request):
        log.info ("USER %s", identity)
        return [ ('admin', )]

    settings = config.get_settings ()
    authorizations = settings.get ('bisque.authorization')
    authorizations = authorizations and [ x.strip() for x in authorizations.split(',')] or []
    # Create global policy
    stack_policy = AuthenticationStackPolicy()
    if 'mex' in authorizations:
        from .mex_authorization import MexAuthAuthenticationPolicy
        stack_policy.add_policy('mex', MexAuthAuthenticationPolicy())
    else:
        from pyramid_who.whov2 import WhoV2AuthenticationPolicy
       #authtk_policy = AuthTktAuthenticationPolicy('sosecret', callback=verify_user, hashalg='sha512')
       #stack_policy.add_policy('authtk', authtk_policy)

        session_policy = SessionAuthenticationPolicy()
        stack_policy.add_policy('session', session_policy)

        who2_policy = WhoV2AuthenticationPolicy('config/who.ini', 'auth_tkt', callback=verify_user)
        stack_policy.add_policy('who2', who2_policy)

        save_policy = BisqueSavePolicy()
        stack_policy.add_policy('saved', save_policy)

    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(stack_policy)
    config.set_authorization_policy(authz_policy)









