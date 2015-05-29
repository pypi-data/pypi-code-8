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

# Groups to test
groups = [("EC 224", ec224), ("MNT-224", mnt224), ("SS-512", ss512)]
oprf_groups = groups

clientRequest = (9081734987123904872349867139876123498761234986712394876123498762, 
                 1986123498761234987623498761234987612349817329487091283749872134, 
                 7623459876234598761387465123876513240098743590878765409823498724)


# Production PRFs that we want to test
prfs = [
    ("query-ecc",  TaggedPrf(ec224, serialize=True)), 
    ("oquery-ecc", EcOprf(ec224, serialize=True)), 
    ("query-bls",  TaggedPrf(mnt224, serialize=True)), 
    ("oquery-bls", BlsPop(mnt224, serialize=True)), 
]

def testPrfQuery(iterations=ROUNDS, zkp=True):
    """
    Tests the PRF queries without ZKPs.
    """
    # Unpack query parameters.
    w,t,m = clientRequest

    # Run each group throught the gauntlet.
    for name,prf in prfs:

        # Wrap the message before we send it.
        _, x = prf.wrapMessage(m)

        # Timeit
        query = lambda: prf.query(w,t,x, DUMMY_SK, DUMMY_Z, proof=zkp)
        seconds = timeit(query, number=iterations)

        # Print results
        text = "-ZKP" if zkp else ""

        print "{}, {} iterations: {:4.3f} seconds (total);\t"\
            "{:4.3f} seconds (average)".format(name+text, 
                iterations, seconds, seconds/iterations)


def checkPerformance(groups, request=clientRequest, rounds=ROUNDS):
	"""
	Tests the performance of the PRF under a list of groups
	"""
	prf = None
	w,t,m = clientRequest

	# No-arg function for timeit
	def query():
		clientQueryOprf(prf, w,t,m)

	# Run each group through the gauntlet
	for name, group in groups:
                set_dummy_z(group, OPRF=False)

		# Initialize the PRF with the specified group.
		prf = TaggedPrf(group)
		print "Testing-PRF {} for {} rounds".format(name, rounds)
		print timeit(query, number=rounds)
		print

                if (name, group) in oprf_groups:
                        prf = TaggedOprf(group, serialize=True)
                        set_dummy_z(group, OPRF=True)
                        print "Testing-OPRF {} for {} rounds".format(name, rounds)
                        print timeit(query, number=rounds)
                        print
                

# Run performance  testing
if __name__ == "__main__":
#    checkPerformance(groups)
    testPrfQuery()
    testPrfQuery(zkp=False)
