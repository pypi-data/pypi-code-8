
from django.apps import AppConfig


default_app_config = 'leonardo_module_oauth.OAuthConfig'


class Default(object):

    @property
    def apps(self):
        apps = [
            'leonardo_module_oauth',

            'allauth',
            'allauth.account',
            'allauth.socialaccount',
        ]
        try:
            from .settings import PROVIDERS
        except Exception:
            pass
        try:
            from local_settings import PROVIDERS  # noqa
        except Exception:
            pass
        apps += PROVIDERS
        return apps

    auth_backends = [
        'allauth.account.auth_backends.AuthenticationBackend',
    ]

    context_processors = [
        'allauth.account.context_processors.account',
        'allauth.socialaccount.context_processors.socialaccount',
    ]


class OAuthConfig(AppConfig, Default):
    name = 'leonardo_module_oauth'
    verbose_name = ("All Auth")

default = Default()
