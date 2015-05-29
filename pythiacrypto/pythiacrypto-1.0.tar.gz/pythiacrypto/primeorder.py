"""
A finite (integer) group of prime order (q).
"""

from charm.core.math.integer import (integer, hashInt, isPrime, random, 
    randomPrime, encode, decode, bitsize, serialize, deserialize)

from charm.toolbox.integergroup import IntegerGroup
from common import stringToLong
 
 
class PrimeOrderGroup(object):
    """
    A finite group of prime order. This implementation is a subclass of
    the ShnorrGroup charm.toolbox.IntegerGroup, so the order q must
    be one of the Schnorr primes where p == 2q + 1 and p,q are both prime.
    
    All operations in this group are order q.
    """
    def __init__(self, q=None, g=None, bits=128):
        """
        Create a new group of order @p.
        """
        # Fix residuousity to quadratic. At least, I think that is what @r is 
        # used for.
        self.r = 2

        # Set parameters or select parameters
        if not q:
            _,q = self.genSchnorrPrimes(bits)
        self.setparam(q, g)


    def setparam(self, q, g=None):
        """
        Set parameters for this group. If @g is omitted, a generator @g will 
        be selected at random.
        """
        # Verify the prime order.
        p = 2*q + 1
        if isPrime(p) and isPrime(q):
            self.p = integer(p)
            self.q = integer(q)
        else:
            raise Exception("p and q are not safe primes!")

        # Set or select a generator.
        if g:
            self.g = self.member(g)
        else:
            self.g = self.randomGen()


    def genSchnorrPrimes(self, bits):
        """
        Generates a pair of Schnorr primes (p,q) where p = 2q + 1
        """
        while True:
            p = randomPrime(bits, 1)
            q = (p - 1) / 2
            if isPrime(q):
                break
        return p,q

    def divide(self, a, b):
        """
        Computes a/b (or a*b^{-1}) assuming @a,@b.
        """
        a = self.member(a)
        b = self.member(b)
        return a/b

    def wrap(self, m, t):
        """
        It wraps the message and tweak into one. 
        """
        return self.hashG(t, m)

    def blind(self, msg):
        r = 2*self.random(self.q) + 1
        if isinstance(msg, integer):
            h = msg ** r
        elif isinstance(msg, str):
            m = self.hashZR(msg)
            h = m ** r
        return r, h

    def deblind(self, blind_m, r):
        if isinstance(blind_m, str):
            blind_m = self.deserialize(blind_m)
        rInv = 1/integer(r, self.p-1)
        return blind_m**rInv

    def reduce(self, x):
        """
        Reduce @x modulo q
        """
        return long(long(x) % self.q)


    def hashG(self, *args):
        """
        Hash a series of arbitary values onto this group.
        """
        return hashInt((self._packHashArgs(*args)), self.p, self.q, False)


    def hashZR(self, *args):
        """
        Hash a series of arbitary values into an integer.
        """
        return long(self.hashG(*args))


    def _packHashArgs(self, *args):
        """
        Convert an arbitrary (but non-empty) sequence of arguments into a 
        canonical form for hashing.
        @return a list of normalized arguments, because hashInt requires a list.
        """
        # Reduce any integer.Element types to this modulus
        def quickReduce(x):
            if not x:
                return 0
            if isinstance(x, integer):
                return self.reduce(x)
            elif isinstance(x, int) or isinstance(x, long):
                return self.member(long(x))
            elif isinstance(x, str) or isinstance(x, unicode):
                return self.member(stringToLong(x))
            else:
                raise Exception("Cannot hash item {0} {1}. "\
                    "PrimeOrderGroup can only hash integral arguments "\
                    "(integer.Element, int, long).".format(x, type(x)))
        return [quickReduce(x) for x in args]
        

    def randomMember(self, max=None):
        """
        Select a random group element
        """
        if not max:
            max = self.q
        return random(max)


    def random(self, max=None):
        """
        Select a random integer from 0-@max. If @max is omitted (or 0) then
        a random integer from 0-q is selected.
        """
        return long(self.randomMember(max))


    def randomGen(self):
        """
        Select a random generator for this group of residuosity r=2.
        ACE: Not sure about that last part, but it's my best guess for the
             setting of r.
        """
        while True:
            h = random(self.q)
            g = (h ** self.r) % self.q
            if not g == 1:
                break
        return self.member(g)


    def member(self, x):
        """
        Converts long @x into an element of this group (mod q)
        """
        return integer(long(x) % self.q, self.q)

    def order(self):
        return self.p

    def groupSetting(self):
        return 'integer'
        
    def groupType(self): 
        return 'Prime order group'     
          
    def groupOrder(self):
        return bitsize(self.q)    
    
    def bitsize(self):    
        return bitsize(self.q) / 8 
    

    def serialize(self, x):
        """
        Serialize long or group member @x.
        """
        if type(x) == long:
            x = integer(x)

        elif type(x) != integer:
            raise Exception("Cannot serialize value {} {}. Can only serialize int, long, and integer.Element types".format(x, type(x)))

        return serialize(x)

    
    def deserialize(self, bytes_object):
        assert type(bytes_object) == bytes, "cannot deserialize object"
        return deserialize(bytes_object)
