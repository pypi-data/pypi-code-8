"""
Partially-oblivious tweakable PRF (POP) that uses an elliptic curve as the 
underlying group and prodives a ZKP for verification.
"""
from charm.core.math.integer import integer
from hashlib import sha256

from common import *
from ecgroup import ECGroup
from tweakablePrf import TweakablePrf

# this should be as large as one cannot find a obvious 
# collision in t, H2(t') = H2(t)
IDEAL_VALUE_OF_N = 256

# Tags for HMAC
TAG_Z = "TAG_ECOPRF_EXPAND_Z"

class EcOprf(TweakablePrf):
    """
    A tweakbale OPRF that is also verifiable by clients via zero-knowledge 
    proofs.
    """
    def __init__(self, group, n=IDEAL_VALUE_OF_N, serialize=True):
        """
        Initialize this OPRF using an EcGroup.
        """
        if not isinstance(group, ECGroup):
            raise Exception("Group {} must be an ECGroup.".format(str(group)))
        super(EcOprf, self).__init__(group, serialize)
        self.n = n
        

    def expandZ(self, z, n):
        """
        Expand secret values @z into a vector of @n values using iterated 
        hashing.
        """
        return [ self.group.hashZR(i, z) for i in range(n) ]


    def generateKey(self, avector, t):
        # Hash t and then convert it into a binary string.
        intDigest = int(sha256(bytes(t)).hexdigest(), 16)
        tTilde = reversed(bin(intDigest).zfill(self.n+2))

        e = avector[0]
        # NOTE: Making this operation constant-time out of general principle.
        for i,t in zip(xrange(self.n), tTilde):
            ePrime = e * avector[i+1]
            # Assuming assignment is fast, this should be fine.
            if t == '1':
               e = ePrime

        return e

    def query(self, w, t, x, sk, z, proof=True):
        """
        Server implementation of a PRF query for client ID @w, tag @t, and 
        message @x, uses server's secret key @sk and state value @z associated 
        with the client ID @w.
        Input:
            @z is a vector of keys with size 'n'
            @x is a blinded message, MUST BE in the correct group
        @returns: (p, y, c, u, e) 
            @p is the server's public key associated with w, p == w^e;
            @y is the PRF output; and
            @c,@u (along with p) make up the zero-knowledge proof of the 
                exponent e used to generate y.
            @e server's private exponent
        """

        x = self.deserialize(x)
        assert isinstance(x, type(self.group.g)), "@x must be a group element. Expected {}"\
            " but got {}".format(type(x), type(self.group.g))


        # Expand Z, Z = k_0=sk, k_1, k_2...k_n
        zVector = [self.group.hashZR(sk)] + self.expandZ(z, self.n)
        e = self.generateKey(zVector, t)

        # Create a public key p = g^e
        pk = self.group.g ** e

        # Compute a response y = (H(t,x))^e
        y = x ** e

        # Compute the proof
        if proof:
            c, u = self.generateZkp(x, e, pk, y)
        else:
            c,u = (None, None)
            
        return self.serialize(pk, y, c, u) + (zVector,)


    def delta(self, ePrime, w, sk, z):
        """
        @w: Ignores w
        @ePrime: is a list of numbers [h(sk), zVector]
        Generates the value delta_i = k'_i/k_i where @k'_i is a newer exponent
        @returns: the whole list of delta_i's
        """
        # Derive the older exponent and compute delta.
        keylist= [self.group.hashZR(sk)] + self.expandZ(z, self.n)
        assert keylist[0] != ePrime[0], "Both keys are same. {} and {}"\
                             .format(keylist[0], ePrime[0])
        delta = [self.group.divide(kiPrime,ki) \
                 for kiPrime, ki in zip(ePrime, keylist)]
        return [self.serialize(d) for d in delta]


    def deltaSlow(self, wPrime, skPrime, zPrime, w, sk, z):
        """
        Generates the value delta = ePrime/e. Computes e from w,sk,z; and 
        ePrime from wPRime, skPrime, and zPrime.
        returns (delta, pubkeyPrime) where pubkeyPrime = g^ePrime
        """
        zVectorPrime = [self.group.hashZR(skPrime)] \
                       + self.expandZ(zPrime, self.n)
        return delta(zVectorPrime, w, sk, z), None
        # pPrime = None
        # return self.serialize(delta, pPrime) # as pPrime does not make sense for NR
        
        
    def secretExponent(self, w, sk, z):
        """
        Generates a secret exponent.
        """
        raise Exception("Not valid for Naor-Reingold POPRF protocol");


    def applyDelta(self, y, delta, t):
        """
        One has to specify t as well to perform delta
        Apply the value @delta to an existing PRF response to retrieve an 
        updated response. y' = y^delta
        """
        y,t = self.deserialize(y,t)
        delta = self.deserialize(*delta)
        keydelta = self.generateKey(delta, t)
        return self.serialize(y**keydelta)


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


    def verifyZkp(self, w, t, m, p, y, c, u, previousP=None):
        """
        Verifies a zero-knowledge proof pi = (@c, @u) from the server 
        using server's public key @p (for value w).

        If a @previousP value is provided, verifies that p == previousP.

        If @deserialize is set to True, all group member inputs are assumed to 
        be serialized values values and will be deserialized before processed.

        If the ZKP fails validation or if previousP doesn't match p, 
        an exception is raised.
        """
        # Check pubkeys first.
        if previousP and previousP != p:
            raise Exception("Server's public key p doesn't match previous value.")

        # Deserialize values.
        x,p,y,c,u = self.deserialize(m,p,y,c,u)
        
        assert x.type == 1, "Blinded message must be a point on the G1. "\
            "Got '{}' {}".format(["ZR", "G1", "G2"][x.type], type(x))

        xTilde = x
        t1Prime = self.group.g**u * p**c
        t2Prime = xTilde ** u * y**c
        cPrime = self.group.hashZR(self.group.g, p, xTilde, y, t1Prime, t2Prime)

        # NOTE: I tried using cPrime.isCongruent(c) here and generated segfaults.
        # I suspect a bug in Charm's C-code for isCongruent.
        if long(cPrime) != long(c):
            raise Exception("Server's zero-knowledge proof failed verification for TweakedOPRF.")

    def wrapMessage(self, m):
        """
        Blinds a message @m before making a query.
        returns (r,x) where r is the private value needed for de-blinding and 
           x is the wrapped (blinded) messages.
        """
        r, x = self.group.blind(self.group.hashG(m))
        return self.serialize(r,x)


    def unwrapResponse(self, r, y):
        """
        Deblinds server response @y using blinding factor @r applied to original
        message.
        """
        r,y = self.deserialize(r,y)
        return self.serialize(self.group.deblind(y, r))
