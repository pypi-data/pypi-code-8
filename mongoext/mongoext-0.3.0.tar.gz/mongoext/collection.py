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
            self.__pymongo_collection = pymongo.MongoClient(**self.CONNECTION)[self.DATABASE][self.NAME]
        return self.__pymongo_collection

    @property
    def database(self):
        return self.collection.database

    def clean(self, document):
        for field in (f for f, v in document.items() if v is None):
            del document[field]

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

    def find(self, filter=None, projection=None, skip=0):
        pymongo_cursor = self.collection.find(
            filter=filter and self.pack_fields(filter),
            projection=projection and self.pack_fields(projection),
            skip=skip,
        )
        return mongoext.cursor.Cursor(self, pymongo_cursor)

    def find_one(self, filter_or_id=None, *args, **kw):
        document = self.collection.find_one(filter_or_id, *args, **kw)
        document = self.unpack_fields(document)
        if self._model:
            return self._model(**document)
        else:
            return document

    def find_one_and_replace(self, filter, replacement, projection=None):
        pymongo_cursor = self.collection.find_one_and_replace(
            filter=filter and self.pack_fields(filter),
            replacement=replacement and self.pack_fields(replacement),
            projection=projection and self.pack_fields(projection),
        )
        return mongoext.cursor.Cursor(self, pymongo_cursor)

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
            self.clean(document)

        return self.collection.insert_many(pymongo_documents)

    def insert_one(self, document):
        if self._model and isinstance(document, self._model):
            document = document.to_dict()
        else:
            raise TypeError(type(document))
        self.clean(document)
        document = self.pack_fields(document)
        print document
        return self.collection.insert_one(document).inserted_id

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

    def update(self, spec, document, multi=False):
        spec = self.pack_fields(spec)
        document = self.pack_fields(document)
        self.collection.update(spec, document, multi=multi)
