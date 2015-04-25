#!/bin/env python
# -*- coding: utf-8 -*-

import os
import grp
import signal
import daemon
import lockfile

import include
from dockerfly.settings import dockerfly_version
from dockerfly.settings import RUN_ROOT, LOG_ROOT, DB_ROOT

if not os.path.exists(RUN_ROOT):
    os.makedirs(RUN_ROOT)
if not os.path.exists(LOG_ROOT):
    os.makedirs(LOG_ROOT)
if not os.path.exists(DB_ROOT):
    os.makedirs(DB_ROOT)

from dockerfly.logger import getLogger, getFh
from dockerfly.http.server import run_server

pid_file = os.path.join(RUN_ROOT, 'dockerflyd.pid.lock')
logger = getLogger()

def dockerflyd_setup():
    if os.path.exists(pid_file):
        logger.error("{} has already existed".format(pid_file))

def dockerflyd_cleanup():
    if os.path.exists(pid_file):
        os.remove(pid_file)

def dockerflyd_reload_config():
    pass

def terminate():
    os.kill(os.getpid(), signal.SIGTERM)

context = daemon.DaemonContext(
    working_directory=RUN_ROOT,
    umask=0o002,
    pidfile=lockfile.FileLock(os.path.join(RUN_ROOT, 'dockerflyd.pid')),
    files_preserve = [getFh().stream,],
)

context.signal_map = {
    signal.SIGTERM: dockerflyd_cleanup,
    signal.SIGHUP: terminate,
    signal.SIGUSR1: dockerflyd_reload_config,
    }

mail_gid = grp.getgrnam('mail').gr_gid
context.gid = mail_gid

def rundaemon(host, port):
    dockerflyd_setup()

    with context:
        run_server(host=host, port=port, debug=True)

if __name__ == '__main__':

    rundaemon(host='0.0.0.0', port=5123)

