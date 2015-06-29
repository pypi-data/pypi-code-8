
#RANDGEN EXAMPLE 1

#from eventsim.randgen import generate
#from eventsim.randgen import *
#import eventsim.randgen as gen 
from eventsim.randgen import *


#sorted in ascending order with "s", 
#reverse sorted (descending order) with "r",
#unsorted with no last string argument

#Creates an instance of the generate class

#sample = generate() - all random options
#sample = generate("s")- sorted all random
#sample = generate(start, stop)
#sample = generate(start, stop, step, list-size, "optional")
sample1 = generate(0, 20, 2, 10, "s")

#if using the third import way
#sample1 = gen.generate(0, 10)

#Prints out result
print("\n SAMPLE 1")
print("outcome: ", sample1.outcome())
print("Unique: ", sample1.unique())
print("Occurrence: ", sample1.occur())
print("Probability: ", sample1.getprob())
print("Cummulative: ", sample1.getcum())


#RANDGEN EXAMPLE 2
sample2 = generate(0, 20, 10)

print("\n SAMPLE 2")
print("outcome: ", sample2.outcome())
print("Unique: ", sample2.unique())
print("Occurrence: ", sample2.occur())
print("Probability: ", sample2.getprob())
print("Cummulative: ", sample2.getcum())
