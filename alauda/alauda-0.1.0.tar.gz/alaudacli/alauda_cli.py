import sys
import copy

from alaudacli import cmd_parser, cmd_processor


def patch_argv(argv):
    args = copy.copy(argv)

    if not args:
        print 'Arguments cannot be empty.'
        sys.exit(1)

    if len(args) == 1:
        args.append('-h')
    elif len(args) == 2 and args[1] in ['service']:
        args.append('-h')
    elif len(args) == 3:
        if args[1] == 'service' and args[2] in ['create', 'update', 'get', 'start', 'stop', 'delete']:
            args.append('-h')

    return args[1:]


def main():
    argv = patch_argv(sys.argv)
    args = cmd_parser.parse_cmds(argv)
    cmd_processor.process_cmds(args)

if __name__ == '__main__':
    main()
