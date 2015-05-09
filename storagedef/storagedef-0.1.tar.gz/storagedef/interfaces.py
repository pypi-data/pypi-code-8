# -*- coding: utf-8 -*-

from zope.interface import Interface


class IStorageEngine(Interface):
    """ Strorage abstract layer """

    def delete(filename):
        """  Delete content that labeled filename from the storage. """

    def exists(filename):
        """ Return True if file that has `filename` exists. """

    def retrieve(filename):
        """ Return a file like object. """

    def store(filename, fileobj):
        """ Store fileobj as filename into the storage. """
