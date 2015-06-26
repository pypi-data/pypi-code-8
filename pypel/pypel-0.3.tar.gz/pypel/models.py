# coding: utf-8
"""pypel.models, models for pypel.

THIS SOFTWARE IS UNDER BSD LICENSE.
Copyright (c) 2012-2015 Daniele Tricoli <eriol@mornie.org>

Read LICENSE for more informations.
"""

import os.path

import six

from gi.repository import GExiv2

XMP_KEY_PREFIX = 'Xmp.pypel.'

SUPPORTED_EXT = ('.jpg', '.jpeg', '.png', '.eps')


class DoesNotExist(IOError):
    """The file or directory does not exist"""


class IsADirectory(IOError):
    """This is a directory so you can't use it as a receipt"""


class ImageNotSupported(IOError):
    """Image is not supported"""


class Field(object):
    """Base class for all field types"""

    casting_function = lambda self, value: value
    creation_counter = 1

    def __init__(self):
        self.name = None

        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    @property
    def key(self):
        return XMP_KEY_PREFIX + self.name

    def __get__(self, instance, owner):
        return self.cast(instance.get_value(self.key))

    def __set__(self, instance, value):
        instance.set_value(self.key, value)

    def __delete__(self, instance):
        instance.delete_value(self.key)

    def cast(self, value):
        if value is not None:
            return self.casting_function(value)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)


class CharField(Field):
    """A field for character strings"""


class FloatField(Field):
    """A field for float numbers"""

    casting_function = float


class ModelBase(type):
    """Metaclass for models"""

    def __init__(cls, name, bases, attrs):

        if not hasattr(cls, '_fields'):
            cls._fields = []

        for name in attrs:
            if isinstance(attrs[name], Field):
                # Set field name because it is required for key generation
                setattr(attrs[name], 'name', name.title())

                cls._fields.append(attrs[name])

        cls._fields.sort(key=lambda field: field.creation_counter)

        super(ModelBase, cls).__init__(name, bases, attrs)


class Model(six.with_metaclass(ModelBase)):

    def __init__(self, file):
        self.file = file
        self._metadata = GExiv2.Metadata(file)

        if not self._metadata.has_xmp():
            self._metadata.register_xmp_namespace('pypelNamespace/', 'pypel')

    def get_value(self, key):
        try:
            return self._metadata[key]
        except KeyError:
            return None

    def set_value(self, key, value):
        self._metadata[key] = str(value)
        self._metadata.save_file()

    def delete_value(self, key):
        try:
            del self._metadata[key]
        except KeyError:
            pass
        self._metadata.save_file()

    def asdict(self):
        d = {'file': self.file}
        for field in self._fields:
            name = field.name.lower()
            d[name] = getattr(self, name)

        return d

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.file)


class Receipt(Model):
    price = FloatField()
    retailer = CharField()
    note = CharField()


def delete_metadata(receipt, price=None, retailer=None, note=None):
    """Delete XMP metadata."""

    if not price and not retailer and not note:
        del receipt.price
        del receipt.retailer
        del receipt.note

    if price:
        del receipt.price

    if retailer:
        del receipt.retailer

    if note:
        del receipt.note


def set_metadata(receipt, price=None, retailer=None, note=None):
    """Set XMP metadata."""

    if price:
        receipt.price = price

    if retailer:
        receipt.retailer = retailer

    if note:
        receipt.note = note


def make_receipt(file):
    """Check for errors and create a receipt"""

    if not os.path.exists(file):
        raise DoesNotExist('No such file or directory')
    elif os.path.isdir(file):
        raise IsADirectory('Is a directory')
    elif os.path.splitext(file)[1].lower() not in SUPPORTED_EXT:
        raise ImageNotSupported

    return Receipt(file)
