import numpy

def mulScalVec (scal, vec):
	return [scal * coord for coord in vec]
	
def addScalVec (scal, vec):
	return [scal + coord for coord in vec]
		
def mulVec (vec0, vec1):
	return [pair [0] * pair [1] for pair in zip (vec0, vec1)]
	
def addVec (*vecs):
	return [sum (aTuple) for aTuple in zip (*vecs)]

def subVec (vec0, vec1):
	return [pair [0] - pair [1] for pair in zip (vec0, vec1)]
	
def squaredDist (vec0, vec1):
	return sum (map (lambda coord: coord * coord , subVec (vec0, vec1)))
	
def vecsFromNp (vecsNp):
	return vecsNp.T.tolist ()
	
def vecFromNp (vecsNp, index = 0):
	return vecsFromNp (vecsNp) [index]
	
	
	
	