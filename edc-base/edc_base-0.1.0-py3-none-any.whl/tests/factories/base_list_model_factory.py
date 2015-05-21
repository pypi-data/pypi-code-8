import factory

from edc.testing.factory.factories import BaseFactory


class BaseListModelFactory(BaseFactory):
    ABSTRACT_FACTORY = True

    name = factory.Sequence(lambda n: 'name{0}'.format(n))
    short_name = factory.Sequence(lambda n: 'short name {0}'.format(n))
