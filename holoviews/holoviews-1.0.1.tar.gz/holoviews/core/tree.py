try:
    from cyordereddict import OrderedDict
except:
    from collections import OrderedDict

from .pprint import PrettyPrinter
from .util import sanitize_identifier, unescape_identifier


class AttrTree(object):
    """
    An AttrTree offers convenient, multi-level attribute access for
    collections of objects. AttrTree objects may also be combined
    together using the update method or merge classmethod. Here is an
    example of adding a ViewableElement to an AttrTree and accessing it:

    >>> t = AttrTree()
    >>> t.Example.Path = 1
    >>> t.Example.Path                             #doctest: +ELLIPSIS
    1
    """

    @classmethod
    def merge(cls, trees):
        """
        Merge a collection of AttrTree objects.
        """
        first = trees[0]
        for tree in trees:
            first.update(tree)
        return first

    def __init__(self, items=None, identifier=None, parent=None):
        """
        identifier: A string identifier for the current node (if any)
        parent:     The parent node (if any)
        items:      Items as (path, value) pairs to construct
                    (sub)tree down to given leaf values.

        Note that the root node does not have a parent and does not
        require an identifier.
        """
        self.__dict__['parent'] = parent
        self.__dict__['identifier'] = sanitize_identifier(identifier, escape=False)
        self.__dict__['children'] = []
        self.__dict__['_fixed'] = False

        fixed_error = 'No attribute %r in this AttrTree, and none can be added because fixed=True'
        self.__dict__['_fixed_error'] = fixed_error
        self.__dict__['data'] = OrderedDict()
        items = items.items() if isinstance(items, OrderedDict) else items
        # Python 3
        items = list(items) if items else items
        items = [] if not items else items
        for path, item in items:
            self.set_path(path, item)

    @property
    def path(self):
        "Returns the path up to the root for the current node."
        if self.parent:
            return '.'.join([self.parent.path, str(self.identifier)])
        else:
            return self.identifier if self.identifier else self.__class__.__name__


    @property
    def fixed(self):
        "If fixed, no new paths can be created via attribute access"
        return self.__dict__['_fixed']

    @fixed.setter
    def fixed(self, val):
        self.__dict__['_fixed'] = val


    def update(self, other):
        """
        Updated the contents of the current AttrTree with the
        contents of a second AttrTree.
        """
        if not isinstance(other, AttrTree):
            raise Exception('Can only update with another AttrTree type.')
        fixed_status = (self.fixed, other.fixed)
        (self.fixed, other.fixed) = (False, False)
        for identifier, element in other.items():
            if identifier not in self.data:
                self[identifier] = element
            else:
                self[identifier].update(element)
        (self.fixed, other.fixed) = fixed_status


    def set_path(self, path, val):
        """
        Set the given value at the supplied path where path is either
        a tuple of strings or a string in A.B.C format.
        """
        path = tuple(path.split('.')) if isinstance(path , str) else tuple(path)

        if not all(p[0].isupper() for p in path):
            raise Exception("All paths elements must be capitalized.")

        if len(path) > 1:
            attrtree = self.__getattr__(path[0])
            attrtree.set_path(path[1:], val)
        else:
            self.__setattr__(path[0], val)


    def filter(self, path_filters):
        """
        Filters the loaded AttrTree using the supplied path_filters.
        """
        if not path_filters: return self

        # Convert string path filters
        path_filters = [tuple(pf.split('.')) if not isinstance(pf, tuple)
                        else pf for pf in path_filters]

        # Search for substring matches between paths and path filters
        new_attrtree = self.__class__()
        for path, item in self.data.items():
            if any([all([subpath in path for subpath in pf]) for pf in path_filters]):
                new_attrtree.set_path(path, item)

        return new_attrtree


    def _propagate(self, path, val):
        """
        Propagate the value up to the root node.
        """
        self.data[path] = val
        if self.parent is not None:
            self.parent._propagate((self.identifier,)+path, val)


    def __setitem__(self, identifier, val):
        """
        Set a value at a child node with given identifier. If at a root
        node, multi-level path specifications is allowed (i.e. 'A.B.C'
        format or tuple format) in which case the behaviour matches
        that of set_path.
        """
        if isinstance(identifier, str) and '.' not in identifier:
            self.__setattr__(identifier, val)
        elif isinstance(identifier, str) and self.parent is None:
            self.set_path(tuple(identifier.split('.')), val)
        elif isinstance(identifier, tuple) and self.parent is None:
            self.set_path(identifier, val)
        else:
            raise Exception("Multi-level item setting only allowed from root node.")


    def __getitem__(self, identifier):
        """
        For a given non-root node, access a child element by identifier.

        If the node is a root node, you may also access elements using
        either tuple format or the 'A.B.C' string format.
        """
        keyerror_msg = ''
        split_label = (tuple(identifier.split('.'))
                       if isinstance(identifier, str) else tuple(identifier))
        if len(split_label) == 1:
            identifier = split_label[0]
            if identifier in self.children:
                return self.__dict__[identifier]
            else:
                raise KeyError(identifier + ((' : %s' % keyerror_msg) if keyerror_msg else ''))
        path_item = self
        for identifier in split_label:
            path_item = path_item[identifier]
        return path_item


    def __setattr__(self, identifier, val):
        # Getattr is skipped for root and first set of children
        shallow = (self.parent is None or self.parent.parent is None)
        if identifier[0].isupper() and self.fixed and shallow:
            raise AttributeError(self._fixed_error % identifier)

        super(AttrTree, self).__setattr__(identifier, val)

        if identifier[0].isupper():
            identifier = unescape_identifier(identifier)
            if not identifier in self.children:
                self.children.append(identifier)
            self._propagate((identifier,), val)


    def __getattr__(self, identifier):
        """
        Access a identifier from the AttrTree or generate a new AttrTree
        with the chosen attribute path.
        """
        try:
            return super(AttrTree, self).__getattr__(identifier)
        except AttributeError: pass

        if identifier.startswith('__'):
            raise AttributeError('Attribute %s not found.' % identifier)
        elif self.fixed==True:           raise AttributeError(self._fixed_error % identifier)
        identifier = sanitize_identifier(identifier, escape=False)

        unescaped_identifier = unescape_identifier(identifier)
        if unescaped_identifier in self.children:
            return self.__dict__[unescaped_identifier]

        if identifier[0].isupper():
            identifier = unescaped_identifier
            self.children.append(identifier)
            child_tree = self.__class__(identifier=identifier, parent=self)
            self.__dict__[identifier] = child_tree
            return child_tree
        else:
            raise AttributeError("%s: Custom paths elements must be capitalized." % identifier)


    def __iter__(self):
        return iter(self.data.values())


    def __contains__(self, name):
        return name in self.children or name in self.data


    def __len__(self):
        return len(self.data)


    def get(self, identifier, default=None):
        return self.__dict__.get(identifier, default)


    def keys(self):
        return list(self.data.keys())


    def items(self):
        return list(self.data.items())


    def values(self):
        return list(self.data.values())


    def pop(self, identifier, default=None):
        if identifier in self.children:
            item = self[identifier]
            self.__delitem__(identifier)
            return item
        else:
            return default


    def __repr__(self):
        return PrettyPrinter.pprint(self)


__all__ = ['AttrTree']
