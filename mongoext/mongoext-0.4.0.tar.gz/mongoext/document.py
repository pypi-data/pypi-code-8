from __future__ import absolute_import

import mongoext.abc
import mongoext.collection
import mongoext.schema
import mongoext.exc


class MetaSchema(type):
    FIELD = (mongoext.abc.AbstractField, mongoext.schema.Descriptor)

    def __new__(cls, class_name, bases, attrs):
        schema = {}
        for base in bases:
            for name, obj in vars(base).iteritems():
                if issubclass(type(obj), cls.FIELD):
                    schema[name] = obj
        for name, obj in attrs.iteritems():
            if issubclass(type(obj), cls.FIELD):
                schema[name] = obj
        attrs['_schema'] = schema
        for name, descriptor in schema.items():
            if not isinstance(descriptor, mongoext.abc.AbstractField):
                descriptor = mongoext.abc.AbstractField(descriptor)
            attrs[name] = descriptor
        return super(MetaSchema, cls).__new__(cls, class_name, bases, attrs)


class Document(object):
    __metaclass__ = MetaSchema
    _schema = None

    _id = mongoext.schema.Field()

    def __init__(self, **data):
        data = mongoext.schema.process(self._schema, data, weak=True)
        for name, value in data.items():
            setattr(self, name, value)

    def __contains__(self, name):
        return name in self._schema

    def __len__(self):
        return len(self._schema)

    def __iter__(self):
        for name in self._schema:
            value = getattr(self, name, None)
            if value is not None:
                yield name, getattr(self, name, None)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)
