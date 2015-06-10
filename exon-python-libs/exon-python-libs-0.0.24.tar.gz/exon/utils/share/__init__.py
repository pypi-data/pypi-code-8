__author__ = 'Stephan Conrad <stephan@conrad.pics>'

class Acl(object):
    """
    Class for storing Rights for a Share
    """
    def __init__(self, write = [], read = []):
        self.write = write
        self.read = read

    def __repr__(self):
        return '{read: %s, write: %s}' % (self.read, self.write)


class Share(object):
    """
    Base class for a filesystem Share
    """
    def __init__(self, name = None, path = None, acl = Acl(), options = {}):
        self.name = name
        self.path = path
        self.acl = acl
        self.options = options
        self.type = "share"

    def __repr__(self):
        return '{name: %s, path: %s, acl: %s, options: %s}' % (self.name, self.path, self.acl, self.options)

    def toJson(self):
        return None
    @classmethod
    def fromJson(cls, map):
        raise NotImplementedError( "Should have implemented this" )

class ShareService(object):
    """
    Base class for parsing share service config file
    """
    def getShares(self):
        """
        Reads all shares form config file
        :return: a list of shares
        """
        raise NotImplementedError( "Should have implemented this" )

    def writeShare(self, share):
        """
        Writes on share to the config file
        :param share: a share object
        :return: True or False
        """
        raise NotImplementedError( "Should have implemented this" )
    def fromJson(self, map):
        """
        takes a map from a json and adds the share to the config files
        :param map:
        :return:
        """
        raise NotImplementedError( "Should have implemented this" )
    def delete(self, name):
        """
        Deletes a share from config files
        :param name:
        :return:
        """
        raise NotImplementedError( "Should have implemented this" )