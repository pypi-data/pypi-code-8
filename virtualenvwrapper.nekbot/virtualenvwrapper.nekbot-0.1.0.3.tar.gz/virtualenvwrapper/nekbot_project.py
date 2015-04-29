#!/usr/bin/env python
# encoding: utf-8
"""Create bots automatically with virtualenvwrapper.
"""
__author__ = 'nekmo'

import logging
import os
import subprocess

log = logging.getLogger('virtualenvwrapper.nekbot')


def template(args):
    """Installs NekBot and runs nekbot-admin to create a new bot.
    """
    project, project_dir = args
    os.chdir(project_dir)
    subprocess.check_call(['pip', 'install', 'nekbot'])
    log.info('Running "nekbot-admin createbot %s"', project)
    subprocess.check_call(['nekbot-admin', 'createbot', project])
    return