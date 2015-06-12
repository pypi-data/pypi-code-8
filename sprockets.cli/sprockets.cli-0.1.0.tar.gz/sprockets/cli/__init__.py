"""
Sprockets CLI
=============
The sprockets CLI interface for running applications. Applications are meant
to be run by a controller that is managed by the sprockets CLI interface.

The sprockets CLI interface loads controller applications that are registered
using setuptools entry points.

Controllers
-----------

Each controller is expected to expose at least a ``main(application, args)``
method that would be invoked when starting the application. Additional, a
controller can implement a ``add_cli_arguments(parser)`` method that will be
invoked when setting up the command line parameters. This allows controllers
to inject configuration directives into the cli.

Controller API Summary:

.. code: python

    module.add_cli_arguments(ArgumentParser)     # optional
    module.main(app_module, argparse.Namespace)

Plugins
-------

Plugins are able to inject themselves at multiple points in the application
lifecycle. Plugins that implement a ``initialization(controller)`` method will
see that method invoked before a controller is started.  In addition, if a
``on_startup(controller)`` method is defined, it will be invoked after a
Controller has started a application. Finally if a ``on_shutdown(controller)``
method is defined, it will be invoked when a controller has shutdown.

Plugin API Summary:

.. code: python

    plugin.initialize(controller_module)   # optional
    plugin.on_start(controller_module)     # optional
    plugin.on_shutdown(controller_module)  # optional

Applications
------------

Applications can be a python package or module and if they are registered
to a specific controller, can be referenced by an alias. Application contracts
vary by controller.

"""
version_info = (0, 1, 0)
__version__ = '.'.join(str(v) for v in version_info)

import argparse
import importlib
import json
import logging
import string
import sys

# import logutils for Python 2.6 or logging.config for later versions
if sys.version_info < (2, 7):
    import logutils.dictconfig as logging_config
else:
    from logging import config as logging_config

import pkg_resources

APP_DESC = 'Command line tool for starting a Sprockets application'

DESCRIPTION = 'Available sprockets application controllers'

EPILOG = ('Find more Sprockets controllers and plugins at '
          'https://sprockets.readthedocs.org')

# Logging formatters
SYSLOG_FORMAT = ('%(levelname)s <PID %(process)d:%(processName)s> '
                 '%(name)s.%(funcName)s(): %(message)s')

VERBOSE_FORMAT = ('%(levelname) -10s %(asctime)s %(process)-6d '
                  '%(processName) -20s %(name) -20s '
                  '%(funcName) -20s L%(lineno)-6d: %(message)s')

# Base logging configuration
LOGGING = {'disable_existing_loggers': True,
           'filters': {},
           'formatters': {'syslog': {'format': SYSLOG_FORMAT},
                          'verbose': {'datefmt': '%Y-%m-%d %H:%M:%S',
                                      'format': VERBOSE_FORMAT}},
           'handlers': {'console': {'class': 'logging.StreamHandler',
                                    'formatter': 'verbose'},
                        'syslog': {'class': 'logging.handlers.SysLogHandler',
                                   'formatter': 'syslog'}},
           'incremental': False,
           'loggers': {'sprockets': {'handlers': ['console'],
                                     'level': logging.WARNING,
                                     'propagate': True}},
           'root': {'handlers': [],
                    'level': logging.CRITICAL,
                    'propagate': True},
           'version': 1}

LOGGER = logging.getLogger(__name__)


class CLI(object):
    """The core Sprockets CLI application providing argument parsing and
    logic for starting a controller.

    """
    CONTROLLERS = 'sprockets.controller'
    LOGGER = 'sprockets'
    PLUGINS = 'sprockets.plugin'

    def __init__(self):
        self._controllers = self._get_controllers()
        self._plugins = self._get_plugins()
        self.arg_parser = argparse.ArgumentParser(description=APP_DESC,
                                                  epilog=EPILOG)
        self._add_cli_args()
        self._args = self.arg_parser.parse_args()

    def run(self):
        """Evaluate the command line arguments, performing the appropriate
        actions so the application can be started.

        """
        # The apps command prevents any other processing of args
        if self._args.apps:
            if not self._controllers:
                print('ERROR: No application controllers installed\n')
                sys.exit(1)
            self._print_installed_apps(self._args.controller,
                                       self._args.as_json)
            sys.exit(0)

        # The plugins command prevents any other processing of args
        if self._args.plugins:
            self._print_installed_plugins(self._args.as_json)
            sys.exit(0)

        # Make sure the specified controller is valid
        if self._args.controller not in self._controllers:
            sys.stderr.write('ERROR: Controller "%s" not found\n' %
                             self._args.controller)
            sys.exit(-1)

        # Make sure the specified plugins are valid
        for plugin in self._args.enable:
            if plugin not in self._plugins:
                sys.stderr.write('ERROR: Plugin "%s" not found\n' % plugin)
                sys.exit(-1)

        # If app is not specified at this point, raise an error
        if not self._args.application:
            sys.stderr.write('ERROR: Application not specified\n\n')
            self.arg_parser.print_help()
            sys.exit(-1)

        # If it's a registered app reference by name, get the module name
        app_module = self._get_application_module(self._args.controller,
                                                  self._args.application)

        # Configure logging based upon the flags
        self._configure_logging(app_module,
                                self._args.verbose,
                                self._args.syslog)

        # Shortcut to the controller module
        controller = self._controllers[self._args.controller]

        # Try and run plugin initialization
        for plugin in self._args.enable:
            try:
                self._plugins[plugin].initialize(controller)
            except AttributeError:
                LOGGER.debug('Plugin %s.initialize() undefined', plugin)

        # Try and run the controller
        try:
            self._controllers[self._args.controller].main(app_module,
                                                          self._args)
        except TypeError as error:
            sys.stderr.write('ERROR: could not start the %s controller for %s'
                             ': %s\n' % (self._args.controller,
                                         app_module,
                                         str(error)))
            sys.exit(-1)

        # Try and run plugin initialization
        for plugin in self._args.enable:
            try:
                self._plugins[plugin].on_shutdown(controller)
            except AttributeError:
                LOGGER.debug('Plugin %s.on_shutdown() undefined', plugin)

    def _add_cli_args(self):
        """Add the cli arguments to the argument parser."""
        self.arg_parser.add_argument('--apps',
                                     action='store_true',
                                     help='List installed applications')

        self.arg_parser.add_argument('--plugins',
                                     action='store_true',
                                     help='List installed plugins')

        self.arg_parser.add_argument('--machine-readable',
                                     action='store_true',
                                     dest='as_json',
                                     help='Output application or plugin list '
                                          'as JSON')

        self.arg_parser.add_argument('-e', '--enable',
                                     action='append',
                                     metavar='PLUGIN',
                                     default=[],
                                     nargs="?",
                                     help='Enable a plugin')

        self.arg_parser.add_argument('-s', '--syslog',
                                     action='store_true',
                                     help='Log to syslog')

        self.arg_parser.add_argument('-v', '--verbose',
                                     action='count',
                                     help=('Verbose logging output, use -vv '
                                           'for DEBUG level logging'))

        self.arg_parser.add_argument('--version',
                                     action='version',
                                     version='sprockets v%s ' % __version__)

        # Controller sub-parser
        if '--plugins' not in sys.argv:
            subparsers = self.arg_parser.add_subparsers(dest='controller',
                                                        help=DESCRIPTION)

            # Iterate through the controllers and add their cli arguments
            for key in self._controllers:
                help_text = self._get_controller_help(key)
                sub_parser = subparsers.add_parser(key, help=help_text)
                try:
                    self._controllers[key].add_cli_arguments(sub_parser)
                except AttributeError:
                    LOGGER.debug('Controller %s.add_cli_arguments() undefined',
                                 key)

            # The application argument
            if '--apps' not in sys.argv:
                self.arg_parser.add_argument('application',
                                             metavar='APP',
                                             help='Application to run')

    def _configure_logging(self, application, verbosity=0, syslog=False):
        """Configure logging for the application, setting the appropriate
        verbosity and adding syslog if it's enabled.

        :param str application: The application module/package name
        :param int verbosity: 1 == INFO, 2 == DEBUG
        :param bool syslog: Enable the syslog handler

        """
        # Create a new copy of the logging config that will be modified
        config = dict(LOGGING)

        # Increase the logging verbosity
        if verbosity == 1:
            config['loggers'][self.LOGGER]['level'] = logging.INFO
        elif verbosity == 2:
            config['loggers'][self.LOGGER]['level'] = logging.DEBUG

        # Add syslog if it's enabled
        if syslog:
            config['loggers'][self.LOGGER]['handlers'].append('syslog')

        # Copy the sprockets logger to the application
        config['loggers'][application] = dict(config['loggers']['sprockets'])

        # Configure logging
        logging_config.dictConfig(config)

    def _get_application_module(self, controller, application):
        """Return the module for an application. If it's a entry-point
        registered application name, return the module name from the entry
        points data. If not, the passed in application name is returned.

        :param str controller: The controller type
        :param str application: The application name or module
        :rtype: str

        """
        for pkg in self._get_applications(controller):
            if pkg.name == application:
                return importlib.import_module(pkg.module_name)
        return importlib.import_module(application)

    @staticmethod
    def _get_applications(controller):
        """Return a list of application names for the given controller type
        that have registered themselves as sprockets applications.

        :param str controller: The type of controller for the applications
        :rtype: list

        """
        group_name = 'sprockets.%s.app' % controller
        return pkg_resources.iter_entry_points(group=group_name)

    @staticmethod
    def _get_argument_parser():
        """Return an instance of the argument parser.

        :return: argparse.ArgumentParser

        """
        return argparse.ArgumentParser()

    def _get_controllers(self):
        """Iterate through the installed controller entry points and import
        the modules, returning the dict to be assigned to the CLI._controllers
        dict.

        :return: dict

        """
        return self._get_package_resources(self.CONTROLLERS)

    def _get_controller_help(self, controller):
        """Return the value of the HELP attribute for a controller that should
        describe the functionality of the controller.

        :rtype: str|None

        """
        if hasattr(self._controllers[controller], 'HELP'):
            return self._controllers[controller].HELP
        return None

    @staticmethod
    def _get_package_resources(group):
        """Iterate through the installed entry points for the specified group,
        importing each package, returning a dict of handles by package name.

        :return: dict

        """
        packages = dict()
        for pkg in pkg_resources.iter_entry_points(group=group):
            packages[pkg.name] = importlib.import_module(pkg.module_name)
        return packages

    def _get_plugins(self):
        """Iterate through the installed plugin entry points and import
        the modules, returning the dict to be assigned to the CLI._plugins
        dict.

        :return: dict

        """
        return self._get_package_resources(self.PLUGINS)

    def _print_installed_apps(self, controller, as_json):
        """Print out a list of installed sprockets applications

        :param str controller: The name of the controller to get apps for
        :param bool as_json: Output the data as json


        """
        if as_json:
            apps = [app.name for app in self._get_applications(controller)]
            print(json.dumps({controller: apps}))
            return
        print('Installed Sprockets {0} Apps\n'.format(controller.upper()))
        print("{0:<25} {1:>25}".format('Name', 'Module'))
        print(string.ljust('', 51, '-'))
        for app in self._get_applications(controller):
            print('{0:<25} {1:>25}'.format(app.name,
                                           '({0})'.format(app.module_name)))
        print('')

    def _print_installed_plugins(self, as_json):
        """Print out a list of installed plugin packages

        :param bool as_json: Output the data as json

        """
        if as_json:
            print(json.dumps({'plugins': [p.name for p in self._plugins]}))
            return
        if not self._plugins:
            print('There are no plugins installed\n')
            return
        print('Installed Sprockets Plugins\n')
        print("{0:<25} {1:>25}".format('Name', 'Module'))
        print(string.ljust('', 51, '-'))
        for loader in self._plugins:
            print('{0:<25} {1:>25}'.format(loader.name,
                                           '({0})'.format(loader.module_name)))
        print('')


def main():
    """Main application runner"""
    cli = CLI()
    cli.run()
