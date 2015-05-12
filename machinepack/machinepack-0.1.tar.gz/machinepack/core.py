# -*- coding: utf-8 -*-

import os
import sys
import importlib

import click
import coverage as Coverage
from mako.template import Template

from machinepack.tests import execute_machinetest
from machinepack.pack import MachinePackManager
from machinepack.helpers import render


class MachinePackViewer(MachinePackManager):

    @classmethod
    def generate_template(cls, filename, params):
        template_file = os.path.join(os.path.dirname(__file__), 'templates/%s' % filename)
        return Template(filename=template_file).render(**params)


    @classmethod
    def create_files(cls, paths):

        for path in paths:
            for filename_key in paths[path]:
                filename = "%s/%s" % (path, filename_key)
                content = MachinePackViewer.generate_template(*paths[path][filename_key])
                with open(filename, "a+") as new_file:
                    new_file.write(content)

    def get_source(self, machine):
        return open('%s/%s.py' % (self.package_config['name'], machine)).read()

    def generate_machine(self, name):

        module_path = self.machinepack_name

        paths = {
            module_path: {
                name + '.py': ('machine.mako', {}),
                name + '_test.py': ('machine_test.mako', {})
            }
        }
        MachinePackViewer.create_files(paths)


    def generate_example(self, machine_name):

        # make decorator
        if machine_name not in self.machines_list:
            click.echo('Invalid machine name!')
            return

        config = self.get_machine_meta(machine_name)

        params = {
            'machinepack_name': self.package_config['name'],
            'machinepack_description': config['description'],
            'machinepack_class': self.machine_class,
            'machine_name': machine_name,
            'inputs': config['inputs'],
            'exits': config['exits'],
        }

        template_file = os.path.join(os.path.dirname(__file__), 'templates/example.mako')
        return Template(filename=template_file).render(**params)

    def check_machine_path(self, name):
        path = 'machinepack_%s' % name
        if os.path.exists(path):
            self.echo.warning("Folder '%s' already exist!" % path)
            sys.exit(1)

    def create_basic_structure(self, params):

        name = params['machinepack_name']
        class_name = name.title()

        top_level_path = 'machinepack_' + name
        module_path = top_level_path + '/machinepack_%s' % name

        # create directory structure
        os.makedirs(module_path)

        paths = {
            top_level_path: {
                "setup.py": ('setup.mako', params),
                ".gitignore": ('gitignore.mako', {}),  # TODO: empty params?
                "tox.ini": ('tox.mako', {}),
                ".travis.yml": ('travis.mako', {}),
            },
            module_path: {
                "__init__.py": ('init.mako', {'class_name': class_name}),
                "config.py": ('config.mako', params),
                "hello.py": ('hello.mako', {}),
                "hello_test.py": ('hello_test.mako', {})
            }
        }
        MachinePackViewer.create_files(paths)

    def exec_machine(self, name):
        click.echo('')
        click.echo('Testing: %s' % name)
        machine_meta = self.get_machine_meta(name)

        params = {}
        for input_arg in machine_meta['inputs']:
            value = click.prompt("Value of '%s'" % input_arg)
            params[input_arg] = value

        resp = self.__getattr__(name)(params)

        print render('exec', {'response': resp.name, 'response_args': resp[resp.name]})

    def make_tests(self, machine_name=None, coverage=True):

        if machine_name:
            if machine_name not in self.machines_list:
                click.echo('Invalid machine name!')
                sys.exit(1)
            machines_list = [machine_name]
        else:
            machines_list = self.machines_list

        if coverage:
            cov = Coverage.coverage(omit=["*_test.py", "*__init__.py"])
            cov.start()
            cov.exclude('^meta')

        for machine_name in machines_list:
            tests = importlib.import_module('%s.%s_test' % (self.package_config['name'], machine_name)).tests
            func = self.__getattr__(machine_name)

            click.echo()
            click.secho("Testing: ", nl=False)
            click.secho(machine_name, fg='cyan')
            click.echo('-' * 20)

            for test in tests:
                click.secho("    ", nl=False)
                click.secho('⚬ ' + test['description'] + '... ', bold=True, nl=False)

                resp = execute_machinetest(func, test)

                if resp == True:
                    click.secho('✔', fg='green')
                else:
                    click.secho('✘', fg='red')
                    print resp
        print ""

        if coverage:
            cov.stop()
            cov.save()
            cov.report()

        return ""
