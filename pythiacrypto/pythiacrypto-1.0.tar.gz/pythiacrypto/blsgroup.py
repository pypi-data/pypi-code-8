"""
Bilinear pairing group

G1 x G2 -> GT
where, e(a,b)
g <- random generator
(sk,pk)
"""
from charm.toolbox.IBSig import IBSig
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.core.engine.util import objectToBytes
from charm.core.math.pairing import pc_element
from base64 import b64encode
from common import *

class BLSGroup(IBSig, object):
    """
    A wrapper around IBSig to permit using bilnear pairing groups in the Pythia
    PRF protocol.
    """
    def __init__(self, groupname=None, groupObj=None, generators={}):
        if groupname:
            groupObj = PairingGroup(groupname)
        if not groupObj:
            raise Exception("No Group Initialized")

        IBSig.__init__(self)
        self.group = groupObj
        if generators:
            self.g = self.deserialize(generators['gt'])
            self.g1 = self.deserialize(generators['g1'])
            self.g2 = self.deserialize(generators['g2'])
        else:
            self.g = self.group.random(GT)
            self.g1 = self.group.random(G1)
            self.g2 = self.group.random(G2)
        

        # TODO: Also check g != unit

        # Disabled for benchmarking
        #self.g.initPP()
        #self.g1.initPP()
        #self.g2.initPP()

    def divide(self, a, b):
        """
        Computes a/b (or a*b^{-1}).
        """
        return a/b

    def pair(self, a, b):
        return pair(a, b)

    def dump(self, obj):
        return objectToBytes(obj, self.group)


    def random(self, *args, **kwargs):
        return self.group.random(*args, **kwargs)

        
    def serialize(self, arg):
        if not arg:
            return None        

        elif isinstance(arg, pc_element):
            return self.group.serialize(arg)
        elif isinstance(arg, str):
            return arg
        else:
            raise Exception("Wrong type of object passed. Expecting {0}, Got {1}"\
                            .format(pc_element, type(arg), arg))

    def deserialize(self, arg):
        if not arg:
            return None
        else:
            return self.group.deserialize(arg)
            
    def verify(self, sig, m, pk):
        return pair(sig, self.g2) == pair(m, pk)


    def wrap(self, x, t):
        """
        It wraps the message and tweak into one. 
        """
        assert x.type == 2, "The first argument must be in group type"
        # hashing onto G2 is slower, push to the client
        ht = self.hashG1(t)
        return pair(ht, x)


    # Will run on the clientside
    def blind(self, m):
        r = self.group.random(ZR)
        # hashing to G2 is slower, so let the client do more work. 
        return r, self.hashG2(m)**r # m has to be hashed to G2


    def deblind(self, sig, r):
        if isinstance(sig, str):
            sig = self.deserialize(sig)
        rInv = 1/r
        return sig**rInv 


    def _packHashInputs(self, *args):
        """
        Convert arbitrary list of inputs to a canonical form for hashing.
        """
        # Deal with a variety of known types.
        def toBytes(x):
            if x is None:
                raise Exception("Cannot hash value None")
            elif isinstance(x, pc_element):
                return self.serialize(x)
            elif isinstance(x, bytes):
                return x
            elif isinstance(x, int) or isinstance(x, long):
                return bytes(x)
            else:
                return objectToBytes(x, self.group) 
                #return bytes(str(x), 'utf8')
                
        # Convert our arguments into a single message @m in a canonical form.
        m = '*'.join(b64encode(toBytes(x)) for x in args)
        return m


    def memberZq(self, x):
        """
        Converts long @x into a member of Zq where q is the order of this group.
        """
        return integer(long(x) % self.group.order(), self.group.order())


    def _hash(self, msg, target):
        """
        Hash @msg to the @target type: either ZR or G.
        """
        # Ensure the target type is valid.
        if not target in [ZR, G1, G2]:
            raise Exception("Unknown target [{0}]. Must be charm.toolbox.pairinggroup.ZR or G1, G2")

        # Ensure a valid message.
        if not msg:
            raise Exception("Hash input cannot be empty.")

        # Hash the message to the selected target.
        return self.group.hash(msg, target)


    def hashG1(self, *args):
        """
        Hashes and arbitrary list of inputs to a member of this group.
        """
        return self._hash(self._packHashInputs(*args), G1)


    def hashG2(self, *args):
        """
        Hashes and arbitrary list of inputs to a member of this group.
        """
        return self._hash(self._packHashInputs(*args), G2)


    def hashZR(self, *args):
        """
        Hashes and arbitrary list of inputs to ZR.
        """
        return self._hash(self._packHashInputs(*args), ZR)


    def hashG(self, *args):
        """
        Hashes and arbitrary list of inputs to G1 ** Note to G1 ** just to meet
        the symmetry with other groups.
        """
        return self._hash(self._packHashInputs(*args), G1)


    def hash(self, args, _target=None):
        """
        Hide the base class hash() function because the implementation sucks.
        """
        raise Exception("This function is not supported. Use hashG or hashZR.")
