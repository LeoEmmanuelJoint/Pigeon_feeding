import tkinter as tk
##
# @brief Package adding styles to the GUI elements, as well as other elements
import tkinter.ttk as ttk
##
# @brief To generate a file selection window
from tkinter import PhotoImage

MyWindow = tk.Tk()
canvas = tk.Canvas(master=MyWindow, width=500, height=400, background='gray75')
canvas.pack()
#myimg = PhotoImage(file="AppleView_images\\apple_0.png")
#myimg = PhotoImage(file="PigeonView_images\\pigeon_flying.png")
myimg = PhotoImage(file="Test\\pigeon_asleep.png")
canvas.create_image(10, 10, image=myimg, anchor='nw')

MyWindow.mainloop()