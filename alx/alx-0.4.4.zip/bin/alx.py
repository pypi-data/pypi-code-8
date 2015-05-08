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
Examples:

    # Save a command
    alx save 'ssh -i azure.key ubuntu@ubuntu.cloudapp.net' -n connect
    alx save 'ssh -i azure.key ubuntu@ubuntu2.cloudapp.net'

    # Save & Run command
    alx run 'ssh -i azure.key ubuntu@ubuntu3.cloudapp.net' -n connect3
    alx run 'ssh -i azure.key ubuntu@ubuntu4.cloudapp.net'

    # Execute saved command
    alx do connect
    alx do -n connect
    # Execute last command
    alx do last
    alx do

    # Remove command
    alx flush connect
    # Remove all
    alx flush

   more at https://github.com/gomes-/alx/blob/master/CHEATSHEET.md
"""

import sys, os, time
import logging
from optparse import OptionParser
from gettext import gettext as _

path_file = os.path.abspath(__file__)
dir_path = os.path.dirname(path_file)
dir_top = os.path.split(dir_path)[0]
dir_alxlib = os.path.join(dir_top, 'alxlib')

if os.path.isdir(dir_alxlib):
    sys.path.insert(0, dir_top)

import alxlib
import alxlib.help.msg as msg


if debug:
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.CRITICAL, format=' %(asctime)s - %(levelname)s - %(message)s')

_parser = OptionParser("usage: alx <{save|run|do|list|flush}> [arg2] [options]", version=_version)


def help_info():
    """ Prints Help
    :return:none
    """

    global _parser, _msg_help
    print(_(_msg_help))


def main():
    """Entry point of the code
    """
    # import alxlib.help.msg as msg
    global debug, _parser
    #msg.default, msg.err_arg

    if '-h' in sys.argv or '--help' in sys.argv:
        print(msg.default)

    # parser.add_option("-f", "--file", dest="filename",
    #                  help="write report to FILE", metavar="FILE")

    _parser.add_option("-n", "--name",
                       action="store", dest="name", default="last",
                       help="The 'name', to save your command, default='last'")
    _parser.add_option("-c", "--count",
                       action="store", dest="count", default=1,
                       help="Count for 'nodes ping', default=1")
    _parser.add_option("-t", "--timeout",
                       action="store", dest="timeout", default=30,
                       help="Timeout for 'nodes ping', default=1")
    _parser.add_option("-v", "--verbose",
                       action="store_true", dest="verbose", default=True,
                       help="Print status messages to stdout")
    _parser.add_option("-q", "--quiet",
                       action="store_false", dest="verbose", default=False,
                       help="Don't print status messages to stdout")


    (options, args) = _parser.parse_args()
    logging.debug("options:{0}, args:{1}".format(options, args))

    if len(args) > 0:
        choice(options, args)
    else:
        _parser.print_help()
        help_info()
        print(msg.err_arg)

    """if debug:
        input("\nPress any key to exit ...")"""


def choice(options, args):
    # global msg.default, msg.err_arg, msg.err_cmd

    #save
    if str(args[0]).lower() == "save":
        if len(args) == 2:
            import alxlib.save

            save = alxlib.save.Save()
            save.set_cmd(options.name, args[1])
        else:
            _parser.print_help()
            _parser.error(msg.err_arg)

    #run
    elif str(args[0]).lower() == "run":
        if len(args) == 2:
            import alxlib.save

            save = alxlib.save.Save()
            save.set_cmd(options.name, args[1])
            save.run_cmd(args[1], options.verbose)
        else:
            _parser.print_help()
            _parser.error(msg.err_arg)

    #do
    elif str(args[0]).lower() == "do":
        import alxlib.save

        save = alxlib.save.Save()

        if len(args) == 2:
            cmd = save.get_cmd(args[1])
        else:
            cmd = save.get_cmd(options.name)

        if cmd is not None:
            save.run_cmd(cmd, options.verbose)
        else:
            _parser.error(msg.err_cmd + (": " + args[1]) if (len(args) == 2) else "")

    #list
    elif str(args[0]).lower() == "list":
        import alxlib.save

        save = alxlib.save.Save()

        if len(args) == 2:
            save.list_cmd(args[1], msg.no_list)
        elif options.name.lower() != "last":
            save.list_cmd(options.name, msg.no_list)
        else:
            save.list_all(msg.no_list)

    #flush
    elif str(args[0]).lower() == "flush":
        import alxlib.save

        save = alxlib.save.Save()

        if len(args) == 2:
            save.flush_cmd(args[1])
        elif options.name.lower() != "last":
            save.flush_cmd(options.name)
        else:
            save.flush_all()
    #cloud
    elif str(args[0]).lower() == "keydir":
        if len(args) == 2:
            import alxlib.save, alxlib.data

            save = alxlib.save.Save()
            save.set_data(alxlib.data.key_dir, args[1])
        else:
            _parser.print_help()
            _parser.error(msg.err_arg)

    elif str(args[0]).lower() == "node" or str(args[0]).lower() == "nodes":
        if len(args) == 2:
            if False:
                pass
            elif str(args[1]).lower() == "list" or str(args[1]).lower() == "ls":
                from alxlib.cloud.azure import Azure
                azure= Azure()
                azure.print_list()
            else:
                #ToDo node help
                _parser.print_help()
                _parser.error(msg.err_arg)
        else:
            _parser.print_help()
            _parser.error(msg.err_arg)
    else:
        _parser.print_help()
        help_info()
        print(msg.err_na_arg)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        print(msg.err_py)
        exit()
    else:
        main()
