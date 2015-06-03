import six
import sqlobject


class ModelBase(sqlobject.SQLObject.__metaclass__):

    class DefaultMeta(object):
        pass

    def __new__(cls, name, bases, attrs):
        meta = attrs.pop('Meta', None)
        if len(bases) == 0:
            bases = (sqlobject.SQLObject,)
        new_class = super(ModelBase, cls).__new__(cls, name, bases, attrs)
        if meta is None:
            meta = ModelBase.DefaultMeta
        if 'abstract' not in meta.__dict__:
            meta.abstract = False
        new_class.Meta = meta
        return new_class


class Model(six.with_metaclass(ModelBase)):
    created = sqlobject.DateTimeCol(default=sqlobject.DateTimeCol.now())


class User(Model):
    string_id = sqlobject.StringCol()
    username = sqlobject.StringCol()
    real_name = sqlobject.StringCol()
    image = sqlobject.StringCol()

    def __str__(self):
        return self.string_id


class Channel(Model):
    string_id = sqlobject.StringCol()
    name = sqlobject.StringCol()

    def __str__(self):
        return self.string_id
