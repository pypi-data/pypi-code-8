
import logging


LOG = logging.getLogger(__name__)


class Default(object):

    @property
    def middlewares(self):
        return [
            'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
        ]

    @property
    def apps(self):

        return [

            'leonardo_module_sentry',
            'raven.contrib.django.raven_compat',

        ]

default = Default()
