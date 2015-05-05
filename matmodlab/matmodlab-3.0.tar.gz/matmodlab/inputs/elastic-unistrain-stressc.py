#!/usr/bin/env mmd
from matmodlab import *

def main():

    # set up the simulator
    mps = MaterialPointSimulator("elastic-unistrain-stressc")

    # set up the steps
    N = 100
    mps.StressStep(components=(-7490645504, -3739707392, -3739707392), frames=N)
    mps.StressStep(components=(-14981291008, -7479414784, -7479414784), frames=N)
    mps.StressStep(components=(-7490645504, -3739707392, -3739707392), frames=N)

    # set up the material
    parameters = {"K": 9.980040E+09, "G": 3.750938E+09}
    mps.Material("elastic", parameters)

    # run the model
    mps.run()

    mps.dump(variables=["STRESS", "STRAIN"], format="ascii", ffmt="12.6E")

main()
