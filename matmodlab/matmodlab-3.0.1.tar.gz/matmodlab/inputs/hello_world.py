#!/usr/bin/env python
from matmodlab import *

# set up the simulation
mps = MaterialPointSimulator("hello_world", output='exo')

# stress-controlled uniaxial strain to 1MPa in 25 steps
mps.MixedStep(components=(1.e6, 0., 0.), descriptors="SEE", frames=25)

# set up the material
parameters = {"K": 1.35e11, "G": 5.3e10}
mps.Material("elastic", parameters)

# run the simulation
mps.run()

mps.dump(['STRESS_XX', 'STRESS_YY'], format='mathematica')
mps.view()
