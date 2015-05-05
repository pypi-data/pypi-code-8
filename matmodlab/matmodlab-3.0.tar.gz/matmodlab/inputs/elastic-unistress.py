#!/usr/bin/env mmd
from matmodlab import *

def main():

    # setup the simulation
    mps = MaterialPointSimulator("elastic-unistress")

    # set up the driver
    x, N = -1e-6, 1000
    mps.StressStep(components=(1, 0, 0), scale=x, frames=N)
    mps.StressStep(components=(2, 0, 0), scale=x, frames=N)
    mps.StressStep(components=(1, 0, 0), scale=x, frames=N)
    mps.StressStep(components=(0, 0, 0), scale=x, frames=N)

    # set up the material
    parameters = {"K": 9.980040E+09, "G": 3.750938E+09}
    mps.Material("elastic", parameters)

    # run the simulation
    mps.run()
    mps.dump(format="ascii", variables=["STRESS", "STRAIN"])

main()
