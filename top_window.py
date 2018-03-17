from tkinter import *
from tkinter import ttk
from gui_format import *
from proj_stats import *

class Top_Frame(Frame):

    def __init__(self, master, tclPortObj, projectInfo, fi_info):

        Frame.__init__(self, master)
        self.pack(fill="both")

        tabber = ttk.Notebook(self)
        tabber.pack(fill="both")

        tab3 = projectInfo.create_gui(master)
        tabber.add(tab3, text="Directory Settings")

        #no masters specified since the line after takes care of that
        self.tab1 = Gui_format()
        tabber.add(self.tab1, text="ProjectInfo")

        #self.tab2 = Graph_Tab()
        #tabber.add(self.tab2, text="Empty Tab")

        # self.tab2 = tclPortObj.create_gui(master)
        # tabber.add(self.tab2, text='Tcl Terminal')

        tab4 = fi_info.create_gui(master)
        tabber.add(tab4, text="Fault Injection")

        # self.tab3 = Graph_Tab(self)
        # tabber.add(self.tab3, text="Graphs")

