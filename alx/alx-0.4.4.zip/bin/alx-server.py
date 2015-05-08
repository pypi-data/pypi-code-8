#!/usr/bin/env python

"""
** ALX Swiss Army Knife
**
**  Author: Alex Gomes
**  Download: https://github.com/gomes-/alx
**  Copyright: All Rights Reserved. 2015
"""

debug = False
_version = "0.4.4"
__author__ = 'Alex Gomes'

_msg_help = """
Key not set

1) Download key file at https://github.com/gomes-/alx/blob/master/alexkey.py
2) Edit the file and put your keys (don't add extra space)
3) Store in a safe place
4) Run the command

$ alx keydir /path/to/file/dir

5) Run alx-server.py
"""



# To kick off the script, run the following from the python directory:
# PYTHONPATH=`pwd` python testdaemon.py start

# standard python libs
import logging, time
import os, sys, platform
from gettext import gettext as _

path_file = os.path.abspath(__file__)
dir_path = os.path.dirname(path_file)
dir_top = os.path.split(dir_path)[0]
dir_alxlib = os.path.join(dir_top, 'alxlib')

if os.path.isdir(dir_alxlib):
    sys.path.insert(0, dir_top)

import alxlib.key


if debug:
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')


def check_key():
    key = alxlib.key.Key()
    if key.exist():
        return True
    else:
        print(_msg_help)
        return False


def run():
    import alxlib.cloud.azure

    azure = alxlib.cloud.azure.Azure()

    if azure.connect_sqs() == None:
        logging.critical("Azure connection failure, daemon will not run")
        exit()
    else:
        logging.info("alx-server running ...")
        azure.server_run()


def run_linux(app):
    try:
        #app.run()

        import daemon
        from daemon import runner

        #Solution 1
        #with daemon.DaemonContext():
        #    run()

        #Solution 2
        #working_directory='/opt/lib/alx-server'
        context = daemon.DaemonContext(
            working_directory='/tmp',
            umask=0o002,
            pidfile=daemon.pidfile.PIDLockFile('/var/run/alx-server.pid')
            )

        with context:
            app.run()

        #Solution 3
        """
        logger = logging.getLogger("alx-server-log")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler("/var/log/alx-server.log")
        handler.setFormatter(formatter)
        logger.addHandler(handler)"""

        """daemon_runner = runner.DaemonRunner(app)
        #This ensures that the logger file handle does not get closed during daemonization
        #daemon_runner.daemon_context.files_preserve = [handler.stream]
        daemon_runner.do_action()
        #"""
    except Exception as e:
        logging.critical("Error daemon: {0}".format(e))


class App():
    def __init__(self, func):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        #self.pidfile_path = '/tmp/alx-server.pid'
        self.pidfile_path = '/var/run/alx-server.pid'
        self.pidfile_timeout = 5
        self.func = func

    def run(self):
        self.func()


if check_key():
    try:
        import platform

        if platform.system().lower() == "windows":
            run()
        elif len(sys.argv)>0 and sys.argv[0].lower()=='shell':
            run()
        else:
            print("#To run in shell")
            print("usage: alx-server shell")
            logging.info("alx-server: Running daemon for linux..")
            run_linux(App(run))
    except Exception as e:
        logging.critical("Error running: {0}".format(e))

