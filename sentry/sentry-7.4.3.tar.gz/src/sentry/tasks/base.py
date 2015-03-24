"""
sentry.tasks.base
~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2014 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from celery.task import current, task
from functools import wraps

from sentry.utils import metrics


def instrumented_task(name, stat_suffix=None, **kwargs):
    def wrapped(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            key = 'jobs.duration.{name}'.format(name=name)
            if stat_suffix:
                key += '.{key}'.format(key=stat_suffix(*args, **kwargs))
            with metrics.timer(key):
                result = func(*args, **kwargs)
            return result
        return task(name=name, **kwargs)(_wrapped)
    return wrapped


def retry(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            current.retry(exc=exc)
    return wrapped
