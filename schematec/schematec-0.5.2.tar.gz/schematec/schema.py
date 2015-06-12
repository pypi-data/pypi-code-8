from __future__ import absolute_import

import functools

import schematec.abc as abc
import schematec.converters
import schematec.exc as exc


class Dictionary(abc.Schema):
    def __init__(self, **descriptors):
        self.descriptors = descriptors

    def __call__(self, data, weak=False):
        data = schematec.converters.dictionary(data)

        if not self.descriptors:
            return data

        result = {}

        for name, descriptors in self.descriptors.items():
            if isinstance(descriptors, abc.AbstractDescriptor):
                descriptors = abc.ComplexDescriptor(descriptors)
            elif not isinstance(descriptors, abc.ComplexDescriptor):
                raise TypeError(descriptors)

            if not weak:
                for validator in descriptors.unbound_validators:
                    validator(name, data)

            if name not in data:
                continue

            try:
                value = data[name]
            except KeyError:
                raise exc.SchemaError(name)

            result[name] = descriptors(value, weak=weak)

        return result

dictionary = Dictionary


class Array(abc.Schema):
    def __init__(self, *descriptors):
        if descriptors:
            descriptors = descriptors[0]
            if isinstance(descriptors, abc.AbstractDescriptor):
                descriptors = abc.ComplexDescriptor(descriptors)
            elif not isinstance(descriptors, abc.ComplexDescriptor):
                raise TypeError(descriptors)
            self.descriptors = descriptors
        else:
            self.descriptors = []

    def __call__(self, data, weak=False):
        data = schematec.converters.array(data)

        if not self.descriptors:
            return data

        return map(functools.partial(self.descriptors, weak=weak), data)

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


def process(schema, data, weak=False):
    return expand(schema)(data, weak=weak)
