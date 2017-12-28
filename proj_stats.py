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

    def isValidProject(self, selPath):
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