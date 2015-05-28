import numpy as np
from mayavi import mlab
mlab.figure(1, bgcolor=(1, 1, 1))  # make a white figure
data = np.random.rand((10,10,10))
cp = mlab.contour3d(data)#, contours=contours, transparent=True,
                        #opacity=0.5, colormap='hot')
mlab.view(azimuth=155, elevation=70, distance='auto')
# Show the 3d plot:
mlab.show()
