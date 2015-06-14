"""
ppy.pip
~~~~~~~

Patches pip to work with ppy packages.
"""

from __future__ import absolute_import, print_function

import os
import io
import json
from tempfile import NamedTemporaryFile, mkstemp
from collections import OrderedDict
from types import ModuleType

import pip

from .imports import try_import
from .resolver import (requirements_filename, site_packages_dirname,
                       resolve_package_path)


Command = try_import('pip.basecommand.Command', 'pip.commands.Command')
BaseInstallCommand = try_import('pip.commands.install.InstallCommand')


try:
    input = raw_input
except NameError:
    pass


class InitCommand(Command):
    """
    Initializes a new ppy package.
    """
    name = 'init'

    usage = """
      %prog [options]"""

    summary = 'Initializes a new ppy package.'
    bundle = False

    def run(self, options, args):
        print('This utility will walk you through creating a '
              'requirements.json file.')
        print('It only covers the most common items, and tries to guess '
              'sane defaults.')
        print()

        # TODO: Add this option
        print('See `pip help json` for definitive documentation on these '
              'fields')
        print('and exactly what they do.')
        print()

        print('Use `pip install <pkg> --save` afterwards to install a'
              'package and')
        print('save it as a dependency in the requirements.json file.')
        print()

        # TODO: Convert to ppy package if setup.py or requirements.txt is found

        # Read existing file, if exists
        data = {}
        try:
            data = _load_requirements()
        except (IOError, ValueError):
            pass

        name = os.path.basename(os.getcwd())

        # Set sensible defaults
        data.setdefault('name', name)
        data.setdefault('version', '1.0.0')
        data.setdefault('main', '{}.py'.format(name))  # TODO: Slugify?
        # TODO: Set git repo if within one?
        # TODO: Set sane keywords based on name and README if found
        # TODO: Set author to last git committer, if within a repo?
        # TODO: Use 'License :: OSI Approved :: MIT License' classifier instead
        data.setdefault('license', 'MIT')
        # TODO: platform?
        # TODO: 'Operating System :: OS Independent' classifier?

        # Prompt user
        _prompt(data, 'name')
        _prompt(data, 'version')
        _prompt(data, 'description')
        _prompt(data, 'main', 'entry point')
        _prompt(data, 'scripts/test', 'test command', keep_empty=False)
        _prompt(data, 'repository/url', 'git repository', keep_empty=False)
        _prompt(data, 'keywords', keep_empty=False)
        _prompt(data, 'author')
        _prompt(data, 'license')

        # TODO: Validate name and version?

        # Transform data paths
        test_script = data.pop('scripts/test', None)
        if test_script:
            scripts = _upsert(data, 'scripts', {})
            scripts['test'] = test_script
        repository_url = data.pop('repository/url', None)
        if repository_url:
            repository = _upsert(data, 'repository', {})
            repository['type'] = 'git'
            repository['url'] = repository_url

        # Sort fields
        data = _sorted_dict(data, [
            'name', 'version', 'description', 'main', 'scripts', 'repository',
            'keywords', 'author', 'license',
        ])

        # Confirm
        filename = os.path.abspath(requirements_filename)
        contents = unicode(json.dumps(data, indent=4, ensure_ascii=False,
                                      encoding='utf8') + '\n')
        print('About to write to {}:'.format(filename))
        print()
        print(contents)
        ok = input('Is this ok? (yes) ').lower().strip()
        if ok and not ok.startswith('y'):
            print('Aborted.')
            return

        # Write file
        with io.open(filename, mode='w', encoding='utf8') as f:
            f.write(unicode(contents))


class InstallCommand(BaseInstallCommand):
    def __init__(self, *args, **kw):
        super(InstallCommand, self).__init__(*args, **kw)

        self.initial_args = None

        cmd_opts = self.cmd_opts

        cmd_opts.add_option(
            '-g', '--global',
            dest='global_install',
            action='store_true',
            help='Install globally (this is the default pip behavior outside '
                 'of a ppy package)')

    def main(self, args):
        self.initial_args = args
        return super(InstallCommand, self).main(args)

    def run(self, options, args):
        # Run pip normally if no local site-packages is found
        # TODO: Get this from `pip install dir/file` or from some argument?
        root_path = os.path.abspath(os.getcwd())
        package_path = resolve_package_path(root_path)
        if not package_path:
            return super(InstallCommand, self).run(options, args)

        site_packages_path = os.path.join(package_path, site_packages_dirname)
        requirements_path = os.path.join(package_path, requirements_filename)

        # TODO: Handle --global flag
        local_install = False
        if options.target_dir is None:
            local_install = True
            # Use global when requirements.txt has the 'ppy' switch
            if options.requirements and len(options.requirements) == 1:
                requirements_file = options.requirements[0]
                try:
                    requirements = _read(requirements_file)
                    # TODO: Use os.path.dirname(requirements_file)?
                    # TODO: Check for 'ppy' package directly?
                    if requirements.strip() == 'useppy':
                        options.requirements = []
                    # TODO: Keep this?
                    if requirements.strip() == '.':
                        # TODO: Check setup.py for 'ppy'
                        local_install = False
                except IOError:
                    pass

        if local_install:
            options.target_dir = site_packages_path

        # TODO: pip install <package>           -- contextual local install
        # TODO: pip install -g <package>        -- contextual global install
        # TODO: pip install -r requirements.txt -- contextual explicit install
        # TODO: Recursively install ppy packages
        # TODO: pip help install adjustments

        temp_file = None
        try:
            # TODO: Better check
            #if not self.initial_args:
            if not args and not options.requirements:
                requirements_json = _load_requirements()
                dependencies = requirements_json.get('dependencies')
                if dependencies:
                    temp_file, temp_filename = mkstemp(
                        prefix='requirements-', suffix='.txt', text=True)
                    requirements = _dependencies_to_requirements(dependencies)
                    os.write(temp_file, '\n'.join(requirements))
                    options.requirements.append(temp_filename)
            return super(InstallCommand, self).run(options, args)
        finally:
            if temp_file:
                os.close(temp_file)


def _read(filename):
    with io.open(filename, 'r', encoding='utf8') as f:
        return f.read()


def _prompt(data, field, title=None, keep_empty=True):
    message = '{}: '.format(title or field)
    value = data.get(field)
    if value:
        message += '({}) '.format(value)
    value = input(message)
    if value or (not data.get(field) and keep_empty):
        data[field] = value


def _upsert(data, field, value):
    if field not in data:
        data[field] = value
    return value


def _sorted_dict(data, keys):
    ordered = OrderedDict()
    for key in keys + list(data.keys()):
        if key in data and key not in ordered:
            ordered[key] = data[key]
    return ordered


def _load_requirements():
    with io.open(requirements_filename, encoding='utf8') as f:
        return json.load(f)


def _dependencies_to_requirements(dependencies):
    requirements = []
    for package, semver in dependencies.items():
        # TODO: Translate semver to python versions
        if semver.startswith('^'):
            version = semver[1:]
        if semver.startswith('~'):
            version = semver[1:]
        else:
            version = semver
        version = '==' + version
        requirements.append(package + version)
    return requirements


def patch():
    commands = (pip.commands.commands_dict
                if hasattr(pip.commands, 'commands_dict')
                else pip.commands)
    commands['init'] = InitCommand
    # TODO: Only install this when site-packages is present
    commands['install'] = InstallCommand
    # TODO: pip update  (or 'upgrade'?)
    # TODO: pip help json
