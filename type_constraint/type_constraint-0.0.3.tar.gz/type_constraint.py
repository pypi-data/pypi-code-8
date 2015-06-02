import collections
import types
import re
import inspect
import pprint

__authors__ = ["timchow"]
__version__ = '0.0.3'

def parameter_binding(f, *a, **kw):
    argspec = inspect.getargspec(f)

    binding_result = {}
    unbinding_args = []
    for arg in argspec.args:
        if arg in kw:
            binding_result[arg] = kw.pop(arg)
        else:
            unbinding_args.append(arg)
    binding_result.update(dict(zip(unbinding_args, a)))
    default_parameters = dict(zip(argspec.args[::-1], argspec.defaults[::-1])) \
                            if argspec.defaults else {}
    default_parameters.update(binding_result)
    return default_parameters, kw

def gen_builtin_name2type():
    d = {}
    for attr in dir(types):
        type_ = getattr(types, attr)
        if not (attr.endswith('Type') and isinstance(type_, type)):
            continue
        d[attr] = type_
        if hasattr(type_, '__name__'):
            d[type_.__name__] = type_

    for attr, type_ in types.__builtins__.items():
        if not isinstance(type_, type):
            continue
        d[attr] = type_
    return d
BUILTIN_NAME2TYPE = gen_builtin_name2type()

def print_name2type():
    pprint.pprint(BUILTIN_NAME2TYPE) 

class Check:
    def __init__(self, *a, **kw):
        self._name2type = {}
        for e in [ele for ele in a if isinstance(ele, collections.Mapping)]:
            self._name2type.update(e)
        self._name2type.update(kw)
        self._name2type.update(BUILTIN_NAME2TYPE)

    def _extract(self, dc):
        assert isinstance(dc, basestring), 'param:dc should be `basestring\', not' \
                    '`%s\'' % type(dc)

        constract = []
        for line in dc.split('\n'):
            line = line.strip()
            if line.startswith('@'):
                name, args = re.match(r'@(\w+)\s*(.*)', line).groups()
                args = re.split(r'\s+', args)
                constract.append([name, args])
        return constract

    def check_params(self, constract, f, *a, **kw):
        binding_result, keywords = parameter_binding(f, *a, **kw)
        for name, args in constract:
            if name != 'param' or len(args) < 2 or \
                args[0] not in binding_result or \
                args[1] not in self._name2type:
                continue
            if not isinstance(binding_result[args[0]], self._name2type[args[1]]):
                raise TypeError('argument:%s should be %s, not %s.' 
                    % (args[0], self._name2type[args[1]], type(binding_result[args[0]])))

    def check_exception(self, constract, e):
        pass

    def check_result(self, constract, result):
        for name, args in constract:
            if name != 'return' or len(args) < 1 or \
                args[0] not in self._name2type:
                continue
            if not isinstance(result, self._name2type[args[0]]):
                raise TypeError('return value should be %s, not %s.' %(
                        self._name2type[args[0]], type(result)))

    def __call__(self, f):
        constract = self._extract(f.__doc__) if f.__doc__ else []
        def inner(*a, **kw):
            self.check_params(constract, f, *a, **kw)
            try:
                result = f(*a, **kw)
            except Exception as e:
                self.check_exception(constract, e)
                raise
            else:
                self.check_result(constract, result)
                return result
        return inner

def CheckMeta(*args, **kwargs):
    def __inner(cls_name, bases, attrs):
        for attr in attrs:
            if isinstance(attrs[attr], types.FunctionType):
                attrs[attr] = Check(*args, **kwargs)(attrs[attr])
        return type(cls_name, bases, attrs)
    return __inner

BasicCheck = Check()

