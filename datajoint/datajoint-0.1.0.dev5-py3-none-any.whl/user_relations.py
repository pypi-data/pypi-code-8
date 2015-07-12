from datajoint.relation import Relation
from .autopopulate import AutoPopulate
from datajoint.utils import from_camel_case


class Manual(Relation):
    @property
    def table_name(self):
        return from_camel_case(self.__class__.__name__)


class Lookup(Relation):
    @property
    def table_name(self):
        return '#' + from_camel_case(self.__class__.__name__)


class Imported(Relation, AutoPopulate):
    @property
    def table_name(self):
        return "_" + from_camel_case(self.__class__.__name__)


class Computed(Relation, AutoPopulate):
    @property
    def table_name(self):
        return "__" + from_camel_case(self.__class__.__name__)


class Subordinate:
    """
    Mix-in to make computed tables subordinate
    """
    @property
    def populate_relation(self):
        return None

    def _make_tuples(self, key):
        raise NotImplementedError('Subtables should not be populated directly.')


