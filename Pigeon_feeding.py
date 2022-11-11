##
# @file Pigeon_feeding.py
# @author Léo-Emmanuel JOINT, student at the UQAC
# @author Latchoumi Praba MOGANE, student at the UQAC
# @date 15.10.2022

# @remark 
# In this program, the names of the elements are idetified with prefixes and suffixes
# - the Tkinter control variables are named with the suffix "_gui"
# - the Tkinter.ttk.Combobox elements are identified with the prefix "cbb_"
# - the Tkinter.ttk.Frame elements are identified with the prefix "f_"
# - the Tkinter.ttk.LabelFrame elements are identified with the prefix "lbf_"
# - the Tkinter.ttk.RadioButton elements are identified with the prefix "rbtn_"
# - the Tkinter.ttk.Checkbutton elements are identified with the prefix "chb_"
# - the Tkinter.ttk.Button elements are identified with the prefix "btn_"
# - the Tkinter.ttk.Label and Tkinter.Label elements are identified with the prefix "lbl_"
# - the Tkinter.ttk.Spinbox elements are identified with the prefix "spb_"

# Program that shows the GUI


##
# @brief To generate the GUI
import tkinter as tk
##
# @brief Package adding styles to the GUI elements, as well as other elements
import tkinter.ttk as ttk
##
# @brief To generate a file selection window
from tkinter import PhotoImage, filedialog
##
# @brief To manipulate images, and convert them into a version compatible with Tkinter
from PIL import Image, ImageTk
##
# @brief To manipulate arrays
import numpy as np
##
# @brief To navigate and search through the directories
import os
# @brief To measure the duration (for testing purposes)
import time

# STYLE

##
# @var s1 Theme to use in the interface (sets a style for each gui element)
# @remark Not all themes are avaliable depending on the distribution (Windows, Linux or Mac os)
s1 =ttk.Style()
#print("Available themes:", s1.theme_names()) #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative') on Windows 10
#print("Theme in use:", s1.theme_use()) # vista
s1.theme_use('clam') # Sets the theme




# CLASSES

class Element():

    def __init__(self, map, id, x, y):
        self.idElement = id
        self.type = None
        self.map = map
        self.posX = x
        self.posY = y
        self.exists = True
    
    def get_id(self):
        return(self.idElement)

class Pigeon(Element):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "pigeon"
        self.state = 1 #0 for asleep, 1 for static, 2 for flying

class PigeonFood(Element):
    
    def __init__(self, map, id, x, y, freshness=10):
        super().__init__(map, id, x, y)
        self.type = "pigeonFood"
        self.freshness = freshness # 10 -> fresh, 0 -> spoiled
        
class Map():
    def __init__(self, w=750, h=500):
        self.width = w # width in pixels
        self.height = h #height in pixels
        self.listElements = []
        self.numberOfPigeons = 4
        self.init_Pigeons()
    
    def init_Pigeons(self):
        n = self.numberOfPigeons
        w0 = self.width//n
        h0 = self.height//2
        for k in range(n):
            self.addPigeon(w0+(k*w0), h0)

    def get_max_id(self):
        return max([elt.get_id() for elt in self.listElements], default=0)
    
    def addPigeon(self, posx=0, posy=0):
        self.listElements.append(Pigeon(map=self, id=self.get_max_id(), x=posx, y=posy))
    
    def addFood(self, posx=0, posy=0):
        self.listElements.append(PigeonFood(map=self, id=self.get_max_id(), x=posx, y=posy))

### GUI PART

class ElementView():
    def __init__(self, id, posx, posy, type, canvasId):
        self.type = type
        self.view = None
        self.id = id
        self.x = posx
        self.y = posy
        self.canvasId = canvasId
    
    def update(self, element):
        pass
    
    def represents(self, element):
        return (self.id == element.get_id())
    
    def set_canvas_id(self, id):
        self.id = id

class PigeonView(ElementView):
    def __init__(self, path="PigeonView_images", **kwargs):
        super().__init__(type="Pigeon", **kwargs)
        self.type = "Pigeon"
        self.folder = path
        self.sleepingView = tk.PhotoImage(file=self.folder+"\\pigeon_asleep.png")
        self.staticView = tk.PhotoImage(file=self.folder+"\\pigeon_static.png")
        self.flyingView = tk.PhotoImage(file=self.folder+"\\pigeon_flying.png")
        self.view = self.staticView
    
    def update(self, element):
        match element.state:
            case 0:
                self.view = self.sleepingView
            case 1:
                self.view = self.staticView
            case 2:
                self.view = self.flyingView

class PigeonFoodView(ElementView):
    def __init__(self, path=None, type="Food", **kwargs):
        super().__init__(**kwargs)
        self.folder = path
        # A REFAIRE pour généraliser
        self.freshness10View = tk.PhotoImage(file=self.folder+"\\"+self.type+"_10.png")
        self.freshness8View = tk.PhotoImage(file=self.folder+"\\"+self.type+"_8.png")
        self.freshness6View = tk.PhotoImage(file=self.folder+"\\"+self.type+"_6.png")
        self.freshness4View = tk.PhotoImage(file=self.folder+"\\"+self.type+"_4.png")
        self.freshness2View = tk.PhotoImage(file=self.folder+"\\"+self.type+"_2.png")
        self.freshness0View = tk.PhotoImage(file=self.folder+"\\"+self.type+"_0.png")
        self.view = self.freshness10View

    def update(self, element):
        match element.state:
            case 0:
                self.view = self.freshness0View
            case 1 | 2:
                self.view = self.freshness2View
            case 3 | 4:
                self.view = self.freshness2View
            case 5 | 6:
                self.view = self.freshness2View
            case 7 | 8:
                self.view = self.freshness2View
            case 9 | 10:
                self.view = self.freshness2View

class AppleView(PigeonFoodView):
    def __init__(self, path="AppleView_images", **kwargs):
        super().__init__(path, type="apple", **kwargs)

class Interface(tk.Canvas):
    def __init__(self, map, **kwargs):
        self.map = map
        self.viewTab = [] # array containing the element and its id in the map
        self.createdFoodFreshness = 10
        super().__init__(width=self.map.width, 
                            height=self.map.height, 
                            background="#D9D9D9", **kwargs)
        self.init_display()
        self.update_display()
        self.bind("<Button-1>", self.create_food)
        self.bind("<Motion>", self.follow_mouse)

    def create_food(self, event):
        self.create_apple()

    def create_apple(self):
        self.map.addFood(self.lastx, self.lasty)
        # Ajouter la création effective de l'image
        #self.idMax = self.create_text(100, 100, text='Food', anchor='nw', font='TkMenuFont', fill='red')

    def follow_mouse(self, event):
        self.lastx, self.lasty = event.x, event.y
    
    def createPigeonView(self, pigeon):
        view = PigeonView(id=pigeon.get_id(), 
                            posx=pigeon.posX, 
                            posy=pigeon.posY,
                            canvasId=-1)
        id = self.create_image(view.x, view.y, 
                                anchor=tk.CENTER,
                                image=view.view)
        view.set_canvas_id(id)
        self.viewTab.append(view)
    
    def createPigeonFoodView(self, food):
        """ Creates the pigeon food view and shows it in the canvas """
        view = AppleView(food.id, 
                            freshness=self.createdFoodFreshness, 
                            posx=food.posX, 
                            posy=food.posY,
                            canvasId=-1)
        id = self.create_image(view.x, view.y, 
                                anchor=tk.CENTER,
                                image=view.view)
        view.set_canvas_id(id)
        self.viewTab.append(view)

    def createElementView(self, element):
        match element.type:
            case "pigeon":
                self.createPigeonView(element)
            case "pigeonFood":
                self.createPigeonFoodView(element)

    def init_display(self):
        for element in self.map.listElements:
            self.createElementView(element)

    def update_display(self):
        # Create the missing views based on the elements list
        for element in self.map.listElements:
            found = False
            for view in self.viewTab:
                if view.represents(element):
                    found = True
                    view.update(element)
            if not found:
                self.createElementView(element)


class Environment(tk.Canvas):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.idElement = self.create_text(0, 0, text='Food')
        self.bind("<Button-1>", self.create_food)
        self.bind("<Motion>", self.follow_mouse)

    def create_food(self, event):
        self.idElement = self.create_text(100, 100, text='Food', anchor='nw', font='TkMenuFont', fill='red')

    def follow_mouse(self, event):
        self.lastx, self.lasty = event.x, event.y
        self.moveto(self.idElement, self.lastx, self.lasty)

#root = tk.Tk()
#root.columnconfigure(0, weight=1)
#root.title("Click to drop food !")
#root.rowconfigure(0, weight=1)


MyWindow = tk.Toplevel()
MyWindow.title("Click to drop food !")
MyMap = Map()
MyDisplay = Interface(master=MyWindow, map=MyMap)
MyDisplay.pack()
#env = Environment(root)
#env.pack()

MyWindow.mainloop()
