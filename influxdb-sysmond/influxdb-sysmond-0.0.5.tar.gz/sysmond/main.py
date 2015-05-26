"""
Influx-Sysmond (InfluxDB System Monitoring Client) by Evan Darwin

Usage:
    influx-sysmond [-h | --help] <config>

Options:
    -h --help       Display this message
    -V --version    Display the application version
    -v --verbose    Display verbose logging information

    -d              Detach and run as a daemon
    --dump          Dumps the JSON data to be sent (warning: spammy!)
"""

VERSION = "0.0.5"

from os import path

from docopt import docopt
from . import Config, Daemon

import subprocess

def main():
    args = docopt(__doc__, version='InfluxDB-sysmond version ' + VERSION)

    daemon_config = Config(path.abspath(args['<config>']))
    daemon = Daemon(daemon_config)
