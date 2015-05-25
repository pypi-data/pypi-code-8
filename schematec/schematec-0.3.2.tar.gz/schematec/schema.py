from __future__ import absolute_import

import schematec.abc as abc
import schematec.converters
import schematec.exc as exc


class Dictionary(abc.Schema):
    '''
    Unbound validators is appliyed first.
    Converters is appliyed second in orderder they defined
    Bound validators is appliyed third.
    '''
    def __init__(self, **descriptors):
        self.descriptors = descriptors

    def __call__(self, data, strict=False):
        data = schematec.converters.dictionary(data)

        if not self.descriptors:
            return data

        result = {}

        for name, descriptors in self.descriptors.items():
            if isinstance(descriptors, abc.IDescriptor):
                descriptors = [descriptors]

            unbound_validators = [v for v in descriptors if
                                  isinstance(v, abc.Validator) and not v.BINDING]
            for validator in unbound_validators:
                validator(name, data)

            try:
                value = data[name]
            except KeyError:
                if strict:
                    raise exc.SchemaError(name)
                else:
                    continue

            schemas = [s for s in descriptors if isinstance(s, abc.Schema)]
            for schema in schemas:
                value = schema(value, strict=strict)

            converters = [c for c in descriptors if isinstance(c, abc.Converter)]
            for converter in converters:
                value = converter(value)

            bound_validators = [v for v in descriptors if isinstance(v, abc.Validator) and v.BINDING]
            for validator in bound_validators:
                if isinstance(value, validator.BINDING):
                    validator(value)
            result[name] = value

        return result

dictionary = Dictionary


class Array(abc.Schema):
    '''
    Converters is appliyed first in orderder they defined
    Bound validators is appliyed second.
    '''
    def __init__(self, *descriptors):
        self.descriptors = descriptors

    def __call__(self, data, strict=False):
        data = schematec.converters.array(data)

        if not self.descriptors:
            return data

        schemas = [s for s in self.descriptors if isinstance(s, abc.Schema)]
        for schema in schemas:
            data = [schema(d, strict=strict) for d in data]

        converters = [c for c in self.descriptors if isinstance(c, abc.Converter)]
        for converter in converters:
            data = map(converter, data)

        bound_validators = [v for v in self.descriptors if isinstance(v, abc.Validator) and v.BINDING]
        for validator in bound_validators:
            for value in data:
                if isinstance(value, validator.BINDING):
                    validator(value)

        return data

array = Array
