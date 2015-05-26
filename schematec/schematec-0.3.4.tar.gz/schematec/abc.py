from __future__ import absolute_import


class IDescriptor(object):
    pass


class SyntaxSugarMixin(object):
    def has_sugar_descriptors(self):
        return hasattr(self, '_sugar_descriptors')

    def get_sugar_descriptors(self):
        return self._sugar_descriptors

    def __and__(self, other):
        if not isinstance(other, IDescriptor):
            return super(SyntaxSugarMixin, self).__add__(other)

        if not self.has_sugar_descriptors():
            self._sugar_descriptors = [other]

        self._sugar_descriptors.append(other)
        return self


class Schema(SyntaxSugarMixin, IDescriptor):
    pass


class Converter(SyntaxSugarMixin, IDescriptor):
    pass


class Validator(SyntaxSugarMixin, IDescriptor):
    BINDING = None
