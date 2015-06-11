from __future__ import absolute_import

import schematec.abc as abc
import schematec.converters
import schematec.exc as exc


class Dictionary(abc.Schema):
    def __init__(self, **descriptors):
        self.descriptors = descriptors

    def __call__(self, data, strict=False):
        data = schematec.converters.dictionary(data)

        if not self.descriptors:
            return data

        result = {}

        for name, descriptors in self.descriptors.items():
            if isinstance(descriptors, abc.AbstractDescriptor):
                descriptors = [descriptors]
            elif isinstance(descriptors, abc.ComplexDescriptor):
                descriptors = list(descriptors)
            else:
                raise TypeError(descriptors)

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
    def __init__(self, *descriptors):
        if descriptors:
            descriptors = descriptors[0]
            if isinstance(descriptors, abc.AbstractDescriptor):
                self.descriptors = [descriptors]
            elif isinstance(descriptors, abc.ComplexDescriptor):
                self.descriptors = list(descriptors)
            else:
                raise TypeError(descriptors)
        else:
            self.descriptors = []

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


def expand(schema):
    if isinstance(schema, (abc.AbstractDescriptor, abc.ComplexDescriptor)):
        return schema
    elif isinstance(schema, dict):
        return Dictionary(**{n: expand(d) for n, d in schema.items()})
    elif isinstance(schema, list):
        if schema:
            return Array(expand(schema[0]))
        else:
            return Array()
    else:
        raise exc.SchemaError(schema)


def process(schema, data, strict=False):
    return expand(schema)(data, strict=strict)
