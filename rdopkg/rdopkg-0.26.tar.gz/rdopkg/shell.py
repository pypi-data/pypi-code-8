# -*- encoding: utf-8 -*-

import sys
import argparse

import rdoupdate
import rdoupdate.exception

from . import VERSION
import core
import exception
from utils import log


def action2cmd(action):
    return action.replace('_', '-')


def optarg2cmdarg(arg):
    return "--%s" % action2cmd(arg)


def get_action_args(action, args):
    aargs = {}
    for rarg in action.required_args:
        aargs[rarg.name] = getattr(args, action2cmd(rarg.name))
    for oarg in action.optional_args:
        val = getattr(args, oarg.name)
        if val:
            aargs[oarg.name] = val
    return aargs


def get_parser(runner):
    parser = argparse.ArgumentParser(prog='rdopkg')
    subparsers = parser.add_subparsers(help='available actions')
    parser.add_argument('-i', '--info', action='store_true',
                        help='show information about current action')
    parser.add_argument('-c', '--continue', action='store_true',
                        help='continue running current action')
    verinfo = "%s (rdoupdate %s)" % (VERSION, rdoupdate.VERSION)
    parser.add_argument('--version', action='version', version=verinfo)
    for action in runner.action_manager.actions:
        cmd = action2cmd(action.name)
        action_parser = subparsers.add_parser(cmd, help=action.help,
                                              description=action.help)
        for oarg in action.optional_args:
            if oarg.positional:
                arg_names = [oarg.name]
            else:
                arg_names = oarg.cmdarg_names(optarg2cmdarg)
            action_parser.add_argument(*arg_names, **oarg.kwargs)
        for rarg in action.required_args:
            arg_names = rarg.cmdarg_names(action2cmd)
            action_parser.add_argument(*arg_names, **rarg.kwargs)
        action_parser.set_defaults(action=action)
    return parser


def main(cargs=None):
    if not cargs:
        cargs = sys.argv[1:]

    runner = core.ActionRunner()
    runner.load_state_safe()

    parser = get_parser(runner)
    if not cargs:
        parser.print_help()
        return
    # argparse still can't do this with subparsers (reported 2009)
    if '-i' in cargs or '--info' in cargs:
        runner.info()
        return
    elif '-c' in cargs or '--continue' in cargs:
        # state already loaded
        pass
    else:
        args = parser.parse_args(cargs)
        action = args.action
        action_args = get_action_args(action, args)
        runner.new_action(action, action_args)

    code = 1
    try:
        runner.engage()
        code = 0
    except (
            exception.BranchNotFound,
            exception.BuildArchSanityCheckFailed,
            exception.CantGuess,
            exception.ConfigError,
            exception.CoprError,
            exception.DebugAbort,
            exception.FileNotFound,
            exception.IncompleteChangelog,
            exception.InvalidPackageFilter,
            exception.InvalidQuery,
            exception.InvalidUsage,
            exception.ManualResolutionNeeded,
            exception.NotADirectory,
            exception.RequiredActionArgumentNotAvailable,
            exception.RequirementNotMet,
            exception.RpmModuleNotAvailable,
            exception.SpecFileNotFound,
            exception.ToolNotFound,
            exception.UserAbort,
            exception.UpdateCheckFailed,
            rdoupdate.exception.InvalidUpdateStructure,
            rdoupdate.exception.BuildNotAvailable,
            KeyboardInterrupt,
            ) as ex:
        print("")
        print log.term.important(str(ex) or type(ex).__name__)
    except exception.NoActionInProgress as ex:
        print "%s See `rdopkg -h` for help." % ex
    except exception.CommandFailed as ex:
        # this was logged already
        pass
    return code

if __name__ == '__main__':
    code = main()
    sys.exit(code)
