from ProjDirLblFr import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import numpy as np

"""
gui_format.py
Contains groups of Frame subclasses that setup gui elements for different tabs.
At this point, only Gui_format is used.
Planning on removing Gui_format. 
"""

class Gui_format(Frame):
    '''
    Gui_format
    Setups gui elements for "ProjectInfo" tab.
    '''

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill="both")

        self.dirConfig = DirButtonsFr(self)

        self.proj_dir = ProjDirLblFr(self)

        self.glblVars = GlobalVarsDisplayLblFr(self)

        self.stackTable = StackTableLblFr(self)


class Graph_Tab(Frame):

    def __init__(self, master=None):
        Frame.__init__(self)
        #self.pack(fill="both")

        fig = plt.figure(1, frameon=False)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(np.pi * t)
        plt.plot(t, s)
        canvas = FigureCanvasTkAgg(fig)
        #canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)


class Tcl_Interface_Tab(Frame):

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

        self.tclInput = Entry(buttonEntryFrame)
        #self.tclInput.bind("<Return>", self.exec_tcl_cmd)

        self.tclInput.pack(fill='x')


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill="both")

        self.create_button_entry_frame()
        self.create_text_scrollbar()