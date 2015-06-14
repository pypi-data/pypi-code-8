from __future__ import absolute_import


class Cursor(object):
    def __init__(self, collection, pymongo_cursor):
        self.collection = collection
        self.__pymongo_cursor = pymongo_cursor

    def __iter__(self):
        for document in self.__pymongo_cursor:
            document = self.collection.unpack_fields(document)
            if self.collection.model:
                yield self.collection.model(**document)
            else:
                yield document

    def next(self):
        document = next(self.__pymongo_cursor)
        document = self.collection.unpack_fields(document)
        if self.collection.model:
            return self.collection.model(**document)
        else:
            return document

    def sort(self, key):
        key = self.collection.pack_field(key)
        self.__pymongo_cursor = self.__pymongo_cursor.sort(key)
        return self

    def count(self):
        return self.__pymongo_cursor.count()

    def distinct(self, key):
        key = self.collection.pack_field(key)
        return self.__pymongo_cursor.distinct(key)

    def limit(self, limit):
        self.__pymongo_cursor = self.__pymongo_cursor.limit(limit)
        return self

    def rewind(self):
        self.__pymongo_cursor.rewind()

    def skip(self, skip):
        self.__pymongo_cursor = self.__pymongo_cursor.skip(skip)
        return self
