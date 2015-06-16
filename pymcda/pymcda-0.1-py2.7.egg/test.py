from pymcda import *

SI=iomcda.inputFromTxt('data.csv')
print SI,SI['weight']
mat=SI['matrix']
WS=weightedsum.weightedsum(mat)
criteria=SI['criteria']
for i in range(len(criteria)-1):
	print i
	c=iomcda.extractColumn(SI,i)
	print min(c),max(c)
	cn=WS.increase(c)
	print c,cn