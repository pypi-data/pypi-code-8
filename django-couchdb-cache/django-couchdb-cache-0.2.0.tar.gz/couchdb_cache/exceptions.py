class CouchDBCacheError(Exception):
    pass


class InvalidDocumentError(CouchDBCacheError):
    pass


class BadConfigurationError(CouchDBCacheError):
    pass


class ReadError(CouchDBCacheError):
    pass


class WriteError(CouchDBCacheError):
    pass
