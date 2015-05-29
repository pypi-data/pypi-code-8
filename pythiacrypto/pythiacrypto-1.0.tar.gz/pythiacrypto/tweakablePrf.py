"""
Base class for tweakable PRF schemes including partially-oblivious and n
on-oblivious schemes.
"""
from common import *

NOT_IMPLEMENTED = "This method is not implemented"

class TweakablePrf(object):
    def __init__(self, group, serialize=True):
        self.group = group
        self.serializeAll = serialize
        
    def query(self, w, t, x, sk, z):
        raise Exception(NOT_IMPLEMENTED)

    def delta(self, ePrime, w, sk, z):
        raise Exception(NOT_IMPLEMENTED)

    def deltaSlow(self, wPrime, skPrime, zPrime, w, sk, z):
        raise Exception(NOT_IMPLEMENTED)

    def secretExponent(self, w, sk, z):
        raise Exception(NOT_IMPLEMENTED)

    def applyDelta(self, y, delta):
        raise Exception(NOT_IMPLEMENTED)

    def generateZkp(self, x, e, p, y):
        raise Exception(NOT_IMPLEMENTED)

    def verifyZkp(self, w, t, m, p, y, c, u, previousP=None):
        raise Exception(NOT_IMPLEMENTED)

    def wrapMessage(self, m):
        raise Exception(NOT_IMPLEMENTED)

    def unwrapResponse(self, x):
        raise Exception(NOT_IMPLEMENTED)

    def serialize(self, *args):
        """
        Serialize @args if self.serialize is set.
        """
        def ser(x):
            return urlencode(self.group.serialize(x))

        if self.serializeAll:
            return simpleTuple([ ser(x) for x in args ])
        else: 
            return simpleTuple(args)


    def deserialize(self, *args):
        """
        Deserialize @args if self.serialize is set.
        """
        if self.serializeAll:
            args = [ deserializeStr(x, self.group.deserialize) for x in args ]
            return simpleTuple(args)
        else: 
            return simpleTuple(args)


def deserializeStr(x, func):
    """
    Deserialize @x using a given @func if x is unicode or string.
    """
    # Convert unicode to strings.
    if isinstance(x, unicode):
        x = str(x)

    # Then call the serialization
    if isinstance(x, str):
        return func(urldecode(x))
    else:
        return x


def urlencode(x):
    if x:
        return x.replace("+", "-").replace("/", "_")

def urldecode(x):
    if x:
        return x.replace("-", "+").replace("_", "/")


def simpleTuple(t):
    """
    Generates a simple return type: if list @t contains one item, returns a 
    single item, otherwise returns a tuple.
    """
    if len(t) == 1:
        return t[0]
    else:
        return tuple(t)