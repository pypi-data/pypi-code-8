import schematec.abc
import schematec.converters
import schematec.exc
import schematec.schema
import schematec.validators

from . import (
    abc,
    exc,
)

Descriptor = schematec.abc.Descriptor


class Field(schematec.abc.AbstractDescriptor):
    def __call__(self, value):
        return value


Integer = schematec.converters.Integer

Number = schematec.converters.Number

String = schematec.converters.String

Required = schematec.validators.Required


def process(schema, data, weak=False):
    schematec_schema = {}
    for field, descriptor in schema.items():
        if isinstance(descriptor, abc.AbstractField):
            descriptor = descriptor.descriptors
        schematec_schema[field] = descriptor

    try:
        return schematec.schema.process(schematec_schema, data, weak=weak)
    except schematec.exc.ValidationError as e:
        raise exc.ValidationError(e)
