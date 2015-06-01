# -*- coding: utf-8 -*-
from django.db.models.options import get_verbose_name
from gumby.basehealthcheck import HealthCheckStatusType, BaseHealthCheck
from gumby.healthchecks import healthchecks_dir


class HealthCheck(BaseHealthCheck):
    def check_status(self):
        self._wrapped()


def healthcheck(func_or_name):
    """
    Usage:
        @healthcheck("My Check")
        def my_check():
            if something_is_not_okay():
                raise ServiceReturnedUnexpectedResult()
        @healthcheck
        def other_check():
            if something_is_not_available():
                raise ServiceUnavailable()
    """
    def inner(func):
        cls = type(func.__name__, (HealthCheck,), {'_wrapped': staticmethod(func)})
        cls.identifier = name
        healthchecks_dir.register(cls)
        return func
    if callable(func_or_name):
        name = get_verbose_name(func_or_name.__name__).replace('_', ' ')
        return inner(func_or_name)
    else:
        name = func_or_name
        return inner
