"""
Partially-oblivious tweakable PRF (POP) that uses the bilinear pairing
groups and prodives a ZKP for verification. Should probably be called the
Ristenpart Verifiable POPrf.
"""
from charm.core.math.integer import integer
from common import *
from blsgroup import BLSGroup
from tweakablePrf import TweakablePrf
from charm.core.math.pairing import pc_element

class BlsPop(TweakablePrf):
    """
    Partially-oblivious tweakable PRF (POP) that uses the bilinear pairing
    groups and prodives a ZKP for verification.
    """
    def __init__(self, group, serialize=True):
        """
        Initialize this tagged PRF using a BLSGroup @group.
        """
        if not isinstance(group, BLSGroup):
            raise Exception("Group {} must be BLSGroup".format(str(group)))
        super(BlsPop, self).__init__(group, serialize)
        

    def query(self, w, t, x, sk, z, proof=True):
        """ 
        Blinded signature query. 
        @x blinded message m in G1
        @t any string, tweak
        @w any string, key selector
        @h be an element in G_T
        """
        # Derive a secret exponent e from client ID w, and secret state z.
        e = self.group.hashZR(w, sk, z)

        x = self.deserialize(x)
        assert isinstance(x, pc_element), "Blinded message is not an pc_element."\
            "It is type: {}, value: {}".format(type(x), x)

        assert x.type == 2, "Blinded message must be a point on the G2. Got {}".\
            format(["ZR", "G1", "G2"][x.type])
        
        # hash t to G2
        xTilde = self.group.wrap(x, t)

        # Create a public key p = g^e
        p = self.group.g ** e
        
        # Compute a response y = pair(x, H(t))^e
        y = xTilde ** e

        # Compute a proof
        if proof:
            c, u = self.generateZkp(xTilde, e, p, y)
        else:
            c,u = (None, None)

        return self.serialize(p, y, c, u) + (e,)


    def delta(self, ePrime, w, sk, z):
        """
        Generates the value delta = ePrime/e where @ePrime is a newer exponent
        (derived from newer secret key skPrime), and e is an older exponent
        derived from (older key) @sk, plus @w and @z. 

        For efficiency, this method takes the previously computed value @ePrime
        as an input.
        """
        # Derive the older exponent and compute delta.
        e = self.group.hashZR(w, sk, z)
        delta = self.group.divide(ePrime, e)
        return self.serialize(delta)


    def deltaSlow(self, wPrime, skPrime, zPrime, w, sk, z):
        """
        Generates the value delta = ePrime/e. Computes e from w,sk,z; and 
        ePrime from wPRime, skPrime, and zPrime.
        returns (delta, pubkeyPrime) where pubkeyPrime = g^ePrime
        """
        # Derive both exponents and compute delta.
        ePrime = self.secretExponent(wPrime, skPrime, zPrime)
        e = self.secretExponent(w, sk, z)
        delta = self.group.divide(ePrime, e)

        # Compute new pubkey
        pPrime = self.group.g**ePrime
        return self.serialize(delta, pPrime)


    def secretExponent(self, w, sk, z):
        """
        Generates a secret exponent.
        """
        return self.group.hashZR(w, sk, z)


    def applyDelta(self, y, delta):
        """
        Apply the value @delta to an existing PRF response to retrieve an 
        updated response. y' = y^delta
        """
        y,delta = self.deserialize(y,delta)
        return self.serialize(y**delta)


    def generateZkp(self, x, e, p, y):
        """
        Generates a Camenish-Stadler zero-knowledge proof over signed message
        @x and private key @e. For efficiency, p = g^e, y = m^e are passed
        as parameters so they don't need to be re-computed.
        """
        # Select a random exponent v
        v = self.group.random(0) # in ZR

        # Comute our proof over message x and secret key e.
        t1 = self.group.g**v # self.group.g is in G2 and a random element only.
        t2 = x**v
        c  = self.group.hashZR(self.group.g, p, x, y, t1, t2)

        # NOTE: u is NOT a group element. Making it a group element breaks the
        # ZKP.
        u = v - c*e
        return (c, u)


    def verifyZkp(self, w, t, x, p, y, c, u, previousP=None):
        """
        Verifies a zero-knowledge proof from the server 
        """
        # Check pubkeys first.
        if previousP and previousP != p:
            raise Exception("Server's public key p doesn't match previous value.")

        # Deserialize values if needed.
        x,p,y,c,u = self.deserialize(x,p,y,c,u)
        
        assert x.type == 2, "Blinded message must be a point on the G2. "\
            "Got '{}' {}".format(["ZR", "G1", "G2"][x.type], type(x))

        xTilde = self.group.wrap(x, t)
        t1Prime = self.group.g**u * p**c
        t2Prime = xTilde ** u * y**c
        cPrime = self.group.hashZR(self.group.g, p, xTilde, y, t1Prime, t2Prime)

        if long(cPrime) != long(c):
            raise Exception("Server's zero-knowledge proof failed verification for TweakedOPRF.")


    def wrapMessage(self, m):
        """
        Blinds a message @m before making a query.
        returns (r,x) where r is the private value needed for de-blinding and 
           x is the wrapped (blinded) messages.
        """
        r, x = self.group.blind(self.group.hashG2(m))
        return self.serialize(r,x)


    def unwrapResponse(self, r, y):
        """
        Deblinds server response @y using blinding factor @r applied to original
        message.
        """
        r,y = self.deserialize(r,y)
        return self.serialize(self.group.deblind(y, r))
