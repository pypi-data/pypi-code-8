# -*- coding: UTF-8 -*-
"""
    trytond_async.celery

    Implementation of the celery app

    This module is named celery because of the way celery workers lookup
    the app when `--proj` argument is passed to the worker. For more details
    see the celery documentation at:
    http://docs.celeryproject.org/en/latest/getting-started/next-steps.html#about-the-app-argument
"""
from __future__ import absolute_import

from celery import Celery
from trytond.config import CONFIG

CONFIG.update_etc()

app = Celery(
    'trytond_async',
    broker=CONFIG.options.get('broker_url'),
    backend=CONFIG.options.get('backend_url'),
    include=['trytond_async.tasks']
)

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_TASK_SERIALIZER='tryson',
    CELERY_RESULT_SERIALIZER='tryson',
    CELERY_ACCEPT_CONTENT=[
        'application/x-tryson',
        'application/x-python-serialize'
    ]
)

if __name__ == '__main__':
    app.start()
