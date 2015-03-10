#Bermillo-Madraso-Opiana

from tkinter import *
from tkinter import ttk
import tkinter as tk
import animeclash

    
minidiary =  Tk() #Get the root window
minidiary.title ('ANIME CLASH')
minidiary.geometry ("400x300")
minidiary.resizable (0,0)


img = PhotoImage (file = "anime.gif" )#Create the PhotoImage widget
w = img.width()
h = img.height()

def write_window():
        minidiary.destroy()
        animeclash.main()
        

   
panel1 = Label(minidiary, image = img)
panel1.pack(side = TOP, fill = BOTH, expand = YES)
panel1.configure(relief = RIDGE, borderwidth = 7, bg = "navyblue")

frame1 = Frame(panel1)
frame1.pack(side = LEFT, pady = 20, padx = 20)
frame2 = Frame(panel1)
frame2.pack(side = LEFT, pady = 20, padx = 20)

write_img = PhotoImage(file = "startgame.gif")
write_btn = Button(frame1, image = write_img, command = write_window)
write_btn.pack()
write_btn.configure(bg = "navyblue")
write_btn.image = write_img



read_img = PhotoImage(file = "quit.gif")
read_btn = Button(frame2, image = read_img, command = minidiary.destroy)
read_btn.pack()
read_btn.configure(bg = "navyblue")
read_btn.image = read_img
panel1.image = img

minidiary.mainloop ()
