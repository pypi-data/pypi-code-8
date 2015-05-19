import numpy
import numpy.random

from algopy import UTPM, Function, CGraph, sum, zeros, diag, dot, qr, trace



D,P,N,M = 2,3,4,5

X = numpy.random.rand(N, N)
Y = numpy.random.rand(N, N) * 1j

cg = CGraph()

FX = Function(X)
FY = Function(Y)

FZ = trace(dot(FY, X))

cg.independentFunctionList = [FY]
cg.dependentFunctionList = [FZ]

cg.gradient(Y)
