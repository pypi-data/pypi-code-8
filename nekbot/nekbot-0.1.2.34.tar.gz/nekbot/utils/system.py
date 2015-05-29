from logging import getLogger
import sys
import os
import shlex
import subprocess
from nekbot.utils.modules import get_module

__author__ = 'nekmo'

logger = getLogger('utils.system')

def reboot():
    args = sys.argv[:]
    logger.info('Re-spawning %s' % ' '.join(args))

    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]

    _startup_cwd = os.getcwd()
    os.chdir(_startup_cwd)
    os.execv(sys.executable, args)

def execute_hook(hook, *args, **kwargs):
    if hook.startswith('python:'):
        function = hook.split('python:', 1)[1]
        function = get_module(function)
        function(*args, **kwargs)
    else:
        environ = os.environ.copy()
        for i, arg in enumerate(args):
            environ['Nekbot-arg-%i' % i] = str(arg)
        for key, value in kwargs.items():
            environ['Nekbot-kwarg-%s' % key] = str(value)
        subprocess.Popen(shlex.split(hook), env=environ)