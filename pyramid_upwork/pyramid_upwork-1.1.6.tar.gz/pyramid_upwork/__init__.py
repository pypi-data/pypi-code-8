from pyramid.config import ConfigurationError
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


from .views import Login, Logout, OauthCallback, forbidden


def includeme(config):
    """Include Upwork auth settings into pyramid config.

    This function does the following:

    * Setup default authentication and authorization policies, and a default
      session factory. Keep in mind that the sessions are not encrypted,
      if you need to store secret information in it, please override
      the session factory.
    * Set login and logout views for use with Upwork auth.
    * Set a forbidden view with a loggin button.

    """
    settings = config.get_settings()

    if 'redis.sessions.secret' not in settings:
        raise ConfigurationError('Missing ``redis.sessions.secret`` setting.\n'
                                 'Probably ``pyramid_redis_sessions`` is not '
                                 'installed')

    if 'upwork.api.key' not in settings:
        raise ConfigurationError('Missing ``upwork.api.key`` setting')

    if 'upwork.api.secret' not in settings:
        raise ConfigurationError('Missing ``upwork.api.secret`` setting')

    # We depend on ``pyramid_redis_sessions``
    config.include('pyramid_redis_sessions')

    # Authentication and authorization policies.
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    authn_policy = SessionAuthenticationPolicy(
        callback=config.registry.get_acl_group)
    config.set_authentication_policy(authn_policy)

    # Login and logout views.
    login_route = settings.get('upwork.login_route', 'login')
    config.registry['upwork.login_route'] = login_route
    login_path = settings.get('upwork.login_path', '/upwork-auth/login')
    config.add_route(login_route, login_path)
    config.add_view(Login, route_name=login_route,
                    permission='login', check_csrf=True)

    logout_route = settings.get('upwork.logout_route', 'logout')
    config.registry['upwork.logout_route'] = logout_route
    logout_path = settings.get('upwork.logout_path', '/upwork-auth/logout')
    config.add_route(logout_route, logout_path)
    config.add_view(Logout, route_name=logout_route,
                    permission=NO_PERMISSION_REQUIRED, check_csrf=True)

    callback_route = settings.get('upwork.callback_route', 'oauth_callback')
    config.registry['upwork.logout_route'] = callback_route
    callback_path = settings.get('upwork.callback_path',
                                 '/upwork-auth/callback')
    config.add_route(callback_route, callback_path)
    config.add_view(OauthCallback, route_name=callback_route,
                    permission='login')

    # A simple 403 view, with a login button.
    config.add_forbidden_view(
        forbidden, renderer='templates/forbidden.jinja2')
