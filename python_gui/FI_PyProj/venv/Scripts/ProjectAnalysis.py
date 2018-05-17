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
        self.f = None
        self.a = None
        self.canvas = None

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

    def sample_file_subframe(self, master):
        self.sample_file = StringVar()
        self.sample_file_name = StringVar()

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
        plot_frame = LabelFrame(master, text="Analysis Plots")
        plot_frame.pack(fill="both")
        # plot_frame.grid(row=1, column=
        button1 = Button(plot_frame, text="Print Plot", command=self.print_plots)
        button1.pack(anchor='e', side='left', padx=10, pady=5)

        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        self.canvas = FigureCanvasTkAgg(self.f, plot_frame)
        tkagg.NavigationToolbar2TkAgg(self.canvas, plot_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)


    def print_plots(self):
        print("yess")
        p = SampleParser()

        print("sample_file.get(): ", self.sample_file.get())
        file = self.sample_file.get()
        plot_list = p.parse_sample_file(file)
        print("plot_list: ", plot_list)
        print("lkjsadflkj")

        if len(plot_list[0]) > 0 :
            self.f.delaxes(self.a)
            self.a = self.f.gca(projection='3d')
            self.a.plot_trisurf(plot_list[0], plot_list[1], plot_list[2], cmap='viridis', edgecolor='none')



            # self.f.delaxes(self.a)
            # self.a = self.f.add_subplot(111)
            # self.a.plot([1, 4, 2, 34, 5, 9, 4, 11], [33, 32, 7, 3, 4, 9, 7, 5])
            self.canvas.show()
            self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

