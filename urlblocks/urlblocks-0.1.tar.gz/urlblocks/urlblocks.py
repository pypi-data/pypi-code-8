from .compat import urlparse
from .netloc import Netloc
from .path import URLPath, path_encode, path_decode
from .ports import DEFAULT_PORTS
from .query_string import QueryString
from .domain_levels import DOMAIN_LEVEL_SECOND
from .six import text_type, u


class BaseURL(text_type):

    """
    A URL.

    This class contains properties and methods for accessing and modifying the
    constituent components of a URL. :class:`URL` instances are
    immutable, as they derive from the built-in ``unicode``, and therefore all
    methods return *new* objects; you need to consider this when using
    :class:`URL` in your own code.

    >>> from urlblocks import URL
    >>> url = URL("http://www.google.com/")
    >>> print(url)
    http://www.google.com/

    URL objects feature properties for directly accessing different parts of
    the URL: :attr:`.scheme`, :attr:`.netloc`, :attr:`.username`,
    :attr:`.password`, :attr:`.hostname`, :attr:`.port`, :attr:`.path`,
    :attr:`.query` and :attr:`.fragment`.

    All of these have a ``with_*`` method for adding/replacing them, and some
    have a ``without_*`` method for removing them altogether. The query string
    and path also have a variety of methods for doing more fine-grained
    inspection and manipulation.
    """

    @classmethod
    def from_iri(cls, iri):
        """
        Create a URL from an IRI, which may have non-ascii text it.

        This is probably how you should construct a URL if the input is
        from a user, since users tend to type addresses using their native
        character sets.

        The domain name will be encoded as per IDNA, and the whole IRI will be
        encoded to UTF-8 and URL-escaped, as per RFC 3987. The IRI is not
        checked for conformance with the IRI specification, so this may still
        accept invalid IRIs and produce invalid URLs.

        Beyond the IRI encoding rules, this also URL-quotes all special
        characters, so that a space character is replaced by %20, for example.
        The % character is *not* quoted, because users often copy/paste
        addresses that are already quoted, and we should not double-quote it.

        >>> print(URL.from_iri(u('https://\xe9xample.com/p\xe5th')))
        https://xn--xample-9ua.com/p%C3%A5th
        """
        # This code approximates Section 3.1 of RFC 3987, using the option of
        # encoding the netloc with IDNA.
        split = urlparse.urlsplit(iri)
        netloc = split.netloc.encode('idna').decode('ascii')
        path = path_encode(split.path.encode('utf-8'), safe='/%;')
        query = path_encode(split.query.encode('utf-8'), safe='=&%')
        fragment = path_encode(split.fragment.encode('utf-8'), safe='%')
        new_components = split._replace(netloc=netloc,
                                        path=path,
                                        query=query,
                                        fragment=fragment,
                                        )
        return cls(urlparse.urlunsplit(new_components))

    @property
    def scheme(self):
        """
        This URL's scheme.

        >>> print(URL("http://www.google.com").scheme)
        http
        """
        return urlparse.urlsplit(self).scheme

    def with_scheme(self, scheme):
        """
        Replace this URL's :attr:`.scheme`.

        >>> print(URL("http://www.google.com").with_scheme("ftp"))  # doctest: +IGNORE_UNICODE
        ftp://www.google.com
        """
        return self.__replace(scheme=scheme)

    @property
    def netloc(self):
        """
        The full network location of this URL.

        This value incorporates :attr:`.username`, :attr:`.password`,
        :attr:`.hostname` and :attr:`.port`.

        >>> print(URL("http://user:pass@www.google.com").netloc)
        user:pass@www.google.com
        """
        return Netloc(urlparse.urlsplit(self).netloc)

    def with_netloc(self, netloc):
        """
        Add or replace this URL's :attr:`.netloc`.

        >>> print(URL("http://www.google.com/a/b/c").with_netloc("www.amazon.com"))
        http://www.amazon.com/a/b/c
        """
        return self.__replace(netloc=netloc)

    @property
    def username(self):
        """
        This URL's username, if any.

        >>> print(URL("http://user@www.google.com").username)
        user
        >>> print(URL("http://www.google.com").username)
        None
        """
        return self.netloc.username

    def with_username(self, username):
        """
        Add or replace this URL's :attr:`.username`.

        >>> print(URL("http://user@www.google.com").with_username("user2"))
        http://user2@www.google.com
        """
        return self.with_netloc(self.netloc.with_username(username))

    def without_username(self):
        """
        Remove this URL's :attr:`.username`.

        >>> print(URL("http://user@www.google.com/").without_username())
        http://www.google.com/
        """
        return self.with_netloc(self.netloc.without_username())

    @property
    def password(self):
        """
        This URL's password, if any.

        >>> print(URL("http://user:somepassword@www.google.com").password)
        somepassword
        >>> print(URL("http://user@www.google.com").password)
        None
        """
        return self.netloc.password

    def with_password(self, password):
        """
        Add or replace this URL's :attr:`.password`.

        >>> print(URL("http://user:somepassword@www.google.com").with_password("passwd"))
        http://user:passwd@www.google.com
        """
        return self.with_netloc(self.netloc.with_password(password))

    def without_password(self):
        """
        Remove this URL's :attr:`.password`.

        >>> print(URL("http://user:pwd@www.google.com").without_password())
        http://user@www.google.com
        """
        return self.with_netloc(self.netloc.without_password())

    @property
    def hostname(self):
        """
        This URL's hostname.

        >>> print(URL("http://www.google.com").hostname)
        www.google.com
        """
        return self.netloc.hostname

    def with_hostname(self, hostname):
        """
        Add or replace this URL's :attr:`.hostname`.

        >>> print(URL("http://www.google.com/a/b/c").with_hostname("cdn.amazon.com"))
        http://cdn.amazon.com/a/b/c
        """
        return self.with_netloc(self.netloc.with_hostname(hostname))

    @property
    def port(self):
        """
        This URL's port number, or ``None``.

        >>> URL("http://www.google.com:8080").port
        8080
        >>> print(URL("http://www.google.com").port)
        None
        """
        return self.netloc.port

    def with_port(self, port):
        """
        Add or replace this URL's :attr:`.port`.

        >>> print(URL("http://www.google.com/a/b/c").with_port(8080))
        http://www.google.com:8080/a/b/c
        """
        return self.with_netloc(self.netloc.with_port(port))

    def without_port(self):
        """
        Remove this URL's :attr:`.port`.

        >>> print(URL("http://www.google.com:8080/a/b/c").without_port())
        http://www.google.com/a/b/c
        """
        return self.with_netloc(self.netloc.without_port())

    @property
    def auth(self):
        """
        The username and password of this URL as a 2-tuple.

        >>> URL("http://user:password@www.google.com").auth  # doctest: +IGNORE_UNICODE
        ('user', 'password')
        >>> URL("http://user@www.google.com").auth  # doctest: +IGNORE_UNICODE
        ('user', None)
        >>> URL("http://www.google.com").auth
        (None, None)
        """
        return self.netloc.auth

    def with_auth(self, *auth):
        """
        Add or replace this URL's :attr:`.username` and :attr:`.password`.

        With two arguments, this method adds/replaces both username and
        password. With one argument, it adds/replaces the username and removes
        any password.

        >>> print(URL("http://user:password@www.google.com").with_auth("otheruser", "otherpassword"))
        http://otheruser:otherpassword@www.google.com
        >>> print(URL("http://www.google.com").with_auth("user"))
        http://user@www.google.com
        """
        return self.with_netloc(self.netloc.with_auth(*auth))

    def without_auth(self):
        """
        Remove any :attr:`.username` and :attr:`.password` on this URL.

        >>> print(URL("http://user:password@www.google.com/a/b/c").without_auth())
        http://www.google.com/a/b/c
        """
        return self.with_netloc(self.netloc.without_auth())

    @property
    def default_port(self):
        """
        The destination port number for this URL.

        If no port number is explicitly given in the URL, this will return the
        default port number for the scheme if one is known, or ``None``. The
        mapping of schemes to default ports is defined in
        :const:`urlblocks.ports.DEFAULT_PORTS`.

        For URLs *with* explicit port numbers, this just returns the value of
        :attr:`.port`.

        >>> URL("https://www.google.com").default_port
        443
        >>> URL("http://www.google.com").default_port
        80
        >>> URL("http://www.google.com:126").default_port
        126
        """
        port = urlparse.urlsplit(self).port
        if port is not None:
            return port
        return DEFAULT_PORTS.get(self.scheme)

    @property
    def path(self):
        """
        This URL's path.

        >>> print(URL("http://www.google.com/a/b/c").path)
        /a/b/c
        >>> print(URL("http://www.google.com").path)
        <BLANKLINE>
        """
        return URLPath(urlparse.urlsplit(self).path)

    def with_path(self, path):
        """
        Add or replace this URL's :attr:`.path`.

        >>> print(URL("http://www.google.com/a/b/c").with_path("c/b/a"))
        http://www.google.com/c/b/a
        """
        return self.__replace(path=path)

    @property
    def root(self):
        """
        The root node of this URL.

        This is just a synonym for ``url.with_path('/')``.

        >>> print(URL("http://www.google.com/a/b/c").root)
        http://www.google.com/
        """
        return self.with_path('/')

    @property
    def parent(self):
        """
        The direct parent node of this URL.

        >>> print(URL("http://www.google.com/a/b/c").parent)
        http://www.google.com/a/b/
        >>> print(URL("http://www.google.com/a/b/").parent)
        http://www.google.com/a/
        """
        return self.with_path(self.path.parent)

    @property
    def is_leaf(self):
        """
        Whether this URL's :attr:`.path` is a leaf node or not.

        A leaf node is simply one without a trailing slash. Leaf-ness affects
        things like relative URL resolution (c.f. :meth:`.relative`) and
        server-side routing.

        >>> URL("http://www.google.com/a/b/c").is_leaf
        True
        >>> URL('http://www.google.com/a/').is_leaf
        False
        >>> URL('http://www.google.com').is_leaf
        False
        """
        return self.path.is_leaf

    def add_path_segment(self, segment):
        """
        >>> print(URL("http://www.google.com").add_path_segment("a"))
        http://www.google.com/a
        """
        return self.with_path(self.path.add_segment(segment))

    def add_path(self, partial_path):
        """
        >>> print(URL("http://www.google.com").add_path("a/b/c"))
        http://www.google.com/a/b/c
        """
        return self.with_path(self.path.add(partial_path))

    @property
    def query(self):
        """
        This URL's query string.

        >>> print(URL("http://www.google.com").query)
        <BLANKLINE>
        >>> print(URL("http://www.google.com?a=b").query)
        a=b
        """
        return QueryString(urlparse.urlsplit(self).query)

    def with_query(self, query):
        """
        Add or replace this URL's :attr:`.query` string.

        >>> print(URL("http://www.google.com").with_query("a=b"))
        http://www.google.com?a=b
        """
        return self.__replace(query=query)

    def without_query(self):
        """
        Remove this URL's :attr:`.query` string.

        >>> print(URL("http://www.google.com?a=b&c=d").without_query())
        http://www.google.com
        """
        return self.__replace(query='')

    @property
    def query_list(self):
        """
        This URL's :attr:`.query` as a list of name/value pairs.

        This attribute is read-only. Changes you make to the list will not
        propagate back to the URL.

        >>> URL("http://www.google.com?a=b&c=d").query_list  # doctest: +IGNORE_UNICODE
        [('a', 'b'), ('c', 'd')]
        """
        return self.query.list

    @property
    def query_dict(self):
        """
        This URL's :attr:`.query` as a dict mapping names to values.

        Each name will have only its last value associated with it. For all the
        values for a given key, see :attr:`.query_multi_dict`.

        >>> URL("http://www.google.com?a=b&c=d").query_dict == {'a': 'b', 'c': 'd'}
        True
        >>> URL("http://www.google.com?a=b&a=c").query_dict == {'a': 'c'}
        True
        """
        return self.query.dict

    @property
    def query_multi_dict(self):
        """
        This URL's :attr:`.query` as a dict mapping names to lists of values.

        All values associated with a given name will be represented, in order,
        in that name's list.

        >>> URL("http://www.google.com?a=b&c=d").query_multi_dict == {'a': ['b'], 'c': ['d']}
        True
        >>> URL("http://www.google.com?a=b&a=c").query_multi_dict == {'a': ['b', 'c']}
        True
        """
        return self.query.multi_dict

    def add_query_param(self, name, value):
        """
        Add a single query parameter.

        You can ``add`` several query parameters with the same name to a URL.

        >>> print(URL("http://www.google.com").add_query_param("a", "b"))
        http://www.google.com?a=b
        >>> print(URL("http://www.google.com").add_query_param("a", "b").add_query_param("a", "c"))
        http://www.google.com?a=b&a=c
        """
        return self.with_query(self.query.add_param(name, value))

    def add_query_params(self, *args, **kwargs):
        """
        Add multiple query parameters.

        Accepts anything you would normally pass to ``dict()``: iterables of
        name/value pairs, keyword arguments and dictionary objects.

        >>> print(URL("http://www.google.com").add_query_params([('a', 'b'), ('c', 'd')]))
        http://www.google.com?a=b&c=d
        >>> print(URL("http://www.google.com").add_query_params(a="b"))
        http://www.google.com?a=b
        """
        return self.with_query(self.query.add_params(*args, **kwargs))

    def set_query_param(self, name, value):
        """
        Set a single query parameter, overriding it if it exists already.

        >>> print(URL("http://www.google.com?a=b&c=d").set_query_param("a", "z"))
        http://www.google.com?c=d&a=z
        """
        return self.with_query(self.query.set_param(name, value))

    def set_query_params(self, *args, **kwargs):
        """
        Set query parameters, overriding existing ones.

        Accepts anything you would normally pass to ``dict()``: iterables of
        name/value pairs, keyword arguments and dictionary objects.

        >>> print(URL("http://www.google.com?a=b&c=d").set_query_params([('a', 'z'), ('d', 'e')]))
        http://www.google.com?c=d&a=z&d=e
        >>> print(URL("http://www.google.com?a=b").set_query_params(a="z"))
        http://www.google.com?a=z
        """
        return self.with_query(self.query.set_params(*args, **kwargs))

    def del_query_param(self, name):
        """
        Remove any and all query parameters with the given name from the URL.

        >>> print(URL("http://www.google.com?a=b&c=d&c=e").del_query_param("c"))
        http://www.google.com?a=b
        """
        return self.with_query(self.query.del_param(name))

    def del_query_params(self, params):
        """
        Remove multiple query params from the URL.

        >>> print(URL("http://www.google.com?a=b&c=d&d=e").del_query_params(["c", "d"]))
        http://www.google.com?a=b
        """
        return self.with_query(self.query.del_params(params))

    @property
    def fragment(self):
        """
        This URL's fragment.

        >>> print(URL("http://www.google.com/a/b/c#fragment").fragment)
        fragment
        """
        return path_decode(urlparse.urlsplit(self).fragment)

    def with_fragment(self, fragment):
        """
        Add or replace this URL's :attr:`.fragment`.

        >>> print(URL("http://www.google.com/a/b/c#fragment").with_fragment("new_fragment"))
        http://www.google.com/a/b/c#new_fragment
        """
        return self.__replace(fragment=path_encode(fragment))

    def without_fragment(self):
        """
        Remove this URL's :attr:`.fragment`.

        >>> print(URL("http://www.google.com/a/b/c#fragment").without_fragment())
        http://www.google.com/a/b/c
        """
        return self.__replace(fragment='')

    def with_trailing_slash(self):
        """
        >>> print(URL("http://www.google.com").with_trailing_slash())
        http://www.google.com/
        >>> print(URL("http://www.google.com/").with_trailing_slash())
        http://www.google.com/
        >>> print(URL("http://www.google.com/?a=1").with_trailing_slash())
        http://www.google.com/?a=1
        >>> print(URL("http://www.google.com?a=1").with_trailing_slash())
        http://www.google.com/?a=1
        >>> print(URL("http://www.google.com:15?a=1").with_trailing_slash())
        http://www.google.com:15/?a=1
        >>> print(URL("http://www.google.com:15/?a=1").with_trailing_slash())
        http://www.google.com:15/?a=1
        >>> print(URL("http://www.google.com:15/asd").with_trailing_slash())
        http://www.google.com:15/asd/
        >>> print(URL("http://www.google.com:15/asd/").with_trailing_slash())
        http://www.google.com:15/asd/
        """
        url_without_query = self.without_query()
        if not url_without_query.endswith('/'):
            return self.replace(url_without_query, url_without_query + '/', 1)
        return self

    def without_trailing_slash(self):
        """
        >>> print(URL("http://www.google.com").without_trailing_slash())
        http://www.google.com
        >>> print(URL("http://www.google.com/").without_trailing_slash())
        http://www.google.com
        >>> print(URL("http://www.google.com/?a=1").without_trailing_slash())
        http://www.google.com?a=1
        >>> print(URL("http://www.google.com?a=1").without_trailing_slash())
        http://www.google.com?a=1
        >>> print(URL("http://www.google.com:15?a=1").without_trailing_slash())
        http://www.google.com:15?a=1
        >>> print(URL("http://www.google.com:15/?a=1").without_trailing_slash())
        http://www.google.com:15?a=1
        >>> print(URL("http://www.google.com:15/asd").without_trailing_slash())
        http://www.google.com:15/asd
        >>> print(URL("http://www.google.com:15/asd/").without_trailing_slash())
        http://www.google.com:15/asd
        """
        url_without_query = self.without_query()
        if url_without_query.endswith('/'):
            return self.replace(url_without_query, url_without_query[:-1], 1)
        return self

    @property
    def domains(self):
        """
        All domains of this URL.

        >>> print(URL("http://www.example.code.google.com").domains)  # doctest: +IGNORE_UNICODE
        ['www', 'example', 'code', 'google', 'com']
        """
        return self.netloc.domains

    @property
    def subdomain(self):
        """
        This URL's subdomain.

        >>> print(URL('http://www.google.com').subdomain)
        www
        """
        return self.netloc.subdomain

    def add_subdomain(self, subdomain):
        """
        Add new subdomain.

        >>> print(URL('http://google.com').add_subdomain('code'))
        http://code.google.com
        """
        return self.with_netloc(self.netloc.add_subdomain(subdomain))

    def remove_subdomain(self):
        """
        Remove current subdomain.

        >>> print(URL('http://code.google.com').remove_subdomain())
        http://google.com
        """
        return self.with_netloc(self.netloc.remove_subdomain())

    def get_domain(self, domain_level=DOMAIN_LEVEL_SECOND):
        """
        Getting a domain of this URL by domain_level, which by default points to base level domain.

        >>> print(URL("http://www.example.code.google.com").get_domain())
        google
        >>> from .domain_levels import DOMAIN_LEVEL_TOP
        >>> print(URL("http://www.example.code.google.com").get_domain(DOMAIN_LEVEL_TOP))
        com
        """
        return self.netloc.get_domain(domain_level=domain_level)

    def with_domain(self, domain, domain_level=DOMAIN_LEVEL_SECOND):
        """
        Add or replace this URL's domain on selected level.
        >>> print(URL('http://google.com').with_domain('example'))
        http://example.com
        """
        return self.with_netloc(self.netloc.with_domain(domain, domain_level=domain_level))

    def relative(self, other):
        """
        Resolve another URL relative to this one.

        For example, if you have a browser currently pointing to
        ``http://www.google.com/a/b/c/``, then an HTML element like
        ``<a href="../d/e/f">`` would resolve to
        ``http://www.google.com/a/b/d/e/f`` using this function.

        >>> print(URL("http://www.google.com/a/b/c/").relative("../d/e/f"))
        http://www.google.com/a/b/d/e/f
        """
        # Relative URL resolution involves cascading through the properties
        # from left to right, replacing
        other = _RelativeURL(other)
        if other.scheme:
            return URL(other)
        elif other.netloc:
            return URL(other.with_scheme(self.scheme))
        elif other.path:
            return URL(other.with_scheme(self.scheme).with_netloc(self.netloc) \
                             .with_path(self.path.relative(other.path)))
        elif other.query:
            return URL(other.with_scheme(self.scheme).with_netloc(self.netloc) \
                             .with_path(self.path))
        elif other.fragment:
            return URL(other.with_scheme(self.scheme).with_netloc(self.netloc) \
                             .with_path(self.path).with_query(self.query))
        # Empty string just removes fragment; it's treated as a path meaning
        # 'the current location'.
        return self.without_fragment()

    def __replace(self, **replace):
        """Replace a field in the ``urlparse.SplitResult`` for this URL."""
        return type(self)(urlparse.urlunsplit(urlparse.urlsplit(self)._replace(**replace)))


class URLError(Exception):
    pass


class URL(BaseURL):
    class IsEmpty(URLError):
        pass

    class SchemeDoesNotExist(URLError):
        pass

    class HostnameDoesNotExist(URLError):
        pass

    def __repr__(self):
        return u('URL(%r)') % (text_type(self),)

    def __new__(cls, *args, **kwargs):
        obj = super(URL, cls).__new__(cls, *args, **kwargs)
        if not obj:
            raise obj.IsEmpty('URL is empty.')
        if not obj.scheme:
            raise obj.SchemeDoesNotExist('URL "{0}" not provides a scheme.'.format(args[0]))
        if not obj.hostname or len(obj.domains) < 2:
            raise obj.HostnameDoesNotExist('URL "{0}" not provides a hostname, which '
                                           'should contain at least 1 top-level domain and 1 second-level domain.'.
                                           format(args[0]))
        return obj


class _RelativeURL(BaseURL):
    def __repr__(self):
        return u('_RelativeURL(%r)') % (text_type(self),)
