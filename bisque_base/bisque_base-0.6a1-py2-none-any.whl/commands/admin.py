import sys
import os
import subprocess
import re
import pkg_resources
import bq
import optparse
import errno
import logging
import operator

from bq.release import __VERSION__

LOG_LEVELS = {'debug': logging.DEBUG,
                       'info': logging.INFO,
                       'warning': logging.WARNING,
                       'error': logging.ERROR,
                       }



def _help(commands):
    "Custom help text for bq-admin."

    commandls = []
    longest = max(len(key) for key in commands.keys())
    format = "%" + str(longest) + "s  %s"
    #commandlist = commands.keys()
    #commandlist.sort()
    for key,val  in sorted(commands.items(), key = operator.itemgetter(0)):
        commandls .append ( format % (key, val[0] if val else key))
    return  """
Bisque %s command line interface

Commands:
%s""" % (__VERSION__, "\n".join(commandls))


def _load_commands(load=False, name=None):
    commands = {}
    for entrypoint in pkg_resources.iter_entry_points("bisque.commands"):
        if load or name:
            if name and name != entrypoint.name:
                continue
            print "Loading ", entrypoint
            command = entrypoint.load()
            commands[entrypoint.name] = (command.desc, entrypoint)
        else:
            commands[entrypoint.name] = None
    return commands


def main():
    """Main entrypoint for bq-admin commands"""
    commands = {}


    parser = optparse.OptionParser(usage = _help(_load_commands()))
    parser.allow_interspersed_args = False
    #parser.add_option("-c", "--config", dest="config")
    #parser.add_option("-e", "--egg", dest="egg")
    parser.add_option("--logging", default="info", help = "logging level = %s" % "|".join(LOG_LEVELS.keys()))
    #parser.print_help = _help
    (options, args) = parser.parse_args(sys.argv[1:])
    #if not args or not commands.has_key(args[0]):
    #    _help()
    #    sys.exit()
    logging.basicConfig(level = LOG_LEVELS.get (options.logging, logging.INFO))

    if len(args) < 1:
        parser.error("Command needed")
    commandname = args[0]
    commands = _load_commands(True, name=commandname)

    if commandname not in commands:
        parser.error("Need a valid command")

    # strip command and any global options from the sys.argv
    sys.argv = [sys.argv[0],] + args[1:]
    command = commands[commandname][1]
    command = command.load()
    command = command(__VERSION__)
    command.run()

