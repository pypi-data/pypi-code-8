""" Main module that exposes an interface to control the PYTHONPATH environment variable for
    code in development.
"""
__author__ = 'Ian Davis'

import json
import sys

import config
import os_util


home_directory = os_util.home_directory()
DEFAULT_CONFIGURATION_FILEPATH = os_util.make_path(home_directory, 'dev_environment.cfg')


class EnvironmentConfiguration(config.Configuration):
    """ Provides configuration file support for environment manager.
    INI File format should look as follows:
    [paths]
    workspace_path = C:\path\to\workspace\
    branch_name = branch-2-second-printer

    [directories]
    subdirectories = [
            "ScaleManagement",
            "ScaleManagement\\source",
            "Windux\\Application\\shared\\sessionHandler\\python",
            "Windux\\Application\\shared\\util\\licensing",
            "Windux\\Application\\shared\\util\\dongleKey",
            ...
        }

    """
    def __init__(self, file_path):
        self.default_path_values = {'workspace_path': os_util.home_directory(),
                                    'branch_name': 'branch-2-second-printer'}

        default_directories = (r'ScaleManagement',
                               r'ScaleManagement\source',
                               r'Windux\Application\shared\sessionHandler\python',
                               r'Windux\Application\shared\util\licensing',
                               r'Windux\Application\shared\util\dongleKey')
        self.default_directory_values = {'subdirectories': json.dumps(default_directories, indent=4)}
        self.default_sections = {'paths': self.default_path_values,
                                 'directories': self.default_directory_values}

        super(EnvironmentConfiguration, self).__init__(file_path)

    def _verify_section_integrity(self):
        """ Verify that all sections and their default options exist in the configuration file. """

        needs_rewrite = False

        for section_name, options in self.default_sections.iteritems():
            if section_name not in self.sections:
                self.add_section(name=section_name, options=options)
                needs_rewrite = True
                continue

            section = self.sections[section_name]

            for option_name, option_value in options.iteritems():
                if option_name not in section.options:
                    needs_rewrite = True
                    section.options[option_name] = option_value

        if needs_rewrite:
            self.write()

    def _setup_default_sections(self):
        """ Setup all default sections and their values for a first init. """

        for section_name, options in self.default_sections.iteritems():
            self.add_section(name=section_name, options=options)


def setup(configuration_filepath=DEFAULT_CONFIGURATION_FILEPATH):
    environment_configuration = EnvironmentConfiguration(configuration_filepath)
    workspace_path = environment_configuration['paths']['workspace_path']
    branch_name = environment_configuration['paths']['branch_name']
    branch_path = os_util.make_path(workspace_path, branch_name)
    sub_directories = json.loads(environment_configuration['directories']['subdirectories'])

    for sub_directory in sub_directories:
        environment_path = os_util.make_path(branch_path, sub_directory)
        sys.path.append(environment_path)
