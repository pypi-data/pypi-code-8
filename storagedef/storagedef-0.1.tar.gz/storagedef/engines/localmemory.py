# -*- coding: utf-8 -*-

from io import BytesIO
from zope.interface import implementer
from ..exceptions import DoesNotExist
from ..interfaces import IStorageEngine


@implementer(IStorageEngine)
class LocalMemoryStorageEngine(object):

    def __init__(self, **kwargs):
        self.storage = {}

    def delete(self, filename):
        if filename not in self.storage:
            raise DoesNotExist(filename)
        del self.storage[filename]

    def exists(self, filename):
        return filename in self.storage

    def retrieve(self, filename):
        if filename not in self.storage:
            raise DoesNotExist(filename)
        return BytesIO(self.storage[filename])

    def store(self, filename, fileobj):
        v = fileobj.read()
        self.storage[filename] = v
