"""
Tagged PRF provides a verifiable, rate-limited and key-updateable PRF using
either PrimeOrderGroup or ECGroup for the underlying group operations.
"""
from charm.core.math.integer import integer
from common import *
from primeorder import PrimeOrderGroup
from blsgroup import BLSGroup
from ecgroup import ECGroup

class TaggedPrf(object):
    """
    A tagged PRF that is also verifiable by clients via zero-knowledge proofs,
    securely rate-limited on queries, and key-updateable by either the client
    or the server with minimal interaction.
    """
    def __init__(self, group, serialize=True):
        """
        Initialize this tagged PRF using the specified @group: a 
        PrimeOrderGroup, ECGroup, or BLSGroup.

        If @serialized is True, function outputs are serialized and inputs
         are assumed to be serialized.
        """
        if not(isinstance(group, PrimeOrderGroup) or isinstance(group, ECGroup) 
                or isinstance(group, BLSGroup)):
            raise Exception("Group {} must be a pythia.PrimeOrderGroup, "\
                "pythia.ECGroup or pythia.BLSGroup".format(str(group)))
        self.group = group
        self.serializeAll = serialize

    #@profile
    def query(self, w, t, m, sk, z, proof=True):
        """
        Server implementation of a PRF query for client ID @w, tag @t, and 
        message @m, uses server's secret key @sk and state value @z associated 
        with the client ID @w.

        @returns: (p, y, c, u, e) 
            @p is the server's public key associated with w, p == w^e;
            @y is the PRF output; and
            @c,@u (along with p) make up the zero-knowledge proof of the 
                exponent e used to generate y.
            @e server's private exponent
        """
        # Derive a secret exponent e from client ID w, and secret state z.
        e = self.group.hashZR(w, sk, z)

        # Create a public key p = g^e

        # Compute a response y = (H(t,x))^e
        xTilde = self.group.hashG(t, m)
        y = xTilde ** e

        if not proof:
            p,c,u = (None, None, None)
        elif isinstance(self.group, BLSGroup):
            p = self.group.g2 ** e
            c, u = None, None
        else:
            p = self.group.g ** e
            c, u = self.generateZkp(xTilde, e, p, y)

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


    def applyDelta(self, y, delta, t=None):
        """
        Apply the value @delta to an existing PRF response to retrieve an 
        updated response. y' = y^delta
        """
        y,delta = self.deserialize(y,delta)
        return self.serialize(y**delta)


    def applyExponent(self, y, z):
        """
        Apply a client generated exponent @z to a check value @y
        returns: y' = y^z
        """
        y = self.deserialize(y)
        z = self.group.hashZR(z)
        return self.serialize(y**z)

    #@profile
    def generateZkp(self, xTilde, e, p, y):
        """
        Generates a Camenish-Stadler zero-knowledge proof over signed message
        @xTilde and private key @e. For efficiency, p = g^e, y = m^e are passed
        as parameters so they don't need to be re-computed.
        """
        # Select a random exponent v
        v = self.group.random()

        # Comute our proof over message xTilde and secret key e.
        t1 = self.group.g**v
        t2 = xTilde**v
        c = self.group.hashZR(self.group.g, p, xTilde, y, t1, t2)

        # NOTE: u is NOT a group element. Making it a group element breaks the
        # ZKP.
        u = v - c*long(e)
        return (c,u)


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

        # Deserialize values if needed.
        p,y,c,u = self.deserialize(p,y,c,u)

        # For BLS signature check is easy.
        if isinstance(self.group, BLSGroup):
            xTilde = self.group.hashG(t, m)

            if not self.group.verify(y, xTilde, p):
                raise Exception("Server's zero-knowledge proof for BLS group failed.")

            # That's it for the BLS verification.
            return

        # Check the proof
        xTilde = self.group.hashG(t, m)
        t1Prime = (self.group.g**u) * (p**c)
        t2Prime = xTilde**u * y**c
        cPrime = self.group.hashZR(self.group.g, p, xTilde, y, t1Prime, t2Prime)

        # NOTE: I tried using cPrime.isCongruent(c) here and generated segfaults.
        # I suspect a bug in Charm's C-code for isCongruent.
        if long(cPrime) != long(c):
            raise Exception("Server's zero-knowledge proof failed verification.")


    def wrapMessage(self, m):
        return (None, m)

    def unwrapResponse(self, r, y):
        return y

    def serialize(self, *args):
        """
        Serialize @args if self.serialize is set.
        """
        if self.serializeAll:
            
            return simpleTuple([self.group.serialize(x) for x in args])
        else: 
            return simpleTuple(args)


    def deserialize(self, *args):
        """
        Deserialize @args if self.serialize is set.
        """
        if self.serializeAll:
            return simpleTuple([self.group.deserialize(str(x)) for x in args])
        else: 
            return simpleTuple(args)


def simpleTuple(t):
    """
    Generates a simple return type: if list @t contains one item, returns a 
    single item, otherwise returns a tuple.
    """
    if len(t) == 1:
        return t[0]
    else:
        return tuple(t)


