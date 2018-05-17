#ProjDirLblFr.py
from tkinter import *
from tkinter import ttk

"""
Contains Frame and LabelFrame subclasses that contain necessary widgets.
They are arranged in the Gui_format class.
"""

class ProjDirLblFr(LabelFrame):

    def __init__(self, master=None):
        LabelFrame.__init__(self,
                            master=master,
                            labelanchor="nw",
                            text="Project Directory",
                            padx=10,
                            pady=5)
        self.pack(fill="both")

        self.pathname = StringVar()
        self.pathname.set("No project file selected.")

        pathLabel = Label(self, textvariable=self.pathname, anchor=W)
        pathLabel.pack(fill="both")

    def updateFileLabel(self, path):
        if (path != None):
            self.pathname.set(path)
        else:
            self.pathname.set("Invalid project file selected.")


class GlobalVarsDisplayLblFr(LabelFrame):

    def __init__(self, master=None):
        LabelFrame.__init__(self, master=master,
                            labelanchor="nw",
                            text="Globals",
                            padx=10,
                            pady=5)
        self.pack(fill="both")

        self.globalText = Text(self, font='Consolas')
        self.globalText.pack(fill="both")
        self.globalText.insert(END, "This is a text box.\n")
        self.globalText.config(state=DISABLED)

    def displayGlobalVars(self, newtext):
        self.globalText.config(state=NORMAL)
        self.globalText.delete('1.0', END)

        #for line in newtext:
        self.globalText.insert(END, newtext)

        self.globalText.config(state=DISABLED)


class DirButtonsFr(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)
        self.pack()

        self.projDirButton = \
            Button(self,
                   text="Project File",
                   takefocus=0)
        self.projDirButton.pack(side=LEFT)

        self.redoButton = \
            Button(self,
                   text="Update",
                   takefocus=0)
        self.redoButton.pack(side=LEFT)


class StackTableLblFr(LabelFrame):

    def setupTable(self):
        tv = ttk.Treeview(self)
        tv['columns'] = ('size', 'type', 'file')
        tv.heading("#0", text='Function Name', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('size', text='Size')
        tv.column('size', anchor='center', width=100)
        tv.heading('type', text='Type')
        tv.column('type', anchor='center', width=100)
        tv.heading('file', text='File')
        tv.column('file', anchor='center', width=100)
        tv.grid(sticky=(N, S, W, E))
        self.stackTable = tv
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def __init__(self, master=None):
        LabelFrame.__init__(self,
                            master=master,
                            labelanchor="nw",
                            text="Function Stack Use",
                            padx=10,
                            pady=5)
        self.pack(fill="both")
        self.setupTable()

    def populateTable(self, tableEntries):
        self.stackTable.delete(*self.stackTable.get_children())
        for func in tableEntries:
            token = func.split()
            self.stackTable.insert('', 'end',
                                   text=token[0],
                                   values=(token[2], token[3], token[1]))


