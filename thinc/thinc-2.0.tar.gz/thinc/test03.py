 #!/usr/bin/env python
from __future__ import unicode_literals
import numpy 
import time 

try: 
    import numpy.core._dotblas 
    print('Using ATLAS:') 
except ImportError: 
    print('No ATLAS:') 

n_in = 10*64+10*32+10*32
n_h1 = 100
n_h2 = 100
n_out = 80

in_ = numpy.random.random((n_in,1)) 
h1_in = numpy.random.random((n_in,n_h1)) 
h1_out = numpy.random.random((n_h1,)) 
h2_in = numpy.random.random((n_h1,n_h2)) 
h2_out = numpy.random.random((n_out,)) 
out = numpy.random.random((n_h2, n_out)) 
t = time.time() 
h1_in *= in_
h2_in *= h1_out
out *= h2_out

print(out.sum()) 
# S = numpy.matrix(numpy.diag(s)) 
# # y = U * S * V 
# #print(y.shape) 
#
print(time.time()-t) 
