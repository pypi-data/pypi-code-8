__author__ = 'Stephan Conrad <stephan@conrad.pics>'

class Acl(object):
    def __init__(self, write = [], read = []):
        self.write = write
        self.read = read

    def __repr__(self):
        return '{read: %s, write: %s}' % (self.read, self.write)


class Share(object):
    def __init__(self, name = None, path = None, acl = Acl, options = {}):
        self.name = name
        self.path = path
        self.acl = acl
        self.options = options
        self.type = "share"

    def __repr__(self):
        return '{name: %s, path: %s, acl: %s, options: %s}' % (self.name, self.path, self.acl, self.options)

    def toJson(self):
        return None

class ShareService(object):
    def getShares(self):
        raise NotImplementedError( "Should have implemented this" )