from __future__ import absolute_import

import pymongo

import mongoext.cursor


class Collection(object):
    CONNECTION = None
    DATABASE = None

    KEYS_COMPRESSION = None
    NAME = None

    def __init__(self):
        self._model = None
        self.__pymongo_collection = None

        if self.KEYS_COMPRESSION:
            self.keys_compression = dict(self.KEYS_COMPRESSION, _id='_id')
            self.keys_uncompression = {v: k for k, v in self.keys_compression.iteritems()}
        else:
            self.keys_compression = self.keys_uncompression = None

    @property
    def collection(self):
        if not self.__pymongo_collection:
            self.__pymongo_collection = pymongo.Connection(**self.CONNECTION)[self.DATABASE][self.NAME]
        return self.__pymongo_collection

    @property
    def database(self):
        return self.collection.database

    def pack_field(self, key):
        if not self.keys_compression:
            return key
        return self.keys_compression.get(key, key)

    def pack_fields(self, document):
        if not self.keys_compression:
            return document
        compressed_document = {}
        for key, value in document.iteritems():
            if not key.startswith('$'):
                key = self.keys_compression[key]
            if isinstance(value, dict):
                value = self.pack_fields(value)
            compressed_document[key] = value
        return compressed_document

    def unpack_fields(self, document):
        if not self.keys_uncompression:
            return document
        uncompressed_document = {}
        for key, value in document.iteritems():
            if not key.startswith('$'):
                key = self.keys_uncompression[key]
            if isinstance(value, dict):
                value = self.unpack_fields(value)
            uncompressed_document[key] = value
        return uncompressed_document

    def find(self, spec=None, fields=None, skip=0):
        pymongo_cursor = self.collection.find(
            spec=spec and self.pack_fields(spec),
            fields=fields and self.pack_fields(fields),
            skip=skip,
        )
        return mongoext.cursor.Cursor(self, pymongo_cursor)

    def find_one(self, *args, **kw):
        cursor = self.find(*args, **kw)
        try:
            return next(cursor)
        except StopIteration:
            return

    def insert(self, documents):
        pymongo_documents = []
        for document in documents:
            if self._model and isinstance(document, self._model):
                pymongo_documents.append(document.to_dict())
            elif isinstance(document, dict):
                pymongo_documents.append(document)
            else:
                raise TypeError(type(document))
        pymongo_documents = [self.pack_fields(d) for d in pymongo_documents]

        for document in pymongo_documents:
            drop_fields = []
            for field in document:
                if document[field] is None:
                    drop_fields.append(field)
            for field in drop_fields:
                del document[field]

        return self.collection.insert(pymongo_documents)

    def insert_one(self, document):
        return self.insert([document])

    def count(self):
        return self.collection.count()

    def distinct(self, key):
        key = self.pack_field(key)
        return self.collection.distinct(key)

    def drop(self):
        return self.collection.drop()

    def remove(self, spec=None, multi=True):
        if spec is None:
            return self.collection.remove(multi=multi)

        spec = self.pack_fields(spec)
        return self.collection.remove(spec, multi=multi)

    def save(self, document):
        if not isinstance(document, dict):
            document = document.to_dict()

        document = self.pack_fields(document)
        return self.collection.save(document)

    def update(self, spec, document, multi=False):
        spec = self.pack_fields(spec)
        document = self.pack_fields(document)
        self.collection.update(spec, document, multi=multi)
