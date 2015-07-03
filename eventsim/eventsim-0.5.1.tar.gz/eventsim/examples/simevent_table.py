#------------------------------------------
# you dont have to worry about anything (easiest and best way)
from eventsim.simevent import * 

#or else you have to import these if you dont import as all :
#from eventsim.simevent import simtable
#from eventsim.simevent import randomsim
# from tkinter import Tk, N, S, W, E
# from tkinter.ttk import Frame, Treeview

#or

#from eventsim.simevent import simtable
#from eventsim.simevent import randomsim
# from tkinter import *
# from tkinter.ttk import *

#first argument of the simtable class must always be your class to be displayed as a table followed by "Tk()" 
v = simulation([2,5,7,3,7])

#drawing the table by calling the class method
simtable(v, Tk()).drawtable()

w = randomsim(3,6)
simtable(w, Tk()).drawtable()