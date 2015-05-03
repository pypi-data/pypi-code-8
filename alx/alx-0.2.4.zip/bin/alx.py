#!/usr/bin/env python

"""
** ALX Swiss Army Knife
**
**  Author: Alex Gomes
**  Download: https://github.com/gomes-/alx
**  Copyright: GPL v3.0
"""

debug = False
_version = "0.2.4"
__author__ = 'Alex Gomes'

msg_help = """
Examples:

    # Save a command
    alx save 'ssh -i azure.pem ubuntu@ubuntu.cloudapp.net' -n connect
    alx save 'ssh -i azure.pem ubuntu@ubuntu.cloudapp.net'

    # Save & Run command
    alx run 'ssh -i azure.pem ubuntu@ubuntu2.cloudapp.net' -n connect2
    alx run 'ssh -i azure.pem ubuntu@ubuntu2.cloudapp.net'

    # Execute saved command
    alx do connect
    # Execute last command
    alx do last
    alx do

    # Remove command
    alx flush connect
    # Remove all command
    alx flush

   more at https://github.com/gomes-/alx/blob/master/CHEATSHEET.md
"""

import sys
import os
import logging
from optparse import OptionParser

path_file = os.path.abspath(__file__)
dir_path = os.path.dirname(path_file)
dir_top = os.path.split(dir_path)[0]
dir_alxlib = os.path.join(dir_top, 'alxlib')

if os.path.isdir(dir_alxlib):
    sys.path.insert(0, dir_top)

import alx


msg_default = "This feature has not been implemented yet"
msg_err_arg = "Error: Incorrect number of arguments"

if debug:
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.CRITICAL, format=' %(asctime)s - %(levelname)s - %(message)s')

parser = OptionParser("usage: %prog arg1 [arg2] [options]", version=_version)


def help_info():
    """ Prints Help
    :return:none
    """

    global parser, msg_help
    parser.print_help()
    print(msg_help)


def main():
    """Entry point of the code
    """
    global debug, parser, msg_default, msg_err_arg

    if '-h' in sys.argv or '--help' in sys.argv:
        print(msg_default)

    # parser.add_option("-f", "--file", dest="filename",
    #                  help="write report to FILE", metavar="FILE")

    parser.add_option("-n", "--name",
                      action="store", dest="name", default="last",
                      help="The 'name', to save your command, default='last'")
    #ToDo
    '''parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=True,
                      help="Print status messages to stdout")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=False,
                      help="Don't print status messages to stdout")'''

    (options, args) = parser.parse_args()
    logging.debug("options:{0}, args:{1}".format(options, args))

    if len(args) > 0:
        choice(options, args)
    else:
        print("\n{0}\n".format(msg_err_arg))
        help_info()

    """if debug:
        input("\nPress any key to exit ...")"""


def choice(options, args):
    global msg_default, msg_err_arg

    #save
    if str(args[0]).lower() == "save":
        if len(args) == 2:
            import alxlib.save

            save = alxlib.save.Save()
            save.set_cmd(options.name, args[1])
        else:
            parser.error(msg_err_arg)

    #run
    elif str(args[0]).lower() == "run":
        import alxlib.save

        save = alxlib.save.Save()

        save.set_cmd(options.name, args[1])
        save.run_cmd(args[1])

    #do
    elif str(args[0]).lower() == "do":
        import alxlib.save

        save = alxlib.save.Save()

        if len(args) == 2:
            cmd = save.get_cmd(args[1])
        else:
            cmd = save.get_cmd(options.name)

        if cmd is not None:
            save.run_cmd(cmd)
        else:
            print("Command not available")


    #flush
    elif str(args[0]).lower() == "flush":
        import alxlib.save

        save = alxlib.save.Save()

        if len(args) == 2:
            save.flush_cmd(args[1])
        elif options.name.lower() != "last":
            save.flush_cmd(options.name);
        else:
            save.flush_all()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        print('Please install Python version 3+ \n for linux: sudo apt-get install python')
        exit()
    else:
        main()
