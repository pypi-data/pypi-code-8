from Tkinter import *
import os

def pre():
    os.system("omxplayer before.mp4")

def rules():
    os.system("omxplayer rules.mp4")

def run():
    os.chdir("..")
    os.chdir("majestic-pi")
    os.system("python start.py")
    master.destory()



master = Tk()
master.title("Majestic Pi Essentials.")

label = Label(master, text="Majestic Pi.", font=("Helvetica", 45))
label.grid(column=2, row=1)

label1 = Label(master, text="Run Pre-Film Adverts:", font=("Helvetica", 20))
button1 = Button(master, text="Click Here!", command=pre)
label1.grid(row=2, column=2)
button1.grid(row=2, column=3)

label2 = Label(master, text="Run Theatre Rules:", font=("Helvetica", 20))
button2 = Button(master, text="Click Here!", command=rules)
label2.grid(row=3, column=2)
button2.grid(row=3, column=3)
label3 = Label(master, text="Run Majestic Pi:", font=("Helvetica", 20))
button3 = Button(master, text="Click Here!", command=run)
label3.grid(row=4, column=2)
button3.grid(row=4, column=3)
