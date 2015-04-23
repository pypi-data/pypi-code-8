from .driver import Driver


class FixtureGenerator(object):

    def __init__(self, sql):
        self.fixtures = {}
        self.sql = sql

    def init_fixture(self, db, application):
        self.db = db
        self.application = application
        self.driver = Driver(db)
        for group in self.sql.groups:
            self.driver.add_group(group)
        self.walk_thru_plugins()

    def walk_thru_plugins(self):
        for plugin in self.application.plugins:
            method = getattr(plugin, 'generate_drivers', None)
            if method:
                method(self.driver)

    def create_all(self):
        self.make_all()
        self.db.flush()
        return self.fixtures

    def _create(self, cls, **kwargs):
        driver = self._get_driver(cls)
        obj = driver.create(**kwargs)
        self._add_object_to_fixtures(obj, kwargs['name'])
        return obj

    def _create_nameless(self, cls, **kwargs):
        driver = self._get_driver(cls)
        obj = driver.create(**kwargs)
        self._add_nameless_object_to_fixtures(obj)
        return obj

    def _add_nameless_object_to_fixtures(self, obj):
        clsname = obj.__class__.__name__
        data = self.fixtures.get(clsname, [])
        data.append(obj)
        self.fixtures[clsname] = data

    def _add_object_to_fixtures(self, obj, name):
        clsname = obj.__class__.__name__
        data = self.fixtures.get(clsname, {})
        data[name] = obj
        self.fixtures[clsname] = data

    def _get_driver(self, cls):
        name = cls if isinstance(cls, str) else cls.__name__
        return getattr(self.driver, name)
