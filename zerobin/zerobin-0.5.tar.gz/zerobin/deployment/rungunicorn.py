#!/usr/bin/env python

from __future__ import absolute_import

from bottle import run

from .wsgi import settings, application

run(application, host=settings.HOST, port=settings.PORT, server="gunicorn")
