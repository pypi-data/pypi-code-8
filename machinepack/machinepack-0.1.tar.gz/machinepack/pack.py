# -*- coding: utf-8 -*-

import os
import sys
import importlib
import glob
import types

from machinepack.exceptions import InvalidArgument, MissingArgument


class MockCallable(object):
    """Mocks a function, can be enquired on how many calls it received"""

    def __init__(self, result):
        self.result = result
        self._calls = []

    def __call__(self, *arguments):
        """Mock callable"""
        self._calls.append(arguments)
        return self.result

    def called(self):
        """docstring for called"""
        return self._calls


class StubModule(types.ModuleType, object):
    """Uses a stub instead of loading libraries"""

    def __init__(self, module_name):
        self.__name__ = module_name
        sys.modules[module_name] = self

    def __repr__(self):
        name = self.__name__
        mocks = ', '.join(set(dir(self)) - set(['__name__']))
        return "<StubModule: %(name)s; mocks: %(mocks)s>" % {'name': name, 'mocks': mocks}


class MockResult(object):
    def __init__(self, **initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])


class Pack(object):
    resp = MockResult

    def __init__(self, config, mocks=None):
        self.config = config
        self.mocks = mocks


    def require(self, module_name):
        if self.mocks:
            module = StubModule(module_name)

            for mock in self.mocks:
                mock_module_name, method = mock.split('.')
                if mock_module_name == module.__name__:
                    module.__setattr__(method, MockCallable(self.mocks[mock]))
            return module
        else:
            return importlib.import_module(module_name)


class MachineResponse(object):
    def __init__(self, name, **args):

        # Here validating responses against meta
        self.name = name
        self.args = args
        self.__setattr__(name, args)

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            return None

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __str__(self):
        return "Response:\n" \
               "\t%s\n" \
               "Response params:\n" \
               "\t%s\n" % (self.name, self.args)


class MachinePackConfig(dict):
    """Dictionary with global config options"""


class MachinePackManager(object):
    def __init__(self, directory=None):

        self.directory = directory
        if directory:
            self.directory = os.path.join(self.directory, os.pardir)
        else:
            self.directory = os.path.join(os.getcwd())

        self.modules_directory = os.path.join(os.getcwd(), os.path.basename(os.getcwd()))

        self.methods = {}

        self.config = MachinePackConfig()

        self.initialization = False

        sys.path.insert(0, '.')
        self.machinepack_name = os.path.basename(self.directory)

        try:
            self.package_config = importlib.import_module('%s.config' % self.machinepack_name).CONFIG
            self.machinepack_config = self.package_config['machinepack_config']
            self.machine_class = self.package_config['name'].split('_')[1].title()

            modules = glob.glob(self.modules_directory + "/*.py")
            modules = [module for module in modules if '_test.' not in module and 'config.' not in module]

            self.machines_list = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f).startswith('_')]

            self._dir = self.machines_list
            self.initialization = True
        except Exception as e:
            pass
            # print "WARNING:", e.message

    def __dir__(self):
        self._dir.append('config')
        return self._dir

    def __getattr__(self, item):
        if item in ['set', 'initialization']:
            return self.__getattribute__(item)

        machine_name = item
        imported_module = importlib.import_module('%s.%s' % (os.path.basename(self.directory), machine_name))
        final_func = imported_module.func

        def proxy_func(params=None, mocks=None, **args):

            if isinstance(params, dict):
                args = params

            MachinePackManager._validate_input(args, imported_module.meta)
            pack = Pack(self.config, mocks=mocks)
            return final_func(args, MachineResponse, pack)

        proxy_func.__name__ = str('proxy_%s' % item)
        return proxy_func

    @classmethod
    def _validate_input(cls, params, meta):
        meta_inputs = meta['inputs']
        for arg in params:
            if arg not in meta_inputs:
                raise InvalidArgument('Invalid argument: %s' % arg)

        for arg in meta_inputs:
            if meta_inputs[arg].get('required', None) and arg not in params:
                raise MissingArgument('Missing argument: %s' % arg)

    def get_machine_meta(self, machine):
        if machine not in self.machines_list:
            return None
        return importlib.import_module('%s.%s' % (self.package_config['name'], machine)).meta

    def set(self, name, value):
        if name not in self.machinepack_config:
            raise InvalidArgument('Invalid config argument: %s' % name)
        self.config['name'] = value
