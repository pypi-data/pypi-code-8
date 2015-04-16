from __future__ import absolute_import

import os

from zymbit.util import run_command

from . import config


def create_ssh_key():
    command = ('/usr/bin/dropbearkey', '-t', 'rsa', '-s', '2048', '-f', config.TUNNEL_SSH_KEY_PATH)
    return run_command(command)


def enable_init_script():
    os.chmod(config.INIT_SCRIPT_PATH, 0755)

    command = (config.INIT_SCRIPT_PATH, 'enable')
    return run_command(command)


def start_service():
    command = (config.INIT_SCRIPT_PATH, 'start')
    return run_command(command)
