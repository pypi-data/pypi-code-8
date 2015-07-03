
#MODELS EXAMPLE 1

#import eventsim.models
#from eventsim.models import prob
#import eventsim.models as mo 

#from eventsim import manual --> manual.manuals(modulename)
#from eventsim.manual import manuals --> manuals(modulename)
#from eventsim.manual import manuals
from eventsim.models import *

#print(prob([1, 4, 9, 16], [0.1, 0.3, 0.9, 1.0])) - not tidy
#print(prob([1, 4, 9, 16], 
	#[0.1, 0.3, 0.9, 1.0])) - not bad

#a = outcome, b = cummulative probability
a = [1, 4, 9, 16]
b = [0.1, 0.3, 0.9, 1.0]

#if module imported as mo
#print("Probability:", mo.prob(a,b))

#if import eventsim.models
#print("Probability:", eventsim.models.prob(a,b))
print("\n SAMPLE1")
print("Probability:", prob(a,b))
print("discreteEmp:", discreteemp(a,b))
print("Expectation Value:", expectval(a,b))
print("Estimated Variance:", estvar(a,b))
print("Estimated Standard deviation:", eststddev(a,b))
print("Estimated Mean:", estmean(a,b))


print("\n SAMPLE2")

#optional arguments
print("discreteEmp:", discreteemp(a, b, 15))
print("Expectation Value:", expectval(a, b, 10))
print("Estimated Variance:", estvar(a, b, 9))
print("Estimated Standard deviation:", eststddev(a, b, 20))
print("Estimated Mean:", estmean(a,b, 9))

#View manual
#print(manuals("models")), print(manuals("randgen")), print(manuals("simevent"))
#print(manuals("models"))
#print(manual.manuals("models"))