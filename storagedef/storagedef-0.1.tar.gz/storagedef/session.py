# -*- coding: utf-8 -*-

from paste.deploy.util import lookup_object
from zope.interface.verify import verifyObject
from .interfaces import IStorageEngine


class Session(object):

    @classmethod
    def from_config(cls, config, prefix='', **kwargs):
        """
        :type config: dict
        :type prefix: str
        :rtype: Session
        """
        config = dict((k[len(prefix):], config[k]) for k in config
                      if k.startswith(prefix))
        config.update(kwargs)
        factory_name = config.pop('provider')
        factory = lookup_object(factory_name)
        engine = factory(**config)
        verifyObject(IStorageEngine, engine)
        return cls(engine)

    def __init__(self, engine=None):
        self.engine = engine

    def delete(self, filename):
        """
        :type filename: str
        """
        self.engine.delete(filename)

    def exists(self, filename):
        """
        :type filename: str
        :rtype: bool
        """
        return self.engine.exists(filename)

    def retrieve(self, filename):
        """
        :type filename: str
        :rtype: file
        """
        return self.engine.retrieve(filename)

    def store(self, filename, fileobj):
        """
        :type filename: str
        :type fileobj: file
        """
        self.engine.store(filename, fileobj)
