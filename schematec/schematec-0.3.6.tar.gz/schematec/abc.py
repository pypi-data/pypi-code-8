from __future__ import absolute_import


class ComplexDescriptor(object):
    def __init__(self, *descriptors):
        self.descriptors = list(descriptors)

    def __and__(self, descriptor):
        if not isinstance(descriptor, AbstractDescriptor):
            raise TypeError(descriptor)

        self.descriptors.append(descriptor)
        return self

    def __iter__(self):
        for descriptor in self.descriptors:
            yield descriptor


class AbstractDescriptor(object):
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


class Validator(AbstractDescriptor):
    BINDING = None
