#first

from tkinter import filedialog
from tkinter import *
import os
from gui_format import Gui_format
from proj_stats import Proj_Stats
from top_window import Top_Frame
import re
import matplotlib
import socket
from tcl_port_coms import Tcl_Port
from fault_injection_stats import FaultInjectionStats

"""
Top level logic.
Reminder that we are using version 8.6 of Tkinter.
"""

MAIN_O_FILE_TOKEN = "Src/main.o"

def check_list_intersection(listA, listB):
    """ Returns true if the lists have at least one element in common. """
    nonzero_intersection = False

    i = set.intersection(set(listA), set(listB))

    if (len(i) != 0):
        nonzero_intersection = True

    return nonzero_intersection

def readPrintOutputMap(filePath):
    print("Reading and Printing the output.map file")

    lineList = []
    mapfile = open(filePath, "r")

    if (mapfile.mode != 'r'):
        print("File not properly opened.")
        quit()

    prevLine = ""
    line = " "
    tokenlist = []
    mainStr = 'Src/main.o'
    flag = False

    while (line != ""):
        line = mapfile.readline()

        if (len(line) == 0):
            break

        tokenlist = line.split()

        if (len(tokenlist) == 0):
            continue

        if (re.search("Src/\w+[.]o", tokenlist[-1])):
            prevLine = line
            flag = True
            continue

        if (flag):
            if (tokenlist[0].startswith("0x2")): #only SRAM locations for now
                if (prevLine != None):
                    lineList.append(prevLine)
                    prevLine = None

                lineList.append(line)
            else:
                flag = False

    mapfile.close()

    if (len(lineList) == 0):
        lineList.append("No global variables found.")

    return lineList

def findGlobalVars():
    print("Finding global vars in C file.")
    cfile = open("output.map", "r")

    if (cfile.mode != 'r'):
        print("File not properly opened.")
        quit()

    line = "lol"
    varList = []

    while (line != ""):
        line = cfile.readline()

        if (len(line) == 0):
            break

def parseStackData():
    suFilePath = os.path.join(proj.projPath, "Debug/Src/main.su")

    try:
        suFile = open(suFilePath, 'r')
    except FileNotFoundError:
        print ("file not found")
        return ".su file not found.\n"

    if (suFile.mode != 'r'): #possibly get rid of this
        print(".su file not found")
        quit()

    line  = "lala"
    tokenAlist = []
    tokenBlist = []
    formatedOutput = []

    while (line != ""):
        line = suFile.readline()

        if len(line) == 0:
            break

        tokenAlist = line.split()
        tokenBlist = tokenAlist[0].split(":")

        #print("A: %s" % tokenAlist)
        #print("B: %s" % tokenBlist)

        formatedOutput.append(tokenBlist[3] + " " + tokenBlist[0] +
                              " " + tokenAlist[1] + " " + tokenAlist[2] + '\n')

    return formatedOutput

def updateProjMemStats():
    if (not proj.isValidProj):
        return None

    toPrint = readPrintOutputMap(os.path.join(proj.projPath, "Debug/output.map"))
    toStackText = parseStackData()
    gui.tab1.stackTable.populateTable(toStackText)
    gui.tab1.glblVars.displayGlobalVars(toPrint)

def projSelButtonPress():
    print("BUTTON PRESSED")
    name = filedialog.askdirectory(parent=gui.tab1)

    print("X" + name + "X")

    if proj.isValidProject(name):
        print("IS VALID")
        #print("directories: %s" % directories)

        proj.isValidProj = True
        proj.projPath = name

        gui.tab1.proj_dir.updateFileLabel(name)
        updateProjMemStats()
    else:
        print("Project file NOT valid")
        proj.isValidProj = False
        gui.tab1.proj_dir.updateFileLabel(None)

def redoButtonPress():
    if (not proj.isValidProj):
        print("Project file NOT valid") #used for debug
        gui.tab1.proj_dir.updateFileLabel(None)
    else:
        print("Will redo.")
        updateProjMemStats()

#================================================

print("Finding stuff")
vars = ['ptr', 'tic', 'tac']
#toPrint = readPrintOutputMap()
toPrint = ""

proj = Proj_Stats()
fi = FaultInjectionStats(proj)

#matplotlib.use("TkAgg")
root = Tk()
root.title("Memory Stats")
#gui = Gui_format(master=root)

tcl_port = Tcl_Port()

gui = Top_Frame(root, tcl_port, proj, fi)

#Set button actions.
gui.tab1.dirConfig.projDirButton.configure(command=projSelButtonPress)
gui.tab1.dirConfig.redoButton.configure(command=redoButtonPress)



# root.tk.eval('puts "hello, pls work"')
# root.tk.eval('source tcl_script.tcl')
# root.tk.eval('puts "DONE"')

# TCP_IP = '127.0.0.1'
# TCP_PORT = 6666
# BUFFER_SIZE = 1024
# MESSAGE = "Hello, World!"
#
# host = socket.gethostname()
# print("host: ", host)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conState = s.connect_ex(('localhost', TCP_PORT))
# print("conState: ", conState)
#
# sendState = s.sendall(b"echo Hello_there")
# print("sendState: ", sendState)
# sendState = s.sendall(b"reset run")
# print("sendState: ", sendState)
#
# data = "Nothing received."
# #data = s.recv(BUFFER_SIZE)
#
# s.close()
# print("received data:", data)

gui.mainloop()
