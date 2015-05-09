#! /usr/bin/env python
from decida.Balloonhelp import Balloonhelp
from Tkinter import *
tk=Tk()
b=Button(text="OK", command=tk.quit) 
b.pack(padx=100, pady=100)
w=Balloonhelp(delay=100, background="#fcf87f", place="left", offset=3)
w.help_message(b, "display\n  tooltips")
tk.mainloop()
