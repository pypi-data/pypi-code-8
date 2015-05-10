
from django.apps import AppConfig


default_app_config = 'leonardo_module_saml.SamlConfig'


class Default(object):

    apps = [
        'leonardo_module_saml',
        'djangosaml2'
    ]

    auth_backends = [
        'djangosaml2.backends.Saml2Backend',
    ]


class SamlConfig(AppConfig, Default):
    name = 'leonardo_module_saml'
    verbose_name = ("SAML Auth")

default = Default()
