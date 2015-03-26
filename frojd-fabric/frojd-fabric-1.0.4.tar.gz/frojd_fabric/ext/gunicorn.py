# -*- coding: utf-8 -*-

"""
frojd_fabric.ext.gunicorn
-------------------------
Contains methods for dealing with the gunicorn server.
"""

from fabric.decorators import task
from fabric.state import env


@task
def restart_gunicorn():
    env.run("service gunicorn restart")
