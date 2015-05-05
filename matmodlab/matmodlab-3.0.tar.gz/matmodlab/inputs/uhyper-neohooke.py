#!/usr/bin/env mmd
from matmodlab import *

def main():

    E = 500.
    Nu = .45
    C10 = E / (4. * (1. + Nu))
    D1 = 6. * (1. - 2. * Nu) / E

    mps = MaterialPointSimulator("uhyper-neohooke")

    f = np.sin
    t = 0.
    n = 200
    dt = 2. * pi / n
    for i in range(n):
        t += dt
        mps.StrainStep(components=(f(t), 0, 0), increment=dt, frames=1, scale=.1)

    # set up the material
    parameters = [C10, D1]
    mps.Material("uhyper", parameters,
                 source_files=["uhyper.f90"],
                 source_directory="{0}/materials/abaumats".format(ROOT_D))

    # set up and run the model
    mps.run()

main()
