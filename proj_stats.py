from tkinter import filedialog
from tkinter import *
import os
from gui_format import Gui_format

REQ_PROJECT_DIR_LIST = (".settings", "Debug",
                        "Drivers", "Inc",
                        "Src", "startup")

class Proj_Stats:

    def __init__(self):
        self.projPath = ""
        #self.projPath.trace("w",self.isValidProject())
        self.isValidProj = False

