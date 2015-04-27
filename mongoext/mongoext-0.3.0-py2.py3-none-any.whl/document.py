from __future__ import absolute_import

import mongoext.collection
import mongoext.scheme
import mongoext.exc


class MetaDocument(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        for base in bases:
            for attr, obj in vars(base).iteritems():
                if issubclass(type(obj), mongoext.scheme.Field):
                    fields[attr] = obj
        for attr, obj in attrs.iteritems():
            if issubclass(type(obj), mongoext.scheme.Field):
                fields[attr] = obj
        attrs['SCHEME'] = mongoext.scheme.Scheme(fields)
        return super(MetaDocument, cls).__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        for attr, obj in vars(cls).iteritems():
            if issubclass(type(obj), mongoext.collection.Collection):
                obj._model = cls
        super(MetaDocument, cls).__init__(name, bases, attrs)


class Document(object):
    __metaclass__ = MetaDocument
    SCHEME = None

    objects = None

    _id = mongoext.scheme.Field()

    def __init__(self, **data):
        for attr, value in data.items():
            if attr not in self.SCHEME:
                raise mongoext.exc.SchemeError(attr)
            setattr(self, attr, value)

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)

    def save(self):
        self.SCHEME.validate(self)
        if self._id:
            self.objects.find_one_and_replace(
                filter={'_id': self._id},
                replacement=self.to_dict(),
            )
        else:
            self._id = self.objects.insert_one(self)

    def to_dict(self):
        return {f: getattr(self, f) for f in self.SCHEME}
