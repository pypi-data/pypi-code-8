"""
    pyrx
    ~~~~

    Python implementation of the Rx schema and validation system
    http://rx.codesimply.com/

    Forked from the main rx github repo (https://github.com/rjbs/rx) Nov 25 '13
    because the python implementation deserves its own place and testin and
    stuff.

    The copyright line of the license for the rx repository reads:
    The contents of the Rx repository are copyright (C) 2008, Ricardo SIGNES.

    The license itself is GPL2: https://github.com/rjbs/rx/blob/master/LICENSE
"""

from __future__ import print_function
import re
import sys
import types

core_types = []

if sys.version_info[0] == 2:
    string_types = (str, unicode)
    num_types = (float, long, int)
else:
    string_types = (str,)
    num_types = (float, int)


class Result():
    def __init__(self, valid, message):
        self.valid = valid
        self.message = message

    def __bool__(self):
        return self.valid
    __nonzero__ = __bool__


class RxError(Exception):
    pass


class Util(object):
    @staticmethod
    def make_range_check(opt):
        range = {}
        for entry in opt.keys():
            if entry not in ('min', 'max', 'min-ex', 'max-ex'):
                raise ValueError("illegal argument to make_range_check")

            range[entry] = opt[entry]

        def check_range(value, explain=False):
            if range.get('min') is not None and value < range['min']:
                return Result(False, str(value) + ": too low")
            if range.get('min-ex') is not None and value <= range['min-ex']:
                return Result(False, str(value) + ": less than or equal min-ex")
            if range.get('max-ex') is not None and value >= range['max-ex']:
                return Result(False, str(value) + ": greater than or equal max-ex")
            if range.get('max') is not None and value > range['max']:
                return Result(False, str(value) + ": greater than man")
            return Result(True, "All Good")

        return check_range


def _get_logger(trace):
    def log(frame, event, arg):
        if event == 'return' and arg is False:
            message = "False "
            context = frame.f_locals
            if 'self' in context and hasattr(context['self'], 'subname'):
                message += ' while checking {}'.format(context['self'].subname())
            elif 'self' in context and hasattr(context['self'], 'uri'):
                message += ' while checking {}'.format(context['self'].uri())
            if 'value' in context:
                message += ', value {}'.format(context['value'])
            trace.append(message)
        #debug print frame.f_lineno, event, arg, frame.f_locals
        return log
    return log


def trace_wrap(type_class):
    class TracedType(type_class):
        def __init__(self, *args, **kwargs):
            super(TracedType, self).__init__(*args, **kwargs)
            self.trace = []

        def check(self, value, *args, **kwargs):
            self.trace = []

            result = super(TracedType, self).check(value, *args, **kwargs)
            if not result:
                sys.settrace(_get_logger(self.trace))
                super(TracedType, self).check(value, *args, **kwargs)
                sys.settrace(None)

            return result

    return lambda *args, **kwargs: TracedType(*args, **kwargs)


class Factory(object):
    def __init__(self, opt={}):
        self.prefix_registry = {
            '': 'tag:codesimply.com,2008:rx/core/',
            '.meta': 'tag:codesimply.com,2008:rx/meta/',
        }

        self.type_registry = {}
        if opt.get("register_core_types", False):
            for t in core_types:
                self.register_type(t)

    @staticmethod
    def _default_prefixes():
        pass

    def expand_uri(self, type_name):
        if re.match('^\w+:', type_name):
            return type_name

        m = re.match('^/([-._a-z0-9]*)/([-._a-z0-9]+)$', type_name)

        if not m:
            raise RxError("couldn't understand type name '%s'" % type_name)

        if not self.prefix_registry.get(m.group(1)):
            raise RxError("unknown prefix '%s' in type name '%s'" %
                          (m.group(1), type_name))

        return '%s%s' % (self.prefix_registry[m.group(1)], m.group(2))

    def add_prefix(self, name, base):
        if self.prefix_registry.get(name, None):
            raise RxError("the prefix '%s' is already registered" % name)

        self.prefix_registry[name] = base

    def register_type(self, t):
        t_uri = t.uri()

        if self.type_registry.get(t_uri, None):
            raise ValueError("type already registered for %s" % t_uri)

        self.type_registry[t_uri] = t

    def learn_type(self, uri, schema):
        if self.type_registry.get(uri, None):
            raise RxError("tried to learn type for already-registered uri %s"
                          % uri)

        # make sure schema is valid
        # should this be in a try/except?
        self.make_schema(schema)

        self.type_registry[uri] = {"schema": schema}

    def make_schema(self, schema, trace=False):
        if isinstance(schema, string_types):
            schema = {"type": schema}

        if not isinstance(schema, dict):
            raise RxError('invalid schema argument to make_schema')

        uri = self.expand_uri(schema["type"])

        if not self.type_registry.get(uri):
            raise RxError("unknown type %s" % uri)

        type_class = self.type_registry[uri]
        if trace:
            type_class = trace_wrap(type_class)

        if isinstance(type_class, dict):
            if not set(schema.keys()) <= set(['type']):
                raise RxError('composed type does not take check arguments')
            return self.make_schema(type_class["schema"])
        else:
            return type_class(schema, self)


class _CoreType(object):
    @classmethod
    def uri(self):
        return 'tag:codesimply.com,2008:rx/core/' + self.subname()

    def __init__(self, schema, rx):
        if not set(schema.keys()) <= set(['type']):
            raise RxError('unknown parameter for //%s' % self.subname())

    def check(self, value):
        return Result(False, "Core type error")


class AllType(_CoreType):
    @staticmethod
    def subname():
        return 'all'

    def __init__(self, schema, rx):
        if not set(schema.keys()) <= set(('type', 'of')):
            raise RxError('unknown parameter for //all')

        if not(schema.get('of') and len(schema.get('of'))):
            raise RxError('no alternatives given in //all of')

        self.alts = [rx.make_schema(s) for s in schema['of']]

    def check(self, value):
        for schema in self.alts:
            if (not schema.check(value)):
                return Result(False, str(value) + ": All type error")
        return Result(True, "All Good")


class AnyType(_CoreType):
    @staticmethod
    def subname():
        return 'any'

    def __init__(self, schema, rx):
        self.alts = None

        if not set(schema.keys()) <= set(('type', 'of')):
            raise RxError('unknown parameter for //any')

        if schema.get('of') is not None:
            if not schema['of']:
                raise RxError('no alternatives given in //any of')
            self.alts = [rx.make_schema(alt) for alt in schema['of']]

    def check(self, value):
        if self.alts is None:
            return Result(True, "All Good")

        for alt in self.alts:
            if alt.check(value):
                return Result(True, "All Good")

        return Result(False, str(value) + ": AnyType error")


class ArrType(_CoreType):
    @staticmethod
    def subname():
        return 'arr'

    def __init__(self, schema, rx):
        self.length = None

        if not set(schema.keys()) <= set(('type', 'contents', 'length')):
            raise RxError('unknown parameter for //arr')

        if not schema.get('contents'):
            raise RxError('no contents provided for //arr')

        self.content_schema = rx.make_schema(schema['contents'])

        if schema.get('length'):
            self.length = Util.make_range_check(schema["length"])

    def check(self, value):
        if not isinstance(value, (list, tuple)):
            return Result(False, str(value) + ": Not a list or tuple")
        if self.length and not self.length(len(value)):
            return Result(False, str(value) + ": incorrect length")

        for item in value:
            content_schema_result = self.content_schema.check(item)
            if not content_schema_result:
                return Result(False, content_schema_result.message + "\n ArrType error in: " + str(item))

        return Result(True, "All Good")


class BoolType(_CoreType):
    @staticmethod
    def subname():
        return 'bool'

    def check(self, value):
        if value is True or value is False:
            return Result(True, "All Good")
        return Result(False, str(value) + ": not a bool")


class DefType(_CoreType):
    @staticmethod
    def subname():
        return 'def'

    def check(self, value):
        return Result(not(value is None), str(value) + ": DefType???")


class FailType(_CoreType):
    @staticmethod
    def subname():
        return 'fail'

    def check(self, value):
        return Result(False, "Fail type is fail")


class IntType(_CoreType):
    @staticmethod
    def subname():
        return 'int'

    def __init__(self, schema, rx):
        if not set(schema.keys()) <= set(('type', 'range', 'value')):
            raise RxError('unknown parameter for //int')

        self.value = None
        if 'value' in schema:
            if not isinstance(schema['value'], num_types) or \
               isinstance(schema['value'], bool):
                raise RxError('invalid value parameter for //int')
            if schema['value'] % 1 != 0:
                raise RxError('invalid value parameter for //int')
            self.value = schema['value']

        self.range = None
        if 'range' in schema:
            self.range = Util.make_range_check(schema["range"])

    def check(self, value):
        if not isinstance(value, num_types) or isinstance(value, bool):
            return Result(False, str(value) + ": Int type error")
        if value % 1 != 0:
            return Result(False, str(value) + ": not an int")
        if self.range and not self.range(value):
            return Result(False, str(value) + ": int range problem")
        if (not self.value is None) and value != self.value:
            return Result(False, str(value) + ": int value problem")
        return Result(True, "All Good")


class MapType(_CoreType):
    @staticmethod
    def subname():
        return 'map'

    def __init__(self, schema, rx):
        self.allowed = set()

        if not set(schema.keys()) <= set(('type', 'values')):
            raise RxError('unknown parameter for //map')

        if not schema.get('values'):
            raise RxError('no values given for //map')

        self.value_schema = rx.make_schema(schema['values'])

    def check(self, value):
        if not isinstance(value, dict):
            return Result(False, str(value) + ": not a dict")

        for v in value.values():
            value_schema_result = self.value_schema.check(v)
            if not value_schema_result:
                return Result(False, value_schema_result.message + "\n Map type error with " + str(v))

        return Result(True, "All Good")


class NilType(_CoreType):
    @staticmethod
    def subname():
        return 'nil'

    def check(self, value):
        return Result(value is None, str(value) + ": NilType???")


class NumType(_CoreType):
    @staticmethod
    def subname():
        return 'num'

    def __init__(self, schema, rx):
        if not set(schema.keys()) <= set(('type', 'range', 'value')):
            raise RxError('unknown parameter for //num')

        self.value = None
        if 'value' in schema:
            if not isinstance(schema['value'], num_types) or \
               isinstance(schema['value'], bool):
                raise RxError('invalid value parameter for //num')
            self.value = schema['value']

        self.range = None

        if schema.get('range'):
            self.range = Util.make_range_check(schema["range"])

    def check(self, value):
        if not isinstance(value, num_types) or isinstance(value, bool):
            return Result(False, str(value) + ": not a Numtype")
        if self.range and not self.range(value):
            return Result(False, str(value) + ": Num not in range")
        if (not self.value is None) and value != self.value:
            return Result(False, str(value) + ": wrong Num value")
        return Result(True, "All Good")


class OneType(_CoreType):
    @staticmethod
    def subname():
        return 'one'

    def check(self, value):
        if isinstance(value, num_types + string_types + (bool,)):
            return Result(True, "All Good")

        return Result(False, str(value) + ": wrong OneType")


class RecType(_CoreType):
    @staticmethod
    def subname():
        return 'rec'

    def __init__(self, schema, rx):
        if not set(schema.keys()) <= \
                set(('type', 'rest', 'required', 'optional')):
            raise RxError('unknown parameter for //rec')

        self.known = set()
        self.rest_schema = None
        if schema.get('rest'):
            self.rest_schema = rx.make_schema(schema['rest'])

        for which in ('required', 'optional'):
            self.__setattr__(which, {})
            for field in schema.get(which, {}).keys():
                if field in self.known:
                    raise RxError('%s appears in both required and optional' %
                                  field)

                self.known.add(field)

                self.__getattribute__(which)[field] = rx.make_schema(
                    schema[which][field]
                )

    def check_required_keys(self, value, keys):
        for field in keys:
            if field not in value:
                return Result(False, str(value) + ": required key error")
            required_keys_result = self.required[field].check(value[field])
            if not required_keys_result:
                return Result(False, required_keys_result.message + "\n required keys error. \nfield:" + str(field))
        return True

    def check_optional_keys(self, value, keys):
        for field in keys:
            if field not in value:
                continue
            optional_field_result = self.optional[field].check(value[field])
            if not optional_field_result:
                return Result(False, optional_field_result.message + "\n optional field error: " + str(field))
        return True

    def check_unknown_keys(self, value, keys):
        unknown = []
        for field in keys:
            if not field in self.known:
                unknown.append(field)

        if len(unknown) and not self.rest_schema:
            return Result(False, str(value) + "unknown key error")

        if len(unknown):
            rest = {}
            for field in unknown:
                rest[field] = value[field]
            rest_schema_result = self.rest_schema.check(rest)
            if not rest_schema_result:
                return Result(False, rest_schema_result.message + "\n unknown key error with: " + str(rest))
        return True

    def check(self, value):
        if not isinstance(value, dict):
            return Result(False, str(value) + ": not a Dict")

        unknown_keys = self.check_unknown_keys(value, value.keys())
        if not unknown_keys:
            return unknown_keys

        req_keys = self.check_required_keys(value, self.required.keys())
        if not req_keys:
            return req_keys

        optional_keys = self.check_optional_keys(value, self.optional.keys())
        if not optional_keys:
            return optional_keys

        return Result(True, "All good")


class SeqType(_CoreType):
    @staticmethod
    def subname():
        return 'seq'

    def __init__(self, schema, rx):
        if not set(schema.keys()) <= set(('type', 'contents', 'tail')):
            raise RxError('unknown parameter for //seq')

        if not schema.get('contents'):
            raise RxError('no contents provided for //seq')

        self.content_schema = [rx.make_schema(s) for s in schema["contents"]]

        self.tail_schema = None
        if (schema.get('tail')):
            self.tail_schema = rx.make_schema(schema['tail'])

    def check(self, value):
        if not isinstance(value, (list, tuple)):
            return Result(False, str(value) + ": not a list of tuple")

        if len(value) < len(self.content_schema):
            return Result(False, str(value) + ": wrong length")

        for i in range(0, len(self.content_schema)):
            content_schema_check = self.content_schema[i].check(value[i])
            if not content_schema_check:
                return Result(False, content_schema_check.message + "\nvalue: " + value[i])

        if len(value) > len(self.content_schema):
            if not self.tail_schema:
                return Result(False, str(value) + ": TailSchema???")

            tail_schema_result = self.tail_schema.check(value[len(self.content_schema):])
            if not tail_schema_result:
                return Result(False, tail_schema_result.message + "\nTailSchema issue in: " + str(value[len(self.content_schema)]))

        return Result(True, "All Good")


class StrType(_CoreType):
    @staticmethod
    def subname():
        return 'str'

    def __init__(self, schema, rx):
        if not set(schema.keys()) <= set(('type', 'value', 'length')):
            raise RxError('unknown parameter for //str')

        self.value = None
        if 'value' in schema:
            if not isinstance(schema['value'], string_types):
                raise RxError('invalid value parameter for //str')
            self.value = schema['value']

        self.length = None
        if 'length' in schema:
            self.length = Util.make_range_check(schema["length"])

    def check(self, value):
        if not isinstance(value, string_types):
            return Result(False, str(value) + ": not a str type")
        if (not self.value is None) and value != self.value:
            return Result(False, str(value) + ": wrong str value")
        if self.length and not self.length(len(value)):
            return Result(False, str(value) + ": wrong str length")
        return Result(True, "All Good")


core_types = [
    AllType,  AnyType, ArrType, BoolType, DefType,
    FailType, IntType, MapType, NilType,  NumType,
    OneType,  RecType, SeqType, StrType
]
