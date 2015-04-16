from __future__ import absolute_import

import os

from zymbit.linux.util import create_ssh_key
from zymbit.util import run_command

from . import config


def enable_init_script():
    os.chmod(config.INIT_SCRIPT_PATH, 0755)

    script_dir = os.path.dirname(config.INIT_SCRIPT_PATH)

    command = ('/usr/sbin/update-service', '--add', script_dir)

    return run_command(command)


def start_service():
    script_dir = os.path.dirname(config.INIT_SCRIPT_PATH)
    command = ('/usr/bin/supervise', script_dir)
    return run_command(command)
