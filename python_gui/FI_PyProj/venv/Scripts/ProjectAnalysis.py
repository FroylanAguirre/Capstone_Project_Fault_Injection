from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.backends.backend_tkagg as tkagg
from mpl_toolkits import mplot3d
from tkinter import filedialog
import os
import xml.etree.ElementTree as ET
from SampleParser import SampleParser

class ProjectAnalysisPage:

    def __init__(self, proj_info):
        self.project = proj_info
        self.project_name = None  # StringVar()
        self.sample_file = None
        self.sample_file_name = None
        self.sample_analysis_file = None
        self.f1 = None
        self.a1 = None
        self.canvas1 = None
        self.f2 = None
        self.a2 = None
        self.canvas2 = None
        self.f3 = None
        self.a3 = None
        self.canvas3 = None

    def create_gui(self, master):
        analysisFrame = Frame(master)
        analysisFrame.pack(fill="both")

        self.sample_file_subframe(analysisFrame)
        self.analysis_plots_subframe(analysisFrame)

        return analysisFrame

    def get_sample_file(self):
        dir_path = filedialog.askopenfilename(title="Select Sample File")

        if dir_path:
            self.sample_file.set(dir_path)
            print("filename: ", os.path.split(dir_path)[-1])
            self.sample_file_name.set(os.path.split(dir_path)[-1])

        proj_name = self.sample_file_name.get()[:-4]
        self.sample_analysis_file.set("".join(os.path.split(dir_path)[:-1]) + "/" + proj_name + ".sa")
        print("sample_analysis_file: ", self.sample_analysis_file.get())

    def sample_file_subframe(self, master):
        self.sample_file = StringVar()
        self.sample_file_name = StringVar()
        self.sample_analysis_file = StringVar()

        self.sample_file.set(self.project.sample_dir.get())

        file_frame = LabelFrame(master, text="Sample File")
        file_frame.pack(fill="both", padx=10)
        # file_frame.grid(row=0, column=0)

        dialog_frame = Frame(master)
        dialog_frame.pack(fill='both', side='top')

        file_name_frame = Frame(master)
        file_name_frame.pack(side='top')


        sample_file_label = Label(dialog_frame, text="Choose sample file: ")
        sample_file_label.pack(anchor='w', side='left', padx=5, pady=5)
        sample_file_entry = Entry(dialog_frame, textvariable=self.sample_file)
        sample_file_entry.pack(anchor='e', expand=1, fill='x', side='left')
        button1 = Button(dialog_frame, text="...", command=self.get_sample_file)
        button1.pack(anchor='e', side='left', padx=10, pady=5)

        file_name_label = Label(file_name_frame, text="Sample file name: ")
        file_name_label.pack( side='left', padx=15, pady=15)
        file_name = Label(file_name_frame, textvariable=self.sample_file_name)
        file_name.pack( side='left', padx=15, pady=15)

    def analysis_plots_subframe(self, master):
        plotter_frame = LabelFrame(master, text="Analysis Plots")
        plotter_frame.pack(fill="both")

        button1 = Button(plotter_frame, text="Print Plot", command=self.print_plots)
        button1.pack(anchor='n', side='top', padx=10, pady=5)

        plots_frame = Frame(plotter_frame)
        plots_frame.pack(fill="both", expand=True)


        plot1_frame = Frame(plots_frame)
        # plot1_frame.pack(fill="both", expand=True, anchor='e', side='top')
        plot1_frame.grid(row=0, column=0, sticky="nw")

        plot2_frame = Frame(plots_frame)
        plot2_frame.grid(row=0, column=1, sticky="ne")
        # plot2_frame.pack(fill="both", expand=True, anchor='w', side='top')


        # initialize plot1
        self.f1 = Figure(figsize=(4, 4), dpi=100)
        self.a1 = self.f1.add_subplot(111)
        self.a1.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5], 'g')

        self.canvas1 = FigureCanvasTkAgg(self.f1, plot1_frame)
        tkagg.NavigationToolbar2TkAgg(self.canvas1, plot1_frame)
        self.canvas1.show()
        self.canvas1.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        # initialize plot2
        self.f2 = Figure(figsize=(4, 4), dpi=100)
        self.a2 = self.f2.add_subplot(111)
        self.a2.plot([1, 2, 4, 5, 8, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5], 'b')

        self.canvas2 = FigureCanvasTkAgg(self.f2, plot2_frame)
        tkagg.NavigationToolbar2TkAgg(self.canvas2, plot2_frame)
        self.canvas2.show()
        self.canvas2.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)


    def print_plots(self):
        print("yess")
        p = SampleParser()

        print("sample_file.get(): ", self.sample_file.get())
        sample_file = self.sample_file.get()
        analysis_file = self.sample_analysis_file.get()
        print("analysis file: ", analysis_file)
        plot_list = p.parse_sample_file(sample_file, analysis_file)

        print("plot_list: ", plot_list)
        print("lkjsadflkj")

        if len(plot_list[0]) > 0 :
            self.f1.delaxes(self.a1)
            self.a1 = self.f1.gca(projection='3d')
            self.a1.plot_trisurf(plot_list[0], plot_list[1], plot_list[2], cmap='viridis', edgecolor='none')

            self.canvas1.show()
            self.canvas1.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

            self.f2.delaxes(self.a2)
            self.a2 = self.f2.gca(projection='3d')
            self.a2.plot_trisurf(plot_list[0], plot_list[1], plot_list[3], cmap='viridis', edgecolor='none')

            self.canvas2.show()
            self.canvas2.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)


