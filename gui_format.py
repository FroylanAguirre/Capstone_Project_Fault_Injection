from tkinter import filedialog
from tkinter import *
import os

class Gui_format:

    def __init__(self):
        self.root = Tk()
        self.root.title("Memory Stats")
        self.buttonFrame = Frame()
        self.buttonFrame.pack()

        self.projDirButton = \
            Button(self.buttonFrame,
                   text="Project File",
                   takefocus=0)
        self.projDirButton.pack(side=LEFT)

        self.redoButton = \
            Button(self.buttonFrame,
                   text="Update",
                   takefocus=0)
        self.redoButton.pack(side=LEFT)

        self.pathname = StringVar()
        self.pathname.set("No project file selected.")
        #self.pathname.trace("w", projectInfo)

        self.pathLabel = Label(self.root, textvariable=self.pathname, anchor=W)
        self.pathLabel.pack(fill="both")


        self.gblLblFr = LabelFrame(self.root, labelanchor="nw",
                                    text="Globals", padx=10, pady=5)
        self.gblLblFr.pack(fill="both")

        self.globalText = Text(self.gblLblFr, font='Consolas')
        self.globalText.pack(fill="both")
        self.globalText.insert(END, "This is a text box.\n")

        self.stackLblFr = LabelFrame(self.root, labelanchor="nw",
                                    text="Function Stack Use", padx=10, pady=5)
        self.stackLblFr.pack(fill="both")

        #self.stackText = Text(self.stackLblFr)
        #self.stackText.pack(fill="both")
        #self.stackText.insert(END, "Stack info here.\n")

        self.funcNamePndWin = PanedWindow(self.stackLblFr, sashrelief="raised")
        self.funcNamePndWin.pack(fill="x")

        self.stackNameText = Text(self.stackLblFr)
        self.stackNameText.insert(END, "Function name.\n")
        self.funcNamePndWin.add(self.stackNameText)

        self.funcFilePndWin = PanedWindow(self.stackLblFr, sashrelief="raised")
        self.funcFilePndWin.pack(fill="x")

        self.stackFileText = Text(self.stackLblFr)
        self.stackFileText.insert(END, "Function file.\n")
        self.funcNamePndWin.add(self.stackFileText)

    def updateFileLabel(self, path):
        if (path != None):
            self.pathname.set(path)
        else:
            self.pathname.set("Invalid project file selected.")