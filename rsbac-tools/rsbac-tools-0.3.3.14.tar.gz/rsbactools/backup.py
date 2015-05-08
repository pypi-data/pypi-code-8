#
# function that return the backup commands
# only with prefix backup_ in name        
#

import os
import sys
import re
import argparse
import time
import datetime
from subprocess import Popen, PIPE

import logging
logging.basicConfig(format='%(levelname)s:%(name)s:line %(lineno)s: %(message)s')
log = logging.getLogger(__name__)

try:
    from rsbactools import rsbac, RSBAC_PROC_INFO_DIR
except ImportError as error:
    sys.exit(error)


# timestamp
TIMESTAMP = str("%0.f" % datetime.datetime.now().timestamp())
# default backup directory
BACKUP_DIRECTORY = os.path.join(os.getcwd(), "backup")
BACKUP_DIRECTORY_TODAY = os.path.join(
        str(datetime.datetime.now().year),
        str(datetime.datetime.now().month),
        str(datetime.datetime.now().day)
)

# BACKUP_MODULES contains module names which have no entry in 
# /proc/rsbac-info/active or similar
BACKUP_MODULES = ["general", "net", "log", "user"]

# BACKUP_MODULES_EXCLUDE contains module names which are not backup.
#   e.g. JAIL is only process based
BACKUP_MODULES_EXCLUDE = ["JAIL"]

# command function must return a list 
def command_log():
    return ["switch_adf_log", "-b"]

def command_net():
    return [
        ["net_temp", "-a", "-b"], 
        ["attr_back_net", "-a", "NETDEV"], 
        ["attr_back_net", "-a", "NETTEMP"]
    ]

def command_general():
    cmd = []
    for module, status in rsbac.Rsbac().get_modules()["Module"].items():
        if module in BACKUP_MODULES_EXCLUDE:
            continue
        if status == "on":
            cmd.append(["attr_back_fd", "-r", "-M", module, "/"])
            cmd.append(["attr_back_dev", "b"])
    return cmd

def command_auth():
    return ["auth_back_cap", "-r", "/"]

def command_um():
    return [
        ["rsbac_groupshow", "-S", "all", "-b", "-p", "-a"],
        ["rsbac_usershow", "-S", "all", "-b", "-p", "-a"]
    ]
    
def command_rc():
    return ["rc_get_item", "backup"]

def command_user():
    cmd = []
    for module, status in rsbac.Rsbac().get_modules()["Module"].items():
        if module in BACKUP_MODULES_EXCLUDE:
            continue
        if status == "on":
            cmd.append(["attr_back_user", "-a", "-M", module])
    return cmd

def command_pax():
    return []


class Backup(object):
    """Backup RSABAC attribute modules based."""

    def __init__(self):
        self.args = {}
        self.backup_directory = BACKUP_DIRECTORY
        # set the module which should be backuped
        self.modules_to_backup()

    def set_args(self, args):
        self.args = args

    def set_log_level(self, log_level):
        log.setLevel(log_level)

    def get_log_level(self):
        return log.getEffectiveLevel()

    def modules_to_backup(self):
        """Get available modules and extend the module list."""
        modules = []
        for module, status in rsbac.Rsbac().get_modules()["Module"].items():
            if status == "on" and module not in BACKUP_MODULES_EXCLUDE:
                modules.append(module.lower())
        if os.path.exists(os.path.join(RSBAC_PROC_INFO_DIR, "stats_um")):
            modules.append("um")
        BACKUP_MODULES.extend(modules)

    def execute(self, module):
        """Execute the module command and write to different files the result.
            The name are build: 
                backup_timestamp.sh
                command_timestamp.sh
                error_timestamp.sh
        """
        # build function name and call the function to get the shell commands
        cmd = globals()["_".join(["command", module])]()

        # build files path and name
        b = os.path.join(self.backup_directory, "backup_" + TIMESTAMP + ".sh")
        e = os.path.join(self.backup_directory, "error_" + TIMESTAMP + ".sh")
        c = os.path.join(self.backup_directory, "command_" + TIMESTAMP + ".sh")
        
        with open(b, "w") as bf, open(e, "w") as ef, open(c, "w") as cf:
            if isinstance(cmd[0], str):
                cf.write(" ".join([str(x) for x in cmd]) + "\n")
                process = Popen(cmd, stdin=PIPE, stdout=bf, stderr=ef)
                process.wait()
                bf.flush()
            else:
                for i in cmd:
                    cf.write(" ".join([str(x) for x in i]) + "\n")
                    process = Popen(i, stdin=PIPE, stdout=bf, stderr=ef)
                    process.wait()
                    bf.flush()
    
    def update_backup_path(self, path):
        self.backup_directory = os.path.join(self.backup_directory, path)

    def run(self):
        if self.args["directory"]:
            self.backup_directory = self.args["directory"]
        self.update_backup_path(BACKUP_DIRECTORY_TODAY)
        for module in BACKUP_MODULES:
            if module in self.args and not self.args[module]:
                continue
            try:
                self.update_backup_path(module)
                try:
                    log.info("create backup path: %s" % self.backup_directory)
                    os.makedirs(self.backup_directory)
                except OSError as error:
                    log.error(error)
                log.info("starting backup: %s" % module)
                self.execute(module)
                log.info("done ...")
            except KeyError as error:
                log.info("Not implemented: %s()" % module)

