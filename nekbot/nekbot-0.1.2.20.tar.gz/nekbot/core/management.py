import os
import logging
import sys
import shutil

__author__ = 'nekmo'
__dir__ = os.path.abspath(os.path.dirname(__file__))

nekbot_src_dir = os.path.dirname(os.path.dirname(__file__))
conf_src_dir = os.path.join(nekbot_src_dir, 'conf')


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


class Management(object):
    no_configuration_required = ['createbot']

    def __init__(self, settings=None, description=None, default_level=logging.INFO):
        self.parser = self.argument_parser(settings, description, default_level)

    def argument_parser(self, settings=None, description=None, default_level=logging.INFO):
        import argparse
        if settings is None:
            settings = os.environ.get('NEKBOT_SETTINGS_MODULE', 'settings')
        if description is None:
            from __main__ import __doc__ as description
        parser = argparse.ArgumentParser(prog='nekbot', description=description)
        # Niveles de logging
        parser.add_argument('-q', '--quiet', help='set logging to ERROR',
                            action='store_const', dest='loglevel',
                            const=logging.ERROR, default=logging.INFO)
        parser.add_argument('-d', '--debug', help='set logging to DEBUG',
                            action='store_const', dest='loglevel',
                            const=logging.DEBUG, default=logging.INFO)
        parser.add_argument('-v', '--verbose', help='set logging to COMM',
                            action='store_const', dest='loglevel',
                            const=5, default=logging.INFO)
        parser.add_argument('-s', '--settings', help='Settings file module',
                            default=settings)
        parser.sub = parser.add_subparsers()
        # Subcommand Create bot
        parser_createbot = parser.sub.add_parser('createbot', help='Create a new bot directory usign template.')
        parser_createbot.set_defaults(which='createbot')
        parser_createbot.add_argument('name')
        parser_createbot.add_argument('dest', nargs='?', default=None)
        # Subcommand start
        parser_start = parser.sub.add_parser('start', help='Start bot.')
        parser_start.set_defaults(which='start')
        return parser

    def execute(self, parser=None):
        from nekbot.conf import settings
        if parser is None:
            parser = self.parser
        args = parser.parse_args()
        if not args.which in self.no_configuration_required:
            settings.configure(args.settings)
        logging.basicConfig(level=args.loglevel)
        if not hasattr(self, 'command_' + args.which):
            raise ValueError('Comand %s is invalid.' % args.which)
        getattr(self, 'command_' + args.which)(args)

    def command_createbot(self, args):
        if args.dest:
            dest = args.dest
        else:
            dest = args.name
        if not args.dest and os.path.exists(dest):
            sys.stderr.write("Sorry, directory %s exists. I can't create directory.\n" % dest)
            sys.exit(1)
        elif not os.path.exists(dest):
            os.mkdir(dest)
        try:
            copytree(os.path.join(conf_src_dir, 'project_template'), dest)
        except Exception as e:
            sys.stderr.write('Unknown error: %s\n' % e)
        print('Project created as %s' % dest)

    def command_start(self, args):
        from nekbot import NekBot
        nekbot = NekBot()
        nekbot = nekbot.start()
        try:
            nekbot.loop()
        except (KeyboardInterrupt, SystemExit):
            nekbot.close()