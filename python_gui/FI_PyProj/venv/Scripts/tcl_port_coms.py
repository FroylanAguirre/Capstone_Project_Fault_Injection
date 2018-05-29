import socket
from gui_format import Tcl_Interface_Tab
import subprocess
import os

TCP_PORT = 6666
#
# filepath="D:/path/to/batch/myBatch.bat"
# p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
#
# stdout, stderr = p.communicate()
# print p.returncode # is 0 if success

class Tcl_Port:

    def tclPortConnect(self):
        # add subprocess here
        print ("connecting TCL port...")
        self.p = subprocess.Popen(self.filepath, shell=True, stdout=subprocess.PIPE)

        # print (p.returncode) # is 0 if success
        print("openocd started, connect socket...")


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conState = self.sock.connect_ex(('localhost', TCP_PORT))



        if conState == 0:
            print("socket connected...")
            self.isConnected = True
            self.tcl_gui.printToTclTerminal("Connection achieved.")

        else:
            self.isConnected = False
            self.tcl_gui.printToTclTerminal("Connection failure.")

        print("DONE CONNECTING...")

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

                # read_val = self.p.stdout.readline()
                # while not (read_val == b''):
                #
                #     # print("read_val_prev:", read_val_prev, ":")
                #     # read_val_prev = read_val
                #     read_val = self.p.stdout.readline()
                #     print("read_val is:", read_val, ":")
                #     print("... ")

            else:
                self.isConnected = False

            recData = recData[0:-1] # removes the termination char
            return recData

    def send_ocd_cmd(self, cmd):
        if self.isConnected:
            print("input: ", cmd)
            res = self.sendTclCmd(cmd)
            self.tcl_gui.printToTclTerminal("> " + cmd)
            self.tcl_gui.printToTclTerminal(res)
            return res


    def get_runtime(self):
        start_bp = 0x8001104
        end_bp = 0x800126a
        self.send_ocd_cmd("reset halt")
        self.send_ocd_cmd("script import_fi_stuff.tcl")
        runtime_cmd = "set runtime [test_runtime ", hex(start_bp), " ", hex(end_bp), " 1000"
        self.send_ocd_cmd("set runtime [test_runtime 0x8001104 0x800126a 1000]")
        res = self.send_ocd_cmd("ocd_echo $runtime")
        print("RESULT: ", res)

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
        self.tcl_gui.tclGetRuntime.config(command=self.get_runtime)
        self.tcl_gui.tclInput.bind("<Return>", self.sendCmd)
        return self.tcl_gui

    def __init__(self):
        self.p = None
        self.isConnected = False
        self.filepath = "C:/Ac6/SystemWorkbench/plugins/fr.ac6.mcu.debug_2.1.1.201708311556/resources/openocd/scripts/tools/Capstone_Project_Fault_Injection/python_gui/FI_PyProj/venv/BatchFiles/fault_inj.bat"
        

