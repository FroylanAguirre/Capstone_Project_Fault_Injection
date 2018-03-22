import socket
from gui_format import Tcl_Interface_Tab

'''
tcl_port_coms.py
Contains control logic for a machine interface with the Tcl interpreter on OpenOCD.
Not currently used in project, more of a novelty than anything usefull.
'''

# default machine interface TCP port
TCP_PORT = 6666

class Tcl_Port:

    def tclPortConnect(self):
        '''
        Establishes connection with OpenOCD's machine interface.
        :return: Nothing
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conState = self.sock.connect_ex(('localhost', TCP_PORT))

        if (conState == 0):
            self.isConnected = True
            self.tcl_gui.printToTclTerminal("Connection achieved.")
        else:
            self.isConnected = False
            self.tcl_gui.printToTclTerminal("Connection failure.")

    def sendTclCmd(self, cmd):
        '''
        Sends a command string to OpenOCD.
        :param cmd: an OpenOCD command
        :return: result of OpenOCD command
        '''
        if (self.isConnected):
            cmdLength = len(cmd) + 1

            try:
                sentBytes = self.sock.send(cmd.encode())
                sentBytes += self.sock.send(b'\x1a')
            except ConnectionResetError:
                self.isConnected = False
                return "Port closed."

            recData = None
            if (cmdLength == sentBytes):
                recData = self.sock.recv(20) #change this later
            else:
                self.isConnected = False

            return recData

    def sendCmd(self, event):
        if (self.isConnected):
            line = event.widget.get()
            print("input: ", line)
            ack = self.sendTclCmd(line)
            self.tcl_gui.printToTclTerminal("> " + line)
            self.tcl_gui.printToTclTerminal(ack)

    def create_gui(self, master):
        self.tcl_gui = Tcl_Interface_Tab(master)
        self.tcl_gui.tclPortConnect.config(command=self.tclPortConnect)
        self.tcl_gui.tclInput.bind("<Return>", self.sendCmd)
        return self.tcl_gui

    def __init__(self):
        self.isConnected = False
        

