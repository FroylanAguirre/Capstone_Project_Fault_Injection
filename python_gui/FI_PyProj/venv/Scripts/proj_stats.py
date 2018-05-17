from tkinter import filedialog
from tkinter import *
import os
from tkinter import Frame
import re
from tkinter import filedialog
from HeapVariables import HeapVariables
from gui_format import Gui_format
from fault_injection_stats import FaultInjectionStats
# from gui_format import DirSettings

REQ_PROJECT_DIR_LIST = (".settings", "Debug",
                        "Drivers", "Inc",
                        "Src", "startup")

class Proj_Stats:

    def __init__(self):
        self.projPath = "" # path to top project dir (top dir on Project View in Eclipse)
        #self.projPath.trace("w",self.isValidProject())
        self.isValidProj = False # true if projPath is a valid path
        self.config_sampling_dir = None
        self.sample_dir = None
        self.openocdExe_dir = None
        self.heap_vars = HeapVariables() # a list of heap variables and their info

    def set_project_path(self, dir_path):
        self.projPath = dir_path
        self.heap_vars.set_output_map_path(os.path.join(self.projPath, "Debug/output.map"))

    @property
    def check_ready_for_config_creation(self):
        if len(self.config_sampling_dir.get()) == 0:
            print(1)
            return False
        if len(self.sample_dir.get()) == 0:
            print(2)
            return False
        if len(self.openocdExe_dir.get()) == 0:
            print(3)
            return False

        # if re.search('\s+', self.config_sampling_dir.get()): return False
        # if re.search('\s+', self.sample_dir.get()): return False
        # if re.search('\s+', self.openocdExe_dir.get()): return False

        return True

    def isValidProject(self, selPath):

        if len(selPath) == 0:
            return False

        isvalid = True
        reqDirs = [os.path.join(selPath, child) for child in REQ_PROJECT_DIR_LIST]

        dirlist = []
        dirlist = os.listdir(selPath)

        pathlist = [os.path.join(selPath, child) for child in dirlist]
        dirFilterObject = filter(os.path.isdir, pathlist)

        dirlist = list(dirFilterObject)

        print("%s" % dirlist)
        print("%s" % pathlist)

        for dirname in reqDirs:
            if (not (dirname in dirlist)):
                isvalid = False
                print("%s was not found" % dirname)
                break

        return isvalid

    def get_config_dir(self):
        dir_path = filedialog.askdirectory(title="Select Configuration File Directory")

        if dir_path:
            self.config_sampling_dir.set(dir_path)

    def get_sample_data_dir(self):
        dir_path = filedialog.askdirectory(title="Select Sample Data Directory")

        if dir_path:
            self.sample_dir.set(dir_path)

    def get_opencd_exe_dir(self):
        dir_path = filedialog.askdirectory(title="Select openocd.exe Directory")

        if dir_path:
            self.openocdExe_dir.set(dir_path)

    def create_gui(self, master):
        settingsFrame = Frame(master)
        settingsFrame.pack(fill="both")

        lf1 = LabelFrame(master=settingsFrame,
                         text="Configuration and Sampling List File Directory",
                         padx=10,
                         pady=5)
        lf1.pack(fill="both")

        lf2 = LabelFrame(master=settingsFrame,
                         text="Sampling Data Directory",
                         padx=10,
                         pady=5)
        lf2.pack(fill="both")

        lf3 = LabelFrame(master=settingsFrame,
                         text="OpenOCD Executable Directory",
                         padx=10,
                         pady=5)
        lf3.pack(fill="both")

        parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.config_sampling_dir = StringVar()
        self.config_sampling_dir.set(os.path.join(parent_dir, "fi_config").replace("\\","/"))
        self.sample_dir = StringVar()
        self.sample_dir.set(os.path.join(parent_dir, "sample_analysis").replace("\\","/"))
        self.openocdExe_dir = StringVar()
        self.openocdExe_dir.set(parent_dir.replace("\\","/"))

        entry1 = Entry(lf1, textvariable=self.config_sampling_dir)
        entry1.pack(anchor='w', expand=1, fill='x', side='left')
        button1 = Button(lf1, text="...", command=self.get_config_dir)
        button1.pack(anchor='e',side='left')

        entry2 = Entry(lf2, textvariable=self.sample_dir)
        entry2.pack(anchor='w', expand=1, fill='x', side='left')
        button2 = Button(lf2, text="...", command=self.get_sample_data_dir)
        button2.pack(anchor='e', side='left')

        entry3 = Entry(lf3, textvariable=self.openocdExe_dir)
        entry3.pack(anchor='w', expand=1, fill='x', side='left')
        button3 = Button(lf3, text="...", command=self.get_opencd_exe_dir)
        button3.pack(anchor='e', side='left')

        return settingsFrame

