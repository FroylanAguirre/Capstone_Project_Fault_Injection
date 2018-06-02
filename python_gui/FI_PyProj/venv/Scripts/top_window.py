from tkinter import *
from tkinter import ttk
from gui_format import *
from proj_stats import *
from mem_map_canvas import MemoryMapCanvas

class Top_Frame(Frame):

    def __init__(self, master, tclPortObj, projectInfo, fi_info, proj_analysis):

        Frame.__init__(self, master)
        self.pack(fill="both")

        tabber = ttk.Notebook(self)
        tabber.pack(fill="both")

        tab3 = projectInfo.create_gui(master)
        tabber.add(tab3, text="Directory Settings")

        # no masters specified since the line after takes care of that
        self.tab1 = Gui_format()
        tabber.add(self.tab1, text="ProjectInfo")

        # self.tab2 = Graph_Tab()
        # tabber.add(self.tab2, text="Empty Tab")

        self.tab2 = tclPortObj.create_gui(master)
        tabber.add(self.tab2, text='Tcl Terminal')

        self.tab4 = fi_info.create_gui(master)
        tabber.add(self.tab4, text="Fault Injection")

        tab5 = proj_analysis.create_gui(master)
        tabber.add(tab5, text="Failure Analysis")

        # sample_frame = LabelFrame(tab4, text="Sampling Stuff")
        # sample_frame.grid(row=0, column=1)

        # self.tab3 = Graph_Tab(self)
        # tabber.add(self.tab3, text="Graphs")


