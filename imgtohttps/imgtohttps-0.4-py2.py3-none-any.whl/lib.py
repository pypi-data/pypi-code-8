from collections.abc import Container
from urllib.parse import ParseResult, urlparse


class EmptyUrlError(Exception):
    """ Exception for empty urls"""


class RedisContainer:
    """ Redis container"""

    _storage = None
    name = None

    def __init__(self, storage, name):
        """ Initialize container

        :type name: str
        :type storage: Redis or StrictRedis
        :param storage: Redis client
        :param name: Key name or prefix
        """

        self._storage = storage
        self.name = name


class LinkSet(RedisContainer, Container):
    """ Wrapper class for handling some use cases for
    redis sets as usual python sets
    """

    def __contains__(self, link):
        """
        :type link: Link
        :rtype : bool
        """
        return self._storage.sismember(self.name, link.netloc)

    def add(self, link):
        """
        :type link: Link
        """
        self._storage.sadd(self.name, link.netloc)


class LinksMapping(RedisContainer, Container):
    """ Wrapper class for handling some use cases for
    redis hashes as usual python dicts
    """

    def __contains__(self, link):
        """
        :type link: Link
        """
        return self._storage.hexists(self.name, link.url)

    def add(self, link, uploaded):
        """
        :type link: Link
        :type uploaded: Link
        """
        self._storage.hset(self.name, link.url, uploaded.secure)

    def __getitem__(self, link):
        """
        :rtype : Link
        :type link: Link
        """
        if not isinstance(link, Link):
            raise TypeError

        result = self._storage.hget(self.name, link.url)
        if result is None:
            raise KeyError

        return Link(result.decode())


class LinkRegistry(RedisContainer):
    """Registry for metadata of each uploaded image"""

    def update(self, data):
        """
        :type data: dict[str, str|int|None]
        """
        self._storage.hmset(self.name + data['link'], data)


class Link:
    secure_scheme = 'https'
    netloc = None
    path = None
    params = None
    query = None
    fragment = None
    url = None

    def __init__(self, raw_url):
        """ Construct Link instance with some useful methods

        :type raw_url: str
        """
        fragments = urlparse(raw_url)
        if not any(fragments):
            raise EmptyUrlError('Incorrect url')
        else:
            for key, value in fragments._asdict().items():
                setattr(self, key, value)
            self.url = raw_url

    @property
    def is_secure(self):
        """
        :rtype : str
        """
        return self.scheme == self.secure_scheme

    @property
    def secure(self):
        """
        :rtype : str
        """
        if self.is_secure:
            return self.url
        return ParseResult(
            self.secure_scheme,
            self.netloc,
            self.path,
            self.params,
            self.query,
            self.fragment
        ).geturl()
