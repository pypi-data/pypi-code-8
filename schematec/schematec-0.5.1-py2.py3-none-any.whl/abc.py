from __future__ import absolute_import

import collections


class Descriptor(object):
    pass


class ComplexDescriptor(Descriptor, collections.Sequence):
    def __init__(self, *descriptors):
        self.descriptors = list(descriptors)

    @property
    def unbound_validators(self):
        return [v for v in self.descriptors if isinstance(v, UnboundValidator)]

    @property
    def bound_validators(self):
        return [v for v in self.descriptors if isinstance(v, BoundValidator)]

    @property
    def schemas(self):
        return [s for s in self.descriptors if isinstance(s, Schema)]

    @property
    def converters(self):
        return [c for c in self.descriptors if isinstance(c, Converter)]

    def __and__(self, descriptor):
        if not isinstance(descriptor, AbstractDescriptor):
            raise TypeError(descriptor)

        self.descriptors.append(descriptor)
        return self

    def __getitem__(self, index):
        return self.descriptors[index]

    def __len__(self):
        return len(self.descriptors)

    def __call__(self, value):
        for converter in self.converters:
            value = converter(value)

        for validator in self.bound_validators:
            if isinstance(value, validator.BINDING):
                validator(value)

        return value


class AbstractDescriptor(Descriptor):
    def __init__(self):
        pass

    def __call__(self, *args, **kw):
        raise NotImplementedError

    def __and__(self, descriptor):
        if not isinstance(descriptor, AbstractDescriptor):
            raise TypeError(descriptor)

        return ComplexDescriptor(self, descriptor)


class Schema(AbstractDescriptor):
    pass


class Converter(AbstractDescriptor):
    pass


class UnboundValidator(AbstractDescriptor):
    pass


class BoundValidator(AbstractDescriptor):
    BINDING = None
