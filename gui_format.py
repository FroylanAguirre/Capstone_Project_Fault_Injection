#gui_format.py
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from ProjDirLblFr import *
import os

"""
Arranges all necessary frames for the top level window.
"""

class Gui_format(Frame):

    def __init__(self, master=None):
        #self.root = Tk()
        #self.root.title("Memory Stats")
        Frame.__init__(self, master)
        self.pack(fill="both")

        self.dirConfig = DirButtonsFr(self)

        self.proj_dir = ProjDirLblFr(self)

        self.glblVars = GlobalVarsDisplayLblFr(self)

        self.stackTable = StackTableLblFr(self)

        #might be used in future,not sure
        #self.funcNamePndWin = PanedWindow(self.stackLblFr, sashrelief="raised")
        #self.funcNamePndWin.pack(fill="x")

        #self.stackNameText = Text(self.stackLblFr)
        #self.stackNameText.insert(END, "Function name.\n")
        #self.funcNamePndWin.add(self.stackNameText)

        #self.funcFilePndWin = PanedWindow(self.stackLblFr, sashrelief="raised")
        #self.funcFilePndWin.pack(fill="x")

        #self.stackFileText = Text(self.stackLblFr)
        #self.stackFileText.insert(END, "Function file.\n")
        #self.funcNamePndWin.add(self.stackFileText)
