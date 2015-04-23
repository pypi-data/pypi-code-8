from sqlalchemy.orm.exc import NoResultFound


class Driver(object):

    def __init__(self, db):
        self.db = db

    def add_group(self, group):
        setattr(self, group.name, group)
        group.init(self.db)


class DriverGroup(object):

    def init(self, db):
        self.db = db
        self.query = db.query


class SqlDriver(DriverGroup):

    def get_or_create(self, **kwargs):
        try:
            return self.query(self.model).filter_by(**kwargs).one()
        except NoResultFound:
            return self.create(**kwargs)

    def get_by_id(self, id):
        return self.find_all().filter_by(id=id).one()

    def find_all(self):
        return self.query(self.model)

    def create(self, **kwargs):
        obj = self.model()
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.db.add(obj)
        return obj

    def delete_by_id(self, id_):
        self.delete(self.get_by_id(id_))

    def delete(self, obj):
        self.db.delete(obj)
