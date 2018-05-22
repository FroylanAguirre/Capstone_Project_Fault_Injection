import socket
from gui_format import Tcl_Interface_Tab
TCP_PORT = 6666

class Tcl_Port:

    def tclPortConnect(self):
        # add subprocess here
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conState = self.sock.connect_ex(('localhost', TCP_PORT))

        if (conState == 0):
            self.isConnected = True
            self.tcl_gui.printToTclTerminal("Connection achieved.")
        else:
            self.isConnected = False
            self.tcl_gui.printToTclTerminal("Connection failure.")

    def sendTclCmd(self, cmd):
        if (self.isConnected):
            cmdLength = len(cmd) + 1

            try:
                sentBytes = self.sock.send(cmd.encode())
                sentBytes += self.sock.send(b'\x1a')
            except ConnectionResetError:
                self.isConnected = False
                return "Port closed."

            recData = ""
            singleByte = "p"
            if (cmdLength == sentBytes):
                # recData = self.sock.recv(20) #change this later
                while ord(singleByte) != 0x1A:
                    singleByte = self.sock.recv(1)
                    recData += singleByte.decode("utf-8")
                    if singleByte == "":
                        recData = "Connection closed."
            else:
                self.isConnected = False

            recData = recData[0:-1] # removes the termination char
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
        

