#!/usr/bin/env python
"""
Performance testing
"""
from common import *
from groups import *
from testPrf import clientQueryPrf
from taggedPrf import TaggedPrf
from tweakablePrf import TweakablePrf
from ecoprf import EcOprf
from blspop import BlsPop

from timeit import timeit
from testPrf import clientQueryPrf, DUMMY_Z, DUMMY_SK

# Number of iterations for testing
ROUNDS = 1000

clientRequest = (9081734987123904872349867139876123498761234986712394876123498762, 
                 1986123498761234987623498761234987612349817329487091283749872134, 
                 7623459876234598761387465123876513240098743590878765409823498724)


# Production PRFs that we want to test
prfs = [
#    ("query-ecc",  TaggedPrf(ec224, serialize=True)), 
#    ("oquery-ecc", EcOprf(ec224, serialize=True)), 
#    ("query-bls",  TaggedPrf(mnt224, serialize=True)), 
    ("oquery-bls", BlsPop(mnt224, serialize=True)), 
]

def testPrfQuery(iterations=ROUNDS):
    """
    Tests the PRF queries without ZKPs.
    """
    # Unpack query parameters.
    w,t,m = clientRequest

    # Run each group throught the gauntlet.
    for name,prf in prfs:
        print "Running {} for {} iterations".format(name, iterations)
        for i in range(iterations):
            simulateClient(prf, w,t,i)

@profile
def simulateClient(prf,w,t,m):
    # Wrap the message before we send it.
    r, x = prf.wrapMessage(m)
    
    # Query
    p,y,c,u,_ = prf.query(w,t,x, DUMMY_SK, DUMMY_Z)
    
    # Verify proof
    prf.verifyZkp(w,t,x,p,y,c,u)
    
    # Unblind the response values
    yPrime = prf.unwrapResponse(r,y)


# Run performance  testing
if __name__ == "__main__":
    testPrfQuery()
