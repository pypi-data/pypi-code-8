

#from eventsim.simevent import randomsim
#from eventsim.simevent import simulation
#from eventsim.manual import manuals
from eventsim.simevent import *  #imports randomsim and simulation

#simulation is used to find all values when given one or two arguments
#randomsim calculates random vaues given the nuber of arguments to generate

# a = [10,6,2,10,7,4,3,8,10,6,2,6,2,7,9]
# b = [5,1,2,2,1,6,5,3,2,6,2,1,2,6,1]

#Create list to simplify class

#Not preferrable
#test1 = simulation([0,  3,  1,  1,  6,  3,  7,  5,  2,  4,  1], [4,  2,  3,  2,  3,  4,  2,  4,  5,  3,  4]) 

#Manageable
#test1 = simulation([0,  3,  1,  1,  6,  3,  7,  5,  2,  4,  1], 
	#[4,  2,  3,  2,  3,  4,  2,  4,  5,  3,  4])

#better
#a = inter-arrival time, b = service time
a = [0,  3,  1,  1,  6,  3,  7,  5,  2,  4,  1] 
b = [4,  2,  3,  2,  3,  4,  2,  4,  5,  3,  4]

#----- SIMULATION --------
print("TESTING SIMULATION")
print("\n  #TWO ARGUMENTS (Test 1)")
test1 = simulation(a,b)

print("    Interarrival time:", test1.intarrival())
print("    Service time:", test1.service())
print("    Arrival time:", test1.arrival())
print("    Time service begins:", test1.servbegin())
print("    Time service ends:", test1.servend())
print("    Wait time in queue:", test1.queuewait())
print("    Time customer spends in system:", test1.custspend())
print("    Idle time of server", test1.idle())

print("\n  #ONE ARGUMENT (Test 2)")
#----- Code for one arguments --------
#a = inter-arrival time, service time is randomly generated (values between 1 and 10)
test2 = simulation(a)

print("    Interarrival time:", test2.intarrival())
print("    Service time:", test2.service())
print("    Arrival time:", test2.arrival())
print("    Time service begins:", test2.servbegin())
print("    Time service ends:", test2.servend())
print("    Wait time in queue:", test2.queuewait())
print("    Time customer spends in system:", test2.custspend())
print("    Idle time of server", test2.idle())

#-------------------------------------------------------
#----- RANDOMSIIM --------
print("\n\nTESTING RANDOMSIM")
print("\n  #NO ARGUMENTS (Test 3)")

#populates random values into the inter-arrival and service time list to generate other results
test3 = randomsim()

print("    Interarrival time:", test3.intarrival())
print("    Service time:", test3.service())
print("    Arrival time:", test3.arrival())
print("    Time service begins:", test3.servbegin())
print("    Time service ends:", test3.servend())
print("    Wait time in queue:", test3.queuewait())
print("    Time customer spends in system:", test3.custspend())
print("    Idle time of server", test3.idle())

print("\n  #ONE ARGUMENTS (Test 4)")
#populates specified random values into the inter-arrival and service time list to generate other results
#but in this case 5 is the argument so it generates 5 random numbers in both list
test4 = randomsim(5)

print("    Interarrival time:", test4.intarrival())
print("    Service time:", test4.service())
print("    Arrival time:", test4.arrival())
print("    Time service begins:", test4.servbegin())
print("    Time service ends:", test4.servend())
print("    Wait time in queue:", test4.queuewait())
print("    Time customer spends in system:", test4.custspend())
print("    Idle time of server", test4.idle())

print("\n  #TWO ARGUMENTS (Test 5)")
#inter-arrival time and service time = populates values between 1 and args[0], args[1] times
#e.g. below populates inter-arrival time and service time with values between 1 and 3, 7 times
test5 = randomsim(5, 10)

print("    Interarrival time:", test5.intarrival())
print("    Service time:", test5.service())
print("    Arrival time:", test5.arrival())
print("    Time service begins:", test5.servbegin())
print("    Time service ends:", test5.servend())
print("    Wait time in queue:", test5.queuewait())
print("    Time customer spends in system:", test5.custspend())
print("    Idle time of server", test5.idle())


print("\n  #THREE ARGUMENTS (Test 6)")
#inter-arrival time = populates values between 1 and args[0], args[2] times
#service time = populates values between 1 and args[1], args[2] times
#e.g. below populates inter-arrival time with values between 1 and 4, 10 times
#and service time with values between 1 and 6, 10 times

test6 = randomsim(4, 6, 10)

print("    Interarrival time:", test6.intarrival())
print("    Service time:", test6.service())
print("    Arrival time:", test6.arrival())
print("    Time service begins:", test6.servbegin())
print("    Time service ends:", test6.servend())
print("    Wait time in queue:", test6.queuewait())
print("    Time customer spends in system:", test5.custspend())
print("    Idle time of server", test6.idle())

#View manual
#print(manuals("models")), print(manuals("randgen")), print(manuals("simevent"))
#print(manual.manuals("simevent"))
#print(manuals("simevent"))