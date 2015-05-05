#!/usr/bin/env mmd
import os
import numpy as np

from matmodlab import *
import matmodlab.utils.fileio as ufio
import matmodlab.utils.numerix.nonmonotonic as unnm

filename = os.path.join(get_my_directory(), "optimize_al.xls")
strain_exp, stress_exp = zip(*ufio.loadfile(filename, sheet="MML", disp=0,
                                            columns=["STRAIN_XX", "STRESS_XX"]))

def func(x=[], xnames=[], evald="", runid="", *args):
    mps = MaterialPointSimulator(runid)

    xp = dict(zip(xnames, x))
    NU = 0.32  # poisson's ratio for aluminum
    parameters = {"K": xp["E"]/3.0/(1.0-2.0*NU), "G": xp["E"]/2.0/(1.0+NU),
                  "Y0": xp["Y0"], "H": xp["H"], "BETA": 0.0}
    mps.Material("vonmises", parameters)

    # create steps from data. note, len(columns) below is < len(descriptors).
    # The missing columns are filled with zeros -> giving uniaxial stress in
    # this case. Declaring the steps this way does require loading the excel
    # file anew for each run
    mps.DataSteps(filename, steps=30, sheet='MML',
                  columns=('STRAIN_XX',), descriptors='ESS')

    mps.run()
    if not mps.ran:
        return 1.0e9

    strain_sim, stress_sim = zip(*mps.get("STRAIN_XX", "STRESS_XX"))
    error = unnm.calculate_bounded_area(strain_exp, stress_exp,
                                        strain_sim, stress_sim)
    return error

def runner(method, v=1):
    E = OptimizeVariable("E",  2.0e6, bounds=(1.0e5, 1.0e7))
    Y0= OptimizeVariable("Y0", 0.3e5, bounds=(1.0e4, 1.0e6))
    H = OptimizeVariable("H",  1.0e6, bounds=(1.0e4, 1.0e7))
    xinit = [E, Y0, H]

    optimizer = Optimizer("optimize_al", func, xinit, method=method,
                          maxiter=200, tolerance=1.e-3)
    optimizer.run()
    xopt = optimizer.xopt
    return xopt


if __name__ == "__main__":
    runner(["powell", "simplex", "cobyla"][1])
