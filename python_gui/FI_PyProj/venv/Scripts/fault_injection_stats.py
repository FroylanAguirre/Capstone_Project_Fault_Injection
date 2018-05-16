from tkinter import *
# from tkinter import Frame
# from tkinter import Label
# from tkinter import Entry
# from tkinter import IntVar
# from tkinter import LabelFrame
# from tkinter import StringVar
# from tkinter import Checkbutton
# from tkinter import Button
from tkinter import _tkerror
from tkinter import Radiobutton
from tkinter import messagebox
import re
import random
from enum import Enum

class FaultInjectionStats:

    class VarSel(Enum):
        # DO NOT CHANGE THESE VALUES
        # THEY REPRESENT ORDER IN CONFIG FILE
        addr = 0
        inj_time = 1
        bit_pos = 2

    def __init__(self, proj_info):
        self.project = proj_info
        self.bp_list = {'init':None, 'inj':None, 'smpl':None} # dict of IntVal()
        self.to_list = {'init':None, 'inj':None, 'smpl':None} # dict of IntVal()
        self.project_name = None # StringVar()
        self.fault_ranges = {'time':FaultParam(),
                             'mem1': FaultParam(),
                             'mem2': FaultParam(),
                             'reg':FaultParam()} # dict of IntVal
        self.num_inj = 666 # dict of IntVal
        self.inj_area = {'mem':None, 'reg':None} # dict of IntVar
        self.rand_var = None # dict of IntVal, selects if variable varies randomly
        self.var_val_sel = self.VarSel.addr.value #enum VarSel, selects variable quantity
        self.test_number = 0
        self.bit_pos = None #, selects a constant bit position [0, 7]
        self.hex_val = None
        self.dec_val = None

    def create_sample_list(self):
        pass

    def get_integer(self, stringVal):
        base = 10
        if stringVal.startswith('0x'):
            base = 16

        value = 0
        try:
            value = int(stringVal)
        except _tkerror.TclError:
            value = None

        return value

    def create_config_file(self):

        if not self.project.check_ready_for_config_creation:
            messagebox.showerror("Configuration Error",
                                 "Please enter all directory paths in 'Directory Settings' tab.")
            return

        if not self.project_name.get():
            messagebox.showerror("Configuration Error",
                                 "Project name must be non-empty.")
            return

        if not self.check_ready_for_config_creation:
            return

        fp =""
        try:
            fp = self.project.config_sampling_dir.get()
            fp = fp + "/" + self.project_name.get() + ".txt"
            config_file = open(fp, 'w')
        except:
            messagebox.showerror("File Error",
                                "Configuration file not created.")
            return

        self.write_config_file(config_file)
        config_file.close()

        messagebox.showinfo("Input File Creation",
                            "Configuration file created in " + fp)
        self.test_number += 1

        if self.test_number == 1:
            p_name= self.project_name.get()
        else:
            p_name = self.project_name.get()[:-1]

        p_name += str(self.test_number)
        self.project_name.set(p_name)

    def write_config_file(self, config_f):
        samples_filename = self.project.sample_dir.get() + "/"
        samples_filename += "samples.txt"
        config_f.write(samples_filename)

        config_f.write(str(self.to_list['init'].get()) + ' ')
        config_f.write(str(self.to_list['inj'].get()) + ' ')
        config_f.write(str(self.to_list['smpl'].get()) + '\n')

        config_f.write(hex(self.bp_list['init'].get()) + ' ')
        config_f.write(hex(self.bp_list['inj'].get()) + ' ')
        config_f.write(hex(self.bp_list['smpl'].get()))

        # delta = {'time':0,
        #          'mem':0,
        #          'reg':0} # only used for non-random, varying fault parameters
        delta = 0 # only used for non-random, varying fault parameters
 
        change_fault_param = self.var_val_sel.get()

        # break_flag = False
        for n in range(self.num_inj.get()):
            #config_f.write("\n")

            #generate injection times            
            param_time = self.generate_param_value(self.fault_ranges['time'],
                                                       delta=delta)

            # if param_time is None: break

            #generate injection locations
            param_addr = self.rand_addr_value(self.fault_ranges['mem1'].min.get(), self.fault_ranges['mem1'].max.get(), self.fault_ranges['mem2'].min.get(), self.fault_ranges['mem2'].max.get())

            # if change_fault_param == self.VarSel.bit_pos.value:
            #     param_bit = delta
            # else:
            #     param_bit = self.bit_pos.get()

            param_bit = random.randint(0,7)   
   
            config_f.write("\n")
            config_f.write(str(param_time) + " " + str(param_addr) + " ")
            config_f.write(str(param_bit))

            # if (param_bit == 7) and (change_fault_param == self.VarSel.bit_pos.value): break

            delta += 1


    def generate_param_value(self, fault_param, random_on=True, delta=0):
        """
        :param fault_param: a FaultParam type, represents bounds
        :param random: bool, true if value is randomly generated
        :param delta: int, change from min field of fault_param
        :return: new value
        """
        if random_on:
            value = random.randint(fault_param.min.get(), fault_param.max.get() + 1)
        else:
            value = fault_param.min.get() + delta
            if value > fault_param.max.get():
                value = None

        return value

    def rand_addr_value(self, from1, to1 , from2, to2):
        #check if only one addr range is specified
        if from2 == to2:
            return randint(from1, to1)
        #check if addr ranges are in order
        elif from1 < from2:
            while(True): 
                addr = random.randint(from1, to2)
                if addr > from2 or addr < to1:
                    return addr 
        else: 
            while(True): 
                addr = random.randint(from2, to1)
                if addr > from1 or addr < to2:
                    return addr 


    def create_gui(self, master):
        fiFrame = Frame(master)
        fiFrame.pack(fill="none")

        self.proj_name_subframe(fiFrame)
        self.bit_pos_radiobutton(fiFrame)

        self.breakpoint_timeout_subframe(fiFrame)
        self.hex_to_dec_subframe(fiFrame)
        self.fault_range_subframe(fiFrame)

        self.general_options_subframe(fiFrame)
        self.variable_quantity_subframe(fiFrame)

        #self.bit_pos_radiobutton(fiFrame)

        create_config_bttn = Button(fiFrame,
                                    text="Create Config File",
                                    takefocus=0,
                                    command=self.create_config_file)
        #create_config_bttn.pack()
        create_config_bttn.grid(row=3, column=1)

        return fiFrame

    @property
    def check_ready_for_config_creation(self):
        is_ready = True

        if re.search('\s+', self.project_name.get()): return False
        if not self.project.check_ready_for_config_creation: return False

        for key in self.fault_ranges:
            is_ready = is_ready and self.fault_ranges[key].check()

        if is_ready is False:
            messagebox.showerror("Configuration Error",
                                 "Fault parameter range is not a positive integer.")
            return False

        for key in self.bp_list:
            is_ready = is_ready and (self.bp_list[key].get() is not None)

        if is_ready is False:
            messagebox.showerror("Configuration Error",
                                 "Breakpoint address is not a positive integer.")
            return False

        for key in self.to_list:
            is_ready = is_ready and (self.to_list[key].get() is not None)

        if is_ready is False:
            messagebox.showerror("Configuration Error",
                                 "Breakpoint timeout not a positive integer.")
            return False

        if not (self.inj_area['mem'].get() or \
                self.inj_area['reg'].get()):
            messagebox.showerror("Configuration Error",
                                 "You must select at least one injection area.")
            return False

        if self.num_inj.get() is None:
            messagebox.showerror("Configuration Error",
                                 "Must provide number of injections.")
            return False

        return True

    def bit_pos_radiobutton(self, master):
        label_frame = LabelFrame(master, text="Bit Postion Selection")
        #label_frame.pack(side='left', anchor='n')
        label_frame.grid(row=0, column=1)

        self.bit_pos = IntVar()

        for pos in range(0, 8):
            name = "bit " + str(pos)
            rb = Radiobutton(label_frame,
                             text=name,
                             variable=self.bit_pos,
                             value=pos)
            rb.pack(side='left')

        self.bit_pos.set(0)

    def variable_quantity_subframe(self, master):
        label_frame = LabelFrame(master, text="Variable Quantity Selection")
        #label_frame.pack()
        label_frame.grid(row=2, column=1)

        self.var_val_sel = IntVar()
        rb_addr = Radiobutton(label_frame,
                              text="Address",
                              variable=self.var_val_sel,
                              value=self.VarSel.addr.value)
        rb_addr.pack(anchor='w')

        rb_inj_time = Radiobutton(label_frame,
                              text="Injection Time",
                              variable=self.var_val_sel,
                              value=self.VarSel.inj_time.value)
        rb_inj_time.pack(anchor='w')

        rb_pos = Radiobutton(label_frame,
                              text="Bit Position",
                              variable=self.var_val_sel,
                              value=self.VarSel.bit_pos.value)
        rb_pos.pack(anchor='w')

        self.var_val_sel.set(self.VarSel.addr.value)




    def general_options_subframe(self, master):
        op_frame = LabelFrame(master, text="General Options")
        #op_frame.pack(ipadx=5)
        op_frame.grid(row=2, column=0)

        n_inj_lbl = Label(op_frame, text="Number of Injections:")
        n_inj_lbl.pack(anchor='center')

        self.num_inj = IntVal()
        e1 = Entry(op_frame, textvariable=self.num_inj)
        e1.pack(anchor='center')

        area_flbl = LabelFrame(op_frame, text="Injection Areas")
        area_flbl.pack()

        self.inj_area['mem'] = IntVar()
        cb1 = Checkbutton(area_flbl, text="SRAM",
                          variable=self.inj_area['mem'])
        cb1.pack(side='top', anchor='w')
        self.inj_area['mem'].set(1)

        self.inj_area['reg'] = IntVar()
        cb2 = Checkbutton(area_flbl, text="Registers",
                          variable=self.inj_area['reg'])
        cb2.pack(side='top', anchor='w')

        self.rand_var = IntVar()
        cb3 = Checkbutton(op_frame,
                          text="Random Quantity Values",
                          variable=self.rand_var)
        cb3.pack()

    def proj_name_subframe(self, master):
        proj_name = LabelFrame(master,
                               text="Project Name",
                               padx=5,
                               pady=5)
        #proj_name.pack(side='left', anchor='n')
        proj_name.grid(row=0, column=0)
        self.project_name = StringVar()
        entry1 = Entry(proj_name, textvariable=self.project_name)
        entry1.pack()

    def hex_to_dec_subframe(self, master):

        self.hex_val = StringVar()
        self.dec_val = StringVar()

        self.hex_val.set("jesus")
        self.dec_val.set("christ")

        htd_frame = LabelFrame(master, text="Hex-to-Decimal")
        htd_frame.grid(row=4, column=0)

        hex_label = Label(htd_frame, text="Hex")
        hex_label.grid(column=0, row=0)
        dec_label = Label(htd_frame, text="Dec")
        dec_label.grid(column=1, row=0)

        hex_entry = Entry(htd_frame, text="Hex Value", textvariable=self.hex_val)
        hex_entry.grid(column=0, row=1, padx=10, pady=5)

        dec_entry = Entry(htd_frame, text="Decimal Value", textvariable=self.dec_val)
        dec_entry.grid(column=1, row=1, padx=10, pady=5)

        to_hex_btn = Button(htd_frame,
                                    text="Convert to Hex",
                                    takefocus=0,
                                    command=self.dec_to_hex,
                                    pady=3)

        to_hex_btn.grid(column=1, row=2)
        to_dec_btn = Button(htd_frame,
                            text="Convert to Dec",
                            takefocus=0,
                            command=self.hex_to_dec,
                            pady=3)

        to_dec_btn.grid(column=0, row=2)

    def dec_to_hex(self):
        dec = int(self.dec_val.get())
        self.hex_val.set(hex(dec))

    def hex_to_dec(self):
        self.dec_val.set(int(self.hex_val.get(), 16))

    def breakpoint_timeout_subframe(self, master):
        bt_frame = LabelFrame(master,
                              text="Breakpoint Addresses and Timeouts",
                              padx=10,
                              pady=5)
        #bt_frame.pack(side='top')
        bt_frame.grid(row=1, column=0)

        bp_label = Label(bt_frame, text="Breakpoint Address")
        to_label = Label(bt_frame, text="Breakpoint Timeouts (ms)")

        init_label = Label(bt_frame, text="Init:")
        inj_label = Label(bt_frame, text="Injection:")
        sampl_label = Label(bt_frame, text="Sample:")
        init_label.grid(column=0, row=1)
        inj_label.grid(column=0)
        sampl_label.grid(column=0)

        bp_label.grid(column=1, row=0)
        to_label.grid(column=2, row=0)

        self.bp_list['init'] = IntVal()
        entry1 = Entry(bt_frame, textvariable=self.bp_list['init'])
        entry1.grid(row=1, column=1)

        self.bp_list['inj'] = IntVal()
        entry2 = Entry(bt_frame, textvariable=self.bp_list['inj'])
        entry2.grid(row=2, column=1)

        self.bp_list['smpl'] = IntVal()
        entry3 = Entry(bt_frame, textvariable=self.bp_list['smpl'])
        entry3.grid(row=3, column=1)

        self.to_list['init'] = IntVal()
        entry4 = Entry(bt_frame, textvariable=self.to_list['init'])
        entry4.grid(row=1, column=2)

        self.to_list['inj'] = IntVal()
        entry5 = Entry(bt_frame, textvariable=self.to_list['inj'])
        entry5.grid(row=2, column=2)

        self.to_list['smpl'] = IntVal()
        entry6 = Entry(bt_frame, textvariable=self.to_list['smpl'])
        entry6.grid(row=3, column=2)

    def fault_range_subframe(self, master):
        f_frame = LabelFrame(master,
                             text="Fault Parameter Ranges",
                             padx=10,
                             pady=5)
        #f_frame.pack()
        f_frame.grid(row=1, column=1)

        bp_label = Label(f_frame, text="Minimum Value")
        to_label = Label(f_frame, text="Maximum Value")

        init_label = Label(f_frame, text="Injection Time:")
        inj_label1 = Label(f_frame, text="SRAM Address Range 1:")
        inj_label2 = Label(f_frame, text="SRAM Address Range 2:")
        sampl_label = Label(f_frame, text="Register Number:")
        init_label.grid(column=0, row=1)
        inj_label1.grid(column=0)
        inj_label2.grid(column=0)
        sampl_label.grid(column=0)

        bp_label.grid(column=1, row=0)
        to_label.grid(column=2, row=0)

        self.fault_ranges['time'].min = IntVal()
        entry1 = Entry(f_frame, textvariable=self.fault_ranges['time'].min)
        entry1.grid(row=1, column=1)

        self.fault_ranges['mem1'].min = IntVal()
        entry2 = Entry(f_frame, textvariable=self.fault_ranges['mem1'].min)
        entry2.grid(row=2, column=1)

        self.fault_ranges['mem2'].min = IntVal()
        entry3 = Entry(f_frame, textvariable=self.fault_ranges['mem2'].min)
        entry3.grid(row=3, column=1)

        self.fault_ranges['reg'].min = IntVal()
        entry4 = Entry(f_frame, textvariable=self.fault_ranges['reg'].min)
        entry4.grid(row=4, column=1)

        self.fault_ranges['time'].max = IntVal()
        entry5 = Entry(f_frame, textvariable=self.fault_ranges['time'].max)
        entry5.grid(row=1, column=2)

        self.fault_ranges['mem1'].max = IntVal()
        entry6 = Entry(f_frame, textvariable=self.fault_ranges['mem1'].max)
        entry6.grid(row=2, column=2)

        self.fault_ranges['mem2'].max = IntVal()
        entry7 = Entry(f_frame, textvariable=self.fault_ranges['mem2'].max)
        entry7.grid(row=3, column=2)

        self.fault_ranges['reg'].max = IntVal()
        entry8 = Entry(f_frame, textvariable=self.fault_ranges['reg'].max)
        entry8.grid(row=4, column=2)


class IntVal(StringVar):

    def __init__(self):
        StringVar.__init__(self)

    def get(self):
        """Return value of variable as an integer."""
        value = self._tk.globalgetvar(self._name)

        if not isinstance(value, str):
            return None

        string_val = str(value)
        base = 10
        if string_val.startswith('0x'):
            base = 16

        value = 0
        try: value = int(string_val, base=base)
        except ValueError: value = None

        return value


class FaultParam:

    def __init__(self):
        self.min = None
        self.max = None

    def check(self):
        is_ok = self.max.get() is not None
        is_ok = is_ok and (self.min.get() is not None)

        return is_ok and (self.max.get() >= self.min.get())

    def create_rand_list(self, num_vals, delta):
        val_list = []

        if self.min is not None:
            return val_list

        if self.max is not None:
            return val_list

        if delta <= 0:
            return val_list

        for ind in range(0, num_vals, step=delta):
            val_list.add(random.randint(self.min.get(),
                                        self.max.get() + 1))

        return val_list
