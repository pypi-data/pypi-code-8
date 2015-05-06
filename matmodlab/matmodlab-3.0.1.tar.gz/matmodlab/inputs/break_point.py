#!/usr/bin/env python
from matmodlab import *

mps = MaterialPointSimulator("break_point")

# stress-controlled uniaxial strain to 1MPa in 25 steps
mps.MixedStep(components=(1.e6, 0., 0.), descriptors="SEE", frames=25)

# set up the material
parameters = {"K": 1.35e11, "G": 5.3e10}
mps.Material("elastic", parameters)

# set up and run the model
mps.break_point("time>.5 and stress_xx >= .5e6")
mps.run()
