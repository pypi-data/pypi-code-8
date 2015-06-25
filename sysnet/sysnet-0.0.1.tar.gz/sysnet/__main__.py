"""
sysnet

Server Administrator



"""

import sys
import time
import sysnet
import argparse
import subprocess

ARG_PARSER = False

def arg_setup():
    global ARG_PARSER
    ARG_PARSER = argparse.ArgumentParser(description=sysnet.__description__)
    ARG_PARSER.add_argument("--version", "-v", action="version", \
        version=u"sysnet " + unicode(sysnet.__version__) )
    initial = vars(ARG_PARSER.parse_args())
    args = {}
    for arg in initial:
        if initial[arg]:
            args[arg] = initial[arg]
    return args

def main():
    print (sysnet.__logo__)
    args = arg_setup()
    # Get the action
    # action = getattr(sys.modules[__name__], args["action"])
    # del args["action"]
    # action(args)
    # return 0

if __name__ == '__main__':
    main()
