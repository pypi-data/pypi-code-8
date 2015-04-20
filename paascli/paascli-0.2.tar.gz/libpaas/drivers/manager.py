__author__ = 'hvishwanath'

from heroku import Heroku
from openshift import Openshift

class DriverManager(object):

    __singleton = None
    def __new__(cls, *args, **kwargs):
        # Check to see if a __singleton exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __singleton objects
        if cls != type(cls.__singleton):
        #if not cls.__singleton:
            cls.__singleton = super(DriverManager, cls).__new__(cls, *args, **kwargs)
        return cls.__singleton

    @classmethod
    def getInstance(cls, *args):
        '''
        Returns a singleton instance of the class
        '''
        if not cls.__singleton:
            cls.__singleton = DriverManager(*args)
        return cls.__singleton

    def __init__(self):
        self.drivers = {}
        self.add_driver("heroku", Heroku)
        self.add_driver("openshift", Openshift)

    def add_driver(self, name, cls):
        self.drivers[name] = cls

    def find_driver(self, name):
        if name in self.drivers:
            return self.drivers.get(name)
        return None

    def remove_driver(self, name):
        if name in self.drivers:
            self.drivers.pop(name)

    def list_drivers(self):
        return self.drivers.keys()

ignore = DriverManager()