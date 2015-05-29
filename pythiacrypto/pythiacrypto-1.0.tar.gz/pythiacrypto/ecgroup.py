"""
An elliptic curve group that can use any curve defined in 
charm.core.math.elliptic_curve.
"""
from charm.core.math.elliptic_curve import elliptic_curve,ec_element,hashEC
from charm.core.math import integer
from charm.toolbox.ecgroup import ECGroup as ECG
from charm.toolbox.ecgroup import ZR,G, order
from charm.core.engine.util import objectToBytes
from base64 import b64encode


class ECGroup(ECG, object):
    """
    An elliptic curve group wrapper around charm.toolbox.ecgroup.ECGroup
    """
    def __init__(self, curve, serializedG=None):
        """
        Creates a new elliptic curve (EC) group using a builtin @curve from
        charm.toolbox.eccurve (e.g. prime192v1) and uses generator @serializedG
        (assumed to be a generator serialized to a string) if specified.
        if @serializedG is omitted (or None), then a generator is selected
        at random from the group.
        """
        self.group = elliptic_curve(nid=curve)
        self.ec_group = self.group
        self.param = curve

        # Set the generator
        if serializedG:
            # Deserialize the generator
            # NOTE: There is no direct way to test if this is valid point 
            # on this curve.
            self.g = self.deserialize(serializedG)
            if not self.g:
                # If deserialization failed, raise an exception
                raise Exception("Generator g {0} failed to deserialized. " \
                        "Maybe it's malformed or maybe not a point on this "\
                        "curve?".format(serializedG))
        else:
            self.g = self.randomG()

    def randomG(self):
        """
        Select a random group element.
        """
        return self.random(_type=G)


    def randomZR(self):
        """
        Select a random integer element.
        """
        return self.random(_type=ZR)


    def divide(self, a, b):
        """
        Computes a/b (or a*b^{-1}).
        """
        return a * (b**(-1))


    def _packHashInputs(self, *args):
        """
        Convert arbitrary list of inputs to a canonical form for hashing.
        """
        # Deal with a variety of known types.
        def toBytes(x):
            if not x: 
                return b'0'
            if isinstance(x, ec_element):
                return self.serialize(x)
            elif isinstance(x, bytes) or isinstance(x, str) \
                 or isinstance(x, unicode):
                return x
            elif type(x) == int or type(x) == long:
                return bytes(x)
            elif isinstance(x, integer.integer):
                return integer.serialize(x)
            else:
                return x

        # Convert our arguments into a single message @m in a canonical form.
        m = '*'.join(b64encode(toBytes(x)) for x in args)
        return m


    def serialize(self, x):
        if not x:
            return None
        else:
            return ECG.serialize(self, x)


    def wrap(self, m, t):
        """
        It wraps the message and tweak into one. 
        """
        return self.hashG(m,t)

    def blind(self, msg):
        r = self.random(_type=ZR)
        return r, msg**r

    def deblind(self, blind_m, r):
        rInv = r ** -1
        return blind_m ** rInv

    def _hash(self, msg, target):
        """
        Hash @msg to the @target type: either ZR or G.
        """
        # Ensure the target type is valid.
        if not (target == ZR or target == G):
            raise Exception("Unknown target [{0}]. Must be charm.toolbox.ecgroup.ZR or G")

        # Ensure a valid message.
        if not msg:
            raise Exception("Hash input cannot be empty.")

        # Hash the message to the selected target.
        return hashEC(self.ec_group, msg, target)


    def hashG(self, *args):
        """
        Hashes and arbitrary list of inputs to a member of this group.
        """
        return self._hash(self._packHashInputs(*args), G)


    def hashZR(self, *args):
        """
        Hashes and arbitrary list of inputs to ZR.
        """
        return self._hash(self._packHashInputs(*args), ZR)


    def hash(self, args, _target=None):
        """
        Hide the base class hash() function because the implementation sucks.
        """
        raise Exception("This function is not supported. Use hashG or hashZR.")
