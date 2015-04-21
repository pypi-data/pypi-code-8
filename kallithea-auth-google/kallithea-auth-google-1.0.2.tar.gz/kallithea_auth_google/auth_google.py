"""Kallithea google authentication plugin."""
import os
import logging

from kallithea.lib import auth_modules
from kallithea.lib.utils2 import safe_unicode
from kallithea.lib.compat import hybrid_property
from kallithea.model.db import Setting, User

from pylons.controllers.util import redirect
import pylons

from requests_oauthlib import OAuth2Session

log = logging.getLogger(__name__)


class KallitheaAuthPlugin(auth_modules.KallitheaExternalAuthPlugin):

    """Google auth kallithea plugin."""

    scope = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile']

    session_key = 'GOOGLE_AUTH_USER'

    @hybrid_property
    def name(self):
        """Plugin short name."""
        return "google"

    @hybrid_property
    def is_container_auth(self):
        """A container auth."""
        return True

    def get_settings(self):
        """Get plugin settings values."""
        plugin_settings = {}
        for v in self.plugin_settings():
            conf_key = "auth_%s_%s" % (self.name, v["name"])
            setting = Setting.get_by_name(conf_key)
            plugin_settings[v["name"]] = setting.app_settings_value if setting else None
        return plugin_settings

    def settings(self):
        """Get plugin settings declaration."""
        settings = [
            {
                "name": "client_id",
                "validator": self.validators.UnicodeString(strip=True, not_empty=True),
                "type": "string",
                "description": "Client id from the google developer console.",
                "default": "client-id",
                "formname": "Client id"
            },
            {
                "name": "client_secret",
                "validator": self.validators.UnicodeString(strip=True, not_empty=True),
                "type": "string",
                "description": "Client secret from the google developer console.",
                "default": "client-secret",
                "formname": "Client secret"
            },
            {
                "name": "hd",
                "validator": self.validators.UnicodeString(strip=True, not_empty=False),
                "type": "string",
                "description": "Google apps domain to limit authentication to.",
                "default": None,
                "formname": "Google apps domain"
            },
        ]
        return settings

    def use_fake_password(self):
        """Use fake passwords to disable them."""
        return True

    def user_activation_state(self):
        """Perform user activation according to global persmissions."""
        def_user_perms = User.get_default_user().AuthUser.permissions['global']
        return 'hg.extern_activate.auto' in def_user_perms

    def store_user_info(self, code):
        """Store user info given the authentication code."""
        settings = self.get_settings()
        # compensation for broken oauthlib
        os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
        oauth = OAuth2Session(
            settings['client_id'], redirect_uri=pylons.url('oauth2callback', qualified=True),
            scope=self.scope)
        oauth.fetch_token(
            'https://accounts.google.com/o/oauth2/token',
            # Google specific extra parameter used for client
            # authentication
            client_secret=settings['client_secret'],
            code=code)
        response = oauth.get('https://www.googleapis.com/oauth2/v1/userinfo')
        user_info = response.json()
        user_info['username'] = user_info['email'].replace('@', '_at_')
        pylons.session[self.session_key] = user_info
        log.debug('user info stored in session: %s', user_info)

    def _get_user_info(self, environ, settings):
        """Get user info."""
        user_info = pylons.session.get(self.session_key)
        if user_info:
            return user_info
        oauth = OAuth2Session(
            settings['client_id'],
            redirect_uri=pylons.url('oauth2callback', qualified=True),
            state=pylons.request.GET.get('came_from'),
            scope=self.scope)
        kwargs = {}
        if settings['hd']:
            kwargs['hd'] = settings['hd']
        authorization_url, state = oauth.authorization_url(
            'https://accounts.google.com/o/oauth2/auth',
            # access_type and approval_prompt are Google specific extra
            # parameters.
            access_type="offline",
            approval_prompt="force",
            **kwargs)
        redirect(authorization_url)

        log.debug('extracted %s', (authorization_url, state))

        return None

    def get_user(self, username=None, settings=None, **kwargs):
        """Get user given the context."""
        environ = kwargs.get('environ') or {}
        user_info = self._get_user_info(environ, settings)
        username = user_info['username']
        email = user_info['email']
        # we got the username, so use default method now
        user = super(KallitheaAuthPlugin, self).get_user(username)
        if user is None:
            user = User.get_by_email(email)
            # username might differ, but email not
            user.username = username
        return user

    def auth(self, userobj, username, password, settings, **kwargs):
        """Authenticate request."""
        environ = kwargs.get('environ')
        if not environ:
            log.debug('Empty environ data skipping...')
            return None

        if not userobj:
            userobj = self.get_user('', environ=environ, settings=settings)

        # we don't care passed username/password for container auth plugins.
        # only way to log in is using environ
        username = None
        identity = {}
        if userobj:
            username = getattr(userobj, 'username')

        if not username:
            # we don't have any objects in DB user doesn't exist extrac username
            # from environ based on the settings
            identity = self._get_user_info(environ, settings)
            if identity:
                username = identity['username']

        # if cannot fetch username, it's a no-go for this plugin to proceed
        if not username:
            return None

        identity = pylons.session.get(self.session_key)
        admin = getattr(userobj, 'admin', False)
        active = getattr(userobj, 'active', True)
        if identity:
            email = identity.get('email', getattr(userobj, 'email', ''))
            firstname = identity.get('given_name', getattr(userobj, 'firstname', ''))
            lastname = identity.get('family_name', getattr(userobj, 'lastname', ''))
        else:
            email = getattr(userobj, 'email', '')
            firstname = getattr(userobj, 'firstname', '')
            lastname = getattr(userobj, 'lastname', '')
        extern_type = getattr(userobj, 'extern_type', '')

        user_attrs = {
            'username': username,
            'firstname': safe_unicode(firstname or username),
            'lastname': safe_unicode(lastname or ''),
            'groups': [],
            'email': email or '',
            'admin': admin or False,
            'active': active,
            'active_from_extern': True,
            'extern_name': username,
            'extern_type': extern_type,
        }

        log.info('user `%s` authenticated correctly' % user_attrs['username'])
        return user_attrs
