#gui_format.py
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import tkinter as tk
from ProjDirLblFr import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import numpy as np

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


class Graph_Tab(Frame):

    def __init__(self, master=None):
        Frame.__init__(self)
        #self.pack(fill="both")

        # fig = plt.figure(1, frameon=False)
        # t = np.arange(0.0, 3.0, 0.01)
        # s = np.sin(np.pi * t)
        # plt.plot(t, s)
        # # canvas = FigureCanvasTkAgg(fig)
        # #canvas.show()
        # # canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class Tcl_Interface_Tab(Frame):

    # def exec_tcl_cmd(self, event):
    #     line = self.tclInput.get()
    #     print("input: ", line)
    #     self.tclInput.delete(0, END) #clear buffer
    #     self.tclTerminal.config(state=NORMAL)
    #     self.tclTerminal.insert(END, '\n')
    #     self.tclTerminal.insert(END, line)
    #     self.tclTerminal.config(state=DISABLED)

    def printToTclTerminal(self, msg):
        self.tclInput.delete(0, END)  # clear buffer
        self.tclTerminal.config(state=NORMAL)
        self.tclTerminal.insert(END, '\n')
        self.tclTerminal.insert(END, msg)
        self.tclTerminal.config(state=DISABLED)


    def create_text_scrollbar(self):
        txtScrollFrame = Frame(self)
        txtScrollFrame.pack(fill="both", expand=1)
        self.tclTerminal = Text(txtScrollFrame, font='Consolas')

        txtScroll = Scrollbar(txtScrollFrame, orient=VERTICAL, command=self.tclTerminal.yview)
        self.tclTerminal['yscroll'] = txtScroll.set

        self.tclTerminal.pack(side="left", expand=1, fill='both')
        #_in is needed so that scroll bar is seen in a half-window <->
        txtScroll.pack(side="right", fill='y', in_=self.tclTerminal)

        self.tclTerminal.insert(END, "Tcl interface on port 6666.\n")
        self.tclTerminal.config(state=DISABLED)

    def create_button_entry_frame(self):
        buttonEntryFrame = Frame(self)
        buttonEntryFrame.pack(fill="x")

        self.tclPortConnect = Button(buttonEntryFrame,
                                text="Tcl Port Connect",
                                takefocus=0)
        self.tclPortConnect.pack()
        self.tclGetRuntime = Button(buttonEntryFrame,
                                    text="get runtim",
                                    takefocus=0)
        self.tclGetRuntime.pack()

        self.tclInput = Entry(buttonEntryFrame)
        #self.tclInput.bind("<Return>", self.exec_tcl_cmd)

        self.tclInput.pack(fill='x')


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill="both")

        self.create_button_entry_frame()
        self.create_text_scrollbar()



