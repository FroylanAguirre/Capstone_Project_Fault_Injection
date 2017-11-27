from tkinter import filedialog
from tkinter import *
import os
from gui_format import Gui_format
from proj_stats import Proj_Stats

REQ_PROJECT_DIR_LIST = (".settings", "Debug",
                        "Drivers", "Inc",
                        "Src", "startup")

def check_list_intersection(listA, listB):
    nonzero_intersection = False

    i = set.intersection(set(listA), set(listB))

    if (len(i) != 0):
        nonzero_intersection = True

    return nonzero_intersection

def readPrintOutputMap(filePath):
    print("Reading and Printing the output.map file")

    lineList = [""]
    mapfile = open(filePath, "r")

    if (mapfile.mode != 'r'):
        print("File not properly opened.")
        quit()

    prevLine = "lala"
    line = "lala"
    tokenlist = ['one', 'two']
    mainStr = 'Src/main.o'
    flag = False

    while (line != ""):
        line = mapfile.readline()

        if (len(line) == 0):
            break

        tokenlist = line.split()

        if (mainStr in tokenlist):
            prevLine = line
        elif (check_list_intersection(tokenlist, vars)):

            if (not flag):
                #print("%s" % prevLine)
                lineList.append(prevLine)
                flag = True

            #print("%s" % line)
            lineList.append(line)
        else:
            flag = False

    mapfile.close()

    #print("lineList = %d" % len(lineList))

    if (len(lineList) == 1): #fix this later, dont know why it returns newline when nothing found
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

        if (len(line) == 0):
            break

        tokenAlist = line.split()
        tokenBlist = tokenAlist[0].split(":")

        #print("A: %s" % tokenAlist)
        #print("B: %s" % tokenBlist)

        formatedOutput.append(tokenBlist[3] + " " + tokenBlist[0] +
                              " " + tokenAlist[1] + " " + tokenAlist[2] + '\n')

    return formatedOutput

def isValidProject(selPath, dirlist):
    isvalid = True
    reqDirs = [os.path.join(selPath, child) for child in REQ_PROJECT_DIR_LIST]

    for dirname in reqDirs:
        if (not (dirname in dirlist)):
            isvalid = False
            print("%s was not found" % dirname)
            break

    return isvalid

def projSelButtonPress():
    print("BUTTON PRESSED")
    name = filedialog.askdirectory(parent=gui.root)
    #gui.pathname.set(name)

    dirlist = []
    dirlist = os.listdir(name)

    pathlist = [os.path.join(name, child) for child in dirlist]
    dirFilterObject = filter(os.path.isdir, pathlist)

    directories = list(dirFilterObject)

    print("%s" % dirlist)
    print("%s" % pathlist)

    if isValidProject(name, directories):
        print("IS VALID")
        print("directories: %s" % directories)

        proj.isValidProj = True
        proj.projPath = name

        gui.updateFileLabel(name)

        toPrint = readPrintOutputMap(os.path.join(name, "Debug/output.map"))

        #toStackText = parseStackData()

        gui.globalText.delete('1.0', END)

        for line in toPrint:
            gui.globalText.insert(END, line)

        #for datum in toStackText:
        #    gui.stackText.insert(END, "  " + datum)

    else:
        print("Project file NOT valid")
        projSelected = False
        gui.updateFileLabel(None)

def redoButtonPress():
    print("WILL REDO")

#================================================

#TODO: Format stack info.

print("Finding stuff")
vars = ['ptr', 'tic', 'tac']
#toPrint = readPrintOutputMap()
toPrint = ""

proj = Proj_Stats()

gui = Gui_format()

gui.projDirButton.configure(command=projSelButtonPress)
gui.redoButton.configure(command=redoButtonPress)

#projSelected = False
#root = Tk()
#root.title("Memory Stats")

#pathname = StringVar()
#pathname.set("this better work")
#labelList = []
#idx = True

#button = Button(root, text="Project File",
#                command=buttonPressed,
#                takefocus=0)
#button.pack(fill="both")

#pathLabel = Label(root, textvariable=pathname, anchor=W)
#pathLabel.pack(fill="both")
#pathname = "plz work"

#textBox = Text(root, font='Consolas')
#textBox.pack(fill="both")
#textBox.insert(END, "This is a text box.\n")

#for line in toPrint:
#    textBox.insert(END, line)

#for line in toPrint:
#    if (idx):
#        labelList.append(
#            Label(root, text = line.rstrip(), anchor = W))
#    else:
#        labelList.append(
#            Label(root, text = line.rstrip(), anchor = W))
#
#    labelList[-1].pack(fill="both")
#    idx = not idx

gui.root.mainloop()
