from cno import SIF, CNOGraph

model = CNOGraph(cnodata("PKN-ToyMMB.sif"), cnodata("MD-ToyMMB.csv"))
pkn = c.copy()

model.preprocessing()
import numpy as np


# so from matlab.
sol = """reaction1 0 1. 0. 1 0 1 EGF Ras
   reaction2 0 1. 0. 1 0 1 EGF PI3K
   reaction3 0 1. 0. 1 0 1 TNFa PI3K
   reaction4 0 1. 0. 1 0 1 TNFa TRAF6
   reaction5 0 1. 0. 1 0 1 TRAF6 NFkB
   reaction6 0 1. 0. 1 0 1 TRAF6 p38
   reaction7 0 1. 0. 1 0 1 TRAF6 Jnk
   reaction8 0 1. 0. 1 0 1 Jnk cJun
   reaction9 0 1. 0. 1 0 1 p38 Hsp27
  reaction10 0 1. 0. 1 0 1 PI3K Akt
  reaction11 0 1. 0. 1 0 1 Ras Raf
  reaction12 0 1. 0. 1 0 1 Raf Mek
  reaction13 0 1. 0. 0 1 1 Akt Mek
  reaction14 0 1. 0. 1 0 1 Mek p90RSK
  reaction15 0 1. 0. 1 0 1 Mek Erk
  reaction16 0 1. 0. 1 0 1 Erk Hsp27
"""
sol_processed = """
reaction1 0 1. 0. 1 0 1 EGF PI3K
reaction2 0 1. 0. 1 0 1 TNFa PI3K
reaction3 0 1. 0. 1 0 1 TNFa NFkB
reaction4 0 1. 0. 1 0 1 TNFa Jnk
reaction5 0 1. 0. 1 0 1 Jnk cJun
reaction6 0 1. 0. 1 0 1 TNFa Hsp27
reaction7 0 1. 0. 1 0 1 PI3K Akt
reaction8 0 1. 0. 1 0 1 EGF Raf
reaction9 0 1. 0. 1 0 1 Raf Mek
reaction10 0 1. 0. 0 1 1 Akt Mek
reaction11 0 1. 0. 1 0 1 Mek p90RSK
reaction12 0 1. 0. 1 0 1 Mek Erk
reaction13 0 1. 0. 1 0 1 Erk Hsp27
reaction14 0 1. 0. 2 0 1 EGF TNFa PI3K
reaction15 0 1. 0. 1 1 1 Raf Akt Mek
reaction16 0 1. 0. 2 0 1 TNFa Erk Hsp27
"""


def cno2ilp(data):
    # more or less same implmenetation as matlab CNO2ILP or debugging but could be simplify !!!

    nR = len(data.reactions)

    # max number of species in a reactions (LHS)
    # could be simplified ? 
    #maxInputs = abs(numpy.min(numpy.sum(numpy.matrix(model.interMat), axis=0)-1))
    #inhibitions = numpy.zeros((maxInputs, nR))

    LHS = [x.split("=")[0] for x in list(data.reactions)]
    RHS = [x.split("=")[1] for x in list(data.reactions)]
    [x.split("+") for x in LHS]

    counter = 1
    for lhs, y in zip(LHS, RHS):
        species = [x for x in lhs.split("+")]
        nSpecies = len(species) + 1

        nI = len([z for z in species if z.startswith("!")])
        nA = len([z for z in species if z.startswith("!")==False])
        assert nA+nI == nSpecies - 1 
        print('reaction%s 0 1. 0.' %(counter)),
        print('%s %s 1' % (nA, nI,)),
        for specy in species:
            if specy.startswith("!"):
                print(specy[1:]),
            else:
                print(specy),
        print(y)
        counter += 1



cno2ilp(model)
print sol_processed
