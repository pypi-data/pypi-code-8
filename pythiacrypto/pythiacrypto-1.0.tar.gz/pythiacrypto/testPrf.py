#!/usr/bin/env python
"""
Test cases for our Delphi PRF protocol.
"""

from common import *
from taggedPrf import TaggedPrf
from tweakablePrf import TweakablePrf
from blspop import BlsPop
from ecoprf import EcOprf

from groups import *
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,pair
from random import randint
from random import _urandom as urandom
from charm.core.math import integer

# The groups we're testing against
groups = [zq128, ec192, ss512, mnt224]

prf_dict = {"PO-ECC": 1, "PO-BLS": 3, "UN-ECC": 5, "UN-BLS": 6}
SERIALIZE = 0
dp(SERIALIZE=SERIALIZE)
s = prf_dict['PO-BLS']-SERIALIZE
tweakablePrfs = [ 
    EcOprf(ec192, serialize=True),     # PO-ECC
    EcOprf(ec224, serialize=False),
    BlsPop(mnt224, serialize=True),    # PO-BLS
    BlsPop(mnt224, serialize=False),
    TaggedPrf(ec192, serialize=True),  # UN-ECC
    TaggedPrf(ec192, serialize=False),
    TaggedPrf(mnt224, serialize=True), # UN-BLS
    TaggedPrf(mnt224, serialize=False),
]#[s:s+1]

testTotal = 0

# Dummy values for faking a server.
DUMMY_SK = 98712349871234098712304987987123498712340987123049878763845761348576234857633        
DUMMY_Z  = 32987197801012098734089724097823405987134509873245098237450987450982734509872 


def testPassed():
    """
    Increments test total.
    """
    global testTotal
    testTotal += 1


#@profile
def queryPrf(prf, w, t, m, previousP=None):
    """
    Tests tweakable PRFs.
    """
    # Wrap the message and query
    r, x = prf.wrapMessage(m)
    (p, y, c, u, _) = prf.query(w, t, x, DUMMY_SK, DUMMY_Z)

    # Verify the proof and unwrap the result
    prf.verifyZkp(w, t, x, p, y, c, u, previousP)
    yPrime = prf.unwrapResponse(r, y)
    return (p, yPrime)


def checkStableTweakable(prf, w, t, m, rounds):
    """
    Tests a tweakable @prf by running the same message through over many
    @rounds. The outputs should be identical.
    """
    # Results from previous runs
    firstResult = None
    previousP = None

    for _ in range(rounds):
        (p, y) = queryPrf(prf, w, t, m, previousP)

    # Cache the first reported server public key for ID w
    if previousP is None:
        previousP = p

    # Verify the results are stable
    if firstResult is None:
        firstResult = y
    else:
        assert y == firstResult, "Error with unblinded result.\n"\
            "Saw:      {0}\n"\
            "Expected: {1}".format(y, firstResult)


def testTweakableStable():
    """
    Tests the tweakable PRFs over a series of different inputs to 
    ensure outputs are stable.
    """
    # Inputs for our tests.
    params = [
        (1, 2, 3456789), 
        (908173498712390487234, 17329487091283749872134, 87654), 
        (98712394087234, 8976987612394876, 68727869176893468705), 
        (-10000, 12304987, 87123487923457893478934189714), 
        (97823904857, -1938475987, 0), 
        (97823904857, -1938475987, 817234)
    ]
    params = params * 1
    # Test each PRF
    for prf in tweakablePrfs:
        # Run each set of inputs a series of times    
        for w,t,m in params:
            checkStableTweakable(prf,w,t,m, rounds=10)
            testPassed()


def clientQueryPrf(prf, w, t, m, previousP=None):
    # Run the query and verify the ZKP.
    (p, y, c, u, _) = prf.query(w, t, m, DUMMY_SK, DUMMY_Z)
    prf.verifyZkp(w, t, m, p, y, c, u, previousP)
    return (p, y)


def checkStable(prf, w, t, m, rounds, OPRF=False):
    """
    Tests the OPRF by running the same message through the OPRF over many 
    @rounds. The outputs should be stable.
    """
    # Results from previous runs
    firstResult = None
    previousP = None

    for _ in range(rounds):
        (p, y) = clientQueryPrf(prf, w, t, m, previousP)

    # Cache the first reported server public key for ID w
    if previousP is None:
        previousP = p

    # Verify the results are stable
    if firstResult is None:
        firstResult = y
    else:
        assert y == firstResult, "Error with unblinded result.\n"\
            "Saw:      {0}\n"\
            "Expected: {1}".format(y, firstResult)


def testStablePRF(group):
    """
    Tests the PRF protocol with the specified @group to assure results are 
    deterministic over a selection of different parameters.
    """
    # Inputs for our tests.
    params = [
        (1, 2, 3456789), 
        (908173498712390487234, 17329487091283749872134, 87654), 
        (98712394087234, 8976987612394876, 68727869176893468705), 
        (-10000, 12304987, 87123487923457893478934189714), 
        (97823904857, -1938475987, 0), 
        (97823904857, -1938475987, 817234)
    ]

    # Test the tagged PRF protocol with the specified group
    prf = TaggedPrf(group)

    # Run each set of inputs a series of times
    for w,t,m in params:
        checkStable(prf,w,t,m, rounds=10)
        testPassed()


def testPrf():
    """
    Tests the PRF protocol for deterministc output (and valid ZKPs)
    using against each of our testing groups.
    """
    for G in groups:
        testStablePRF(G)


def testPrfSerialized():
    """
    Tests the PRF protocol with each group with serialization requested.
    """
    # Inputs for our tests.
    w,t,m = ("client ID ", ";lkjasdf", "Fancy message")

    for group in groups:
        prf = TaggedPrf(group, serialize=True)
        (p, y) = clientQueryPrf(prf, w,t,m)
        assert p and y, "Received invalid values from PRF"
        testPassed()


def testHashZq():
    """
    Tests that the PrimerOrderGroup hash function produces unique results 
    for different inputs.
    """
    inputs = [123, (123, 456), 123456, -987234, (-9876234, 345, 1234) ]

    # Maps hash results to their inputs
    values = {}

    # Test all inputs
    for a in inputs:
        if isinstance(a, tuple):
            result = zq128.hashG(*a)
        else:
            result = zq128.hashG(a)

        assert result, "Invalid hash result {0} for inputs {1}".format(result, a) 

        # Convert to string representation
        result = str(result)

        # Check for this result.
        assert result not in values, "Seen the same hash result {0} more than "\
            "once, for inputs [{1}] and [{2}].".format(result, a, 
            values[result])

        # remember this result
        values[str(result)] = a

    testPassed()


def testSerialization():
    """
    Test serialization of each group multiple times.
    """
    rounds = 5

    for G in groups:
        for _ in range(rounds):

            # BLSGroup.random() takes a special keyword. :/
            if isinstance(G, BLSGroup):
                x = G.random(G1)
            else:
                x = G.random()

            serializationRoundTrip(G, x)

        # Success!
        testPassed()


def serializationRoundTrip(group, x):
    """
    Run an element @x through the PRF serialization and deserialization routines
    and ensure that we get the original item back.
    """
    prf = TaggedPrf(group, serialize=True)
    s = prf.serialize(x)
    x2 = prf.deserialize(s)
    assert x == x2, "Serialization failed. Original: {}\nSerialized: {}\n"\
        "Deserialized: {}".format(x, s, x2)

    # Try again with serialization disabled.
    prf = TaggedPrf(group, serialize=True)
    s = prf.serialize(x)
    x2 = prf.deserialize(s)
    assert x == x2, "Serialization failed. Original: {}\nSerialized: {}\n"\
        "Deserialized: {}".format(x, s, x2)


def testServerKeyRotation():
    """
    Tests key rotation process when server changes it's secret key.
    """
    for G in groups:
        serverKeyRotate(G)  


def serverKeyRotate(group):
    """
    Tests key rotation process when server changes it's secret key.
    """
    prf = TaggedPrf(group)

    # Sample test parameters
    w,t,m,z,sk1,sk2 = ("client ID", "tweak", "message", "fixedZ", 
            "Secret Key 1 - lkhasldkjfhasd;fkj", 
            "Secret Key 2 - lkhjasdlkjasdf")


    # Initial query with sk1
    (p,y,c,u,e) = prf.query(w,t,m,sk1,z)
    prf.verifyZkp(w,t,m,p,y,c,u)

    # Second query
    (p2,y2,c2,u2,e2) = prf.query(w,t,m,sk2,z)
    prf.verifyZkp(w,t,m,p2,y2,c2,u2)

    # Sanity check that core values differ
    assert p != p2 and y != y2 and e != e2, \
        "Error: unexpected matching values after server key rotation."

    # Get and apply delta to find matching values.
    delta = prf.delta(e2, w, sk1, z)
    updatedY = prf.applyDelta(y, delta)

    assert y2 == updatedY, "Updated y-value does not match expected value.\n"\
        "y:                  {}\n"\
        "delta:              {}\n"\
        "y2:                 {}\n"\
        "updatedY = y^delta: {}\n".format(y, delta, y2, updatedY)

    testPassed()


def testHashAllProperties(group):
    """
    Tests that the PrimerOrderGroup hash function produces unique results 
    for different inputs.
    """
    inputs = [123, (123, 456), 123456, -987234, (-9876234, 345, 1234), 
              (1), (1, 1), (11, 1), (1, 11), (1, 1, 1),
              [randint(1,10**9-1) for _ in xrange(100)], 
    ]

    # Maps hash results to their inputs
    values = {}

    # Test all inputs
    for a in inputs:
        if isinstance(a, tuple) or isinstance(a, list):
            result = group.hashG(*a)
        else:
            result = group.hashG(a)

        assert result, "Invalid hash result {0} for inputs {1}".format(result, a) 

        # Convert to string representation
        result = str(result)

        # Check for this result.
        assert result not in values, "Seen the same hash result {0} more than "\
                "once, for inputs [{1}] and [{2}] in Group {3}.".format(result, a, values[result], group)

        # remember this result
        values[str(result)] = a

        
    # check stability
    for a in inputs:
        if isinstance(a, tuple) or isinstance(a, list):
            result = group.hashG(*a)
        else:
            result = group.hashG(a)

        # Convert to string representation
        result = str(result)
        # Check for this result.
        assert result in values, "Cound not see the same hash result for {1}"\
            .format(result, a, values[result])

    global testTotal
    testTotal += 1


def testHash():
    for group in groups:
        testHashAllProperties(group)


# Run each of our tests
if __name__ == "__main__":
    testTweakableStable()
    # testServerKeyRotation()
    # testHash()
    testPrf()
    # testSerialization()
    # testPrfSerialized()
    print "{0} tests passed!".format(testTotal)
