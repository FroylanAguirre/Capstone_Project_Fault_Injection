from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import re
import random
from enum import Enum
from mem_map_canvas import MemoryMapCanvas
import os


class FaultInjectionStats:

    class VarSel(Enum):
        # DO NOT CHANGE THESE VALUES
        # THEY REPRESENT ORDER IN CONFIG FILE
        addr = 0
        inj_time = 1
        bit_pos = 2

    def __init__(self, proj_info):
        self.project = proj_info
        self.bp_list = {'init': None, 'inj': None, 'smpl': None}  # dict of IntVal()
        self.to_list = {'init': None, 'inj': None, 'smpl': None}  # dict of IntVal()
        self.project_name = None  # StringVar()
        self.fault_ranges = {'time': FaultParam(),
                             'mem1': FaultParam(),
                             'mem2': FaultParam()}
        self.num_inj = None  # dict of IntVal
        # self.inj_area = {'mem': None, 'reg': None}  # dict of IntVar
        # self.rand_var = None  # dict of IntVal, selects if variable varies randomly
        # self.var_val_sel = self.VarSel.addr.value  # enum VarSel, selects variable quantity
        self.test_number = 0
        self.bit_pos = None  # , selects a constant bit position [0, 7]
        self.hex_val = None
        self.dec_val = None
        self.sample_file = None
        self.config_file_path = None
        self.mem_map = None
        self.project_file_name = None

    def create_sample_list(self):
        pass

    @staticmethod
    def get_integer(string_val):
        value = int(string_val)
        return value

    def update_proj_file_name(self, proj_file_name):
        self.project_file_name = StringVar()
        self.project_file_name.set(proj_file_name)

    def create_config_file(self):

        self.mem_map.print_sampled_globals()
        print("project file name: ", self.project_file_name.get())

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

        try:
            # create the project config file
            fp = self.project.config_sampling_dir.get().strip('\n')
            cfg_f = fp + "/" + self.project_name.get() + ".cfg"
            print("trying to make a file pointer at: ", cfg_f)
            config_file = open(cfg_f, 'w')
            print("created config file pointer")

            # create the fault injection file
            fp = self.project.config_sampling_dir.get().strip('\n')
            fi_f = fp + "/" + self.project_name.get() + ".fi"
            print("trying to make a file pointer at: ", fi_f)
            fi_file = open(fi_f, 'w')
            print("created fi file pointer")

            # create sampling list
            fp = self.project.config_sampling_dir.get().strip('\n')
            sl_f = fp + "/" + self.project_name.get() + ".sl"
            print("trying to make a file pointer at: ", sl_f)
            sl_file = open(sl_f, 'w')
            print("created sl file pointer")

            # create sample analysis file
            fp = self.project.sample_dir.get().strip('\n')
            sa_f = fp + "/" + self.project_name.get() + ".sa"
            print("trying to make a file pointer at: ", sa_f)
            sa_file = open(sa_f, 'w')
            print("created sl file pointer")

        except FileNotFoundError:
            messagebox.showerror("File Error",
                                 "Configuration file not created.")
            return

        self.write_fault_inj_file(fi_file)
        self.write_config_file(config_file, fi_f, sl_f)
        self.write_sampling_list(sl_file)
        self.write_sample_analysis_file(sa_file)

        config_file.close()
        fi_file.close()
        sl_file.close()
        sa_file.close()

        messagebox.showinfo("Input File Creation",
                            "Configuration file created in " + fp)
        self.test_number += 1

        if self.test_number == 1:
            p_name = self.project_name.get()
        else:
            p_name = self.project_name.get()[:-1]

        p_name += str(self.test_number)
        self.project_name.set(p_name)

    def write_fault_inj_file(self, fi_file):

        if "\n" in self.project.sample_dir.get():
            samples_filename = self.project.sample_dir.get().rstrip() + "/" + self.project_name.get() + ".xml\n"
        else:
            samples_filename = self.project.sample_dir.get() + "/" + self.project_name.get() + ".xml\n"

        fi_file.write(samples_filename)

        # write the time-out list values
        fi_file.write(str(self.to_list['init'].get()) + ' ')
        fi_file.write(str(self.to_list['inj'].get()) + ' ')
        fi_file.write(str(self.to_list['smpl'].get()) + '\n')

        fi_file.write(hex(self.bp_list['init'].get()) + ' ')
        fi_file.write(hex(self.bp_list['inj'].get()) + ' ')
        fi_file.write(hex(self.bp_list['smpl'].get()) + ' ')

        delta = 0

        for n in range(int(self.num_inj.get())):
            # config_f.write("\n")
            # print("n: ", n)
            # generate injection times
            param_time = self.generate_param_value(self.fault_ranges['time'],
                                                   delta=delta)

            # if param_time is None: break
            # print("param time: ", param_time)
            # generate injection locations
            param_addr = self.rand_addr_value(int(self.fault_ranges['mem1'].min.get()),
                                              int(self.fault_ranges['mem1'].max.get()),
                                              int(self.fault_ranges['mem2'].min.get()),
                                              int(self.fault_ranges['mem2'].max.get()))

            # print("param addr: ", param_addr)
            # if change_fault_param == self.VarSel.bit_pos.value:
            #     param_bit = delta
            # else:
            #     param_bit = self.bit_pos.get()

            param_bit = random.randint(0, 7)

            fi_file.write("\n")
            fi_file.write(str(param_time) + " " + str(param_addr) + " ")
            fi_file.write(str(param_bit))

            # if (param_bit == 7) and (change_fault_param == self.VarSel.bit_pos.value): break

            delta += 1

    def write_sampling_list(self, sl_file):
        for var in self.mem_map.selected_globals.sampling_list:
            if var.sample or var.critical:
                sl_file.write(hex(var.addr) + " 8 " + str(var.size) + "\n")

    def write_sample_analysis_file(self, sa_file):
        for var in self.mem_map.selected_globals.sampling_list:
            if var.critical:
                sa_file.write(var.name + " " + hex(var.addr) + " " + str(var.size) + " critical\n")
            elif var.sample:
                sa_file.write(var.name + " " + hex(var.addr) + " " + str(var.size) + " sample\n")

    def write_config_file(self, config_f, fi_f, sl_f):

        print("STARTING TO WRITE TO CONFIG FILE...")
        # write the project directories
        if "\n" in self.project.sample_dir.get():
            config_f.write(self.project.sample_dir.get())
        else:
            config_f.write(self.project.sample_dir.get() + '\n')

        if "\n" in self.project.config_sampling_dir.get():
            config_f.write(self.project.config_sampling_dir.get())
        else:
            config_f.write(self.project.config_sampling_dir.get() + '\n')

        if "\n" in self.project.openocdExe_dir.get():
            config_f.write(self.project.openocdExe_dir.get())
        else:
            config_f.write(self.project.openocdExe_dir.get() + '\n')

        # write the name of the file to write samples to
        # samples_filename = self.project.sample_dir.get() + "/"
        # samples_filename += "samples.txt\n"
        # config_f.write(samples_filename)
        if "\n" in self.project.sample_dir.get():
            samples_filename = self.project.sample_dir.get().rstrip() + "/" + self.project_name.get() + ".xml\n"
        else:
            samples_filename = self.project.sample_dir.get() + "/" + self.project_name.get() + ".xml\n"

        config_f.write(samples_filename)

        # write the time-out list values
        config_f.write(str(self.to_list['init'].get()) + ' ')
        config_f.write(str(self.to_list['inj'].get()) + ' ')
        config_f.write(str(self.to_list['smpl'].get()) + '\n')

        config_f.write(hex(self.bp_list['init'].get()) + ' ')
        config_f.write(hex(self.bp_list['inj'].get()) + ' ')
        config_f.write(hex(self.bp_list['smpl'].get()) + ' ')

        # write the fault injection ranges
        config_f.write("\ninjection_count: ")
        config_f.write(str(self.num_inj.get()) + ' ')
        config_f.write("\ntimes: ")
        config_f.write(str(self.fault_ranges['time'].min.get()) + ' ')
        config_f.write(str(self.fault_ranges['time'].max.get()) + ' ')
        config_f.write("\nmem_range1: ")
        config_f.write(str(self.fault_ranges['mem1'].min.get()) + ' ')
        config_f.write(str(self.fault_ranges['mem1'].max.get()) + ' ')
        config_f.write("\nmem_range2: ")
        config_f.write(str(self.fault_ranges['mem2'].min.get()) + ' ')
        config_f.write(str(self.fault_ranges['mem2'].max.get()) + ' ')
        config_f.write("\n")

        config_f.write(fi_f)
        config_f.write(sl_f)
        config_f.write(self.project_file_name.get())

    def load_config_file(self):
        self.config_file_path = StringVar()
        file_path = filedialog.askopenfilename(initialdir=os.path.dirname(self.project.config_sampling_dir.get()),
                                               title="Select file")

        if file_path:
            self.config_file_path.set(file_path)
        else:
            print("could not open config file")
            return

        ld_file = open(file_path, 'r')

        line = ld_file.readline()
        print("line0: ", line)
        self.project.sample_dir.set(line)
        print("sample_dir: ", line)

        line = ld_file.readline()
        print("line1: ", line)
        self.project.config_sampling_dir.set(line)
        print("config file dir: ", line)

        line = ld_file.readline()
        print("line2: ", line)
        self.project.openocdExe_dir.set(line)

        line = ld_file.readline()
        print("line2.5: ", line)

        line = ld_file.readline().split()
        print("line3: ", line)
        self.to_list['init'].set(line[0])
        self.to_list['inj'].set(line[1])
        self.to_list['smpl'].set(line[2])

        line = ld_file.readline().split()
        print("line4: ", line)
        try:
            self.bp_list['init'].set(line[0])
            self.bp_list['inj'].set(line[1])
            self.bp_list['smpl'].set(line[2])
        except ValueError:
            self.bp_list['init'].set(line[0])
            self.bp_list['inj'].set(line[1])
            self.bp_list['smpl'].set(line[2])

        line = ld_file.readline().split()
        print("line5: ", line)
        self.num_inj.set(line[1])

        line = ld_file.readline().split()
        print("line6: ", line)
        self.fault_ranges['time'].min.set(line[1])
        self.fault_ranges['time'].max.set(line[2])

        line = ld_file.readline().split()
        print("line7: ", line)
        self.fault_ranges['mem1'].min.set(line[1])
        self.fault_ranges['mem1'].max.set(line[2])

        line = ld_file.readline().split()
        print("line8: ", line)
        self.fault_ranges['mem2'].min.set(line[1])
        self.fault_ranges['mem2'].max.set(line[2])

        print("tim2 vals: ", self.fault_ranges['time'].min.get())

    @staticmethod
    def generate_param_value(fault_param, random_on=True, delta=0):
        """
        :param fault_param: a FaultParam type, represents bounds
        :param random_on: bool, true if value is randomly generated
        :param delta: int, change from min field of fault_param
        :return: new value
        """
        if random_on:
            value = random.randint(int(fault_param.min.get()), int(fault_param.max.get()) + 1)
        else:
            value = int(fault_param.min.get()) + delta
            if value > int(fault_param.max.get()):
                value = None

        return value

    @staticmethod
    def rand_addr_value(from1, to1, from2, to2):
        # check if only one address range is specified

        # print("rand address values ", from1, ", ", to1, ", ", from2, ", ", to2)
        if from2 == to2:
            return random.randint(from1, to1)
        # check if address ranges are in order
        elif from1 < from2:
            while True:
                addr = random.randint(from1, to2)
                if addr > from2 or addr < to1:
                    return addr 
        else: 
            while True:
                addr = random.randint(from2, to1)
                if addr > from1 or addr < to2:
                    return addr 

    def create_gui(self, master):
        tab_frame = Frame(master)
        fi_frame = LabelFrame(tab_frame, text="Fault Injection Stuff")
        # self.sample_frame = Frame(tab_frame)
        tab_frame.pack(fill="none")
        fi_frame.grid(row=0, column=0)

        sample_frame = LabelFrame(tab_frame, text="Sampling Stuff")
        sample_frame.grid(row=0, column=1)
        self.mem_map = MemoryMapCanvas(sample_frame)
        # self.sample_frame.pack(fill="none")

        self.proj_name_subframe(fi_frame, 2)
        # self.bit_pos_radiobutton(fi_frame)

        self.general_options_subframe(fi_frame, 3)
        self.breakpoint_timeout_subframe(fi_frame, 4)
        self.fault_range_subframe(fi_frame, 5)
        self.hex_to_dec_subframe(fi_frame, 6)
        # self.analysis_plots_subframe(fi_frame)

        # self.variable_quantity_subframe(fi_frame)

        # self.bit_pos_radiobutton(fi_frame)

        create_config_bttn = Button(fi_frame,
                                    text="Create Config File",
                                    takefocus=0,
                                    command=self.create_config_file)
        create_config_bttn.grid(row=1, column=0)
        load_config_bttn = Button(fi_frame,
                                  text="Load Existing Configuration",
                                  takefocus=0,
                                  command=self.load_config_file)
        load_config_bttn.grid(row=0, column=0)

        return tab_frame

    @property
    def check_ready_for_config_creation(self):
        is_ready = True

        if re.search('\s+', self.project_name.get()):
            return False
        if not self.project.check_ready_for_config_creation:
            return False

        for key in self.fault_ranges:
            is_ready = is_ready and self.fault_ranges[key].check()

            if is_ready is False:
                mes = "Fault parameter range is not a positive integer for _" + str(key) + "_ min: " + \
                      str(self.fault_ranges[key].min.get()) + "_ max: " + str(self.fault_ranges[key].max.get())
                messagebox.showerror("Configuration Error", mes)
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

        # if not (self.inj_area['mem'].get() or
        #         self.inj_area['reg'].get()):
        #     messagebox.showerror("Configuration Error",
        #                          "You must select at least one injection area.")
        #     return False

        if self.num_inj.get() is None:
            messagebox.showerror("Configuration Error",
                                 "Must provide number of injections.")
            return False

        return True

    def general_options_subframe(self, master, row):
        op_frame = LabelFrame(master, text="Number of Injections")
        # op_frame.pack(ipadx=5)
        op_frame.grid(row=row, column=0)

        # n_inj_lbl = Label(op_frame, text="Number of Injections:")
        # n_inj_lbl.pack(anchor='center')

        self.num_inj = IntVal()
        e1 = Entry(op_frame, textvariable=self.num_inj)
        e1.pack(anchor='center')

    def proj_name_subframe(self, master, row):
        proj_name = LabelFrame(master,
                               text="Project Name",
                               padx=5,
                               pady=5)
        # proj_name.pack(side='left', anchor='n')
        proj_name.grid(row=row, column=0)
        self.project_name = StringVar()
        entry1 = Entry(proj_name, textvariable=self.project_name)
        entry1.pack()

    def analysis_plots_subframe(self, master, row):
        self.sample_file = StringVar()
        self.sample_file.set(self.project.sample_dir.get())

        plots_frame = LabelFrame(master, text="Analysis Plots")
        plots_frame.grid(row=row, column=1)

        sample_file_label = Label(plots_frame, text="Sample File")
        sample_file_label.grid(row=0, column=0)
        sample_file_entry = Entry(plots_frame, textvariable=self.sample_file)
        sample_file_entry.grid(row=0, column=1)

    def hex_to_dec_subframe(self, master, row):

        self.hex_val = StringVar()
        self.dec_val = StringVar()

        htd_frame = LabelFrame(master, text="Hex-to-Decimal")
        htd_frame.grid(row=row, column=0)

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

    def breakpoint_timeout_subframe(self, master, row):
        bt_frame = LabelFrame(master,
                              text="Breakpoint Addresses and Timeouts",
                              padx=10,
                              pady=5)
        # bt_frame.pack(side='top')
        bt_frame.grid(row=row, column=0)

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

    def fault_range_subframe(self, master, row):
        f_frame = LabelFrame(master,
                             text="Fault Parameter Ranges",
                             padx=10,
                             pady=5)
        # f_frame.pack()
        f_frame.grid(row=row, column=0)

        bp_label = Label(f_frame, text="Minimum Value")
        to_label = Label(f_frame, text="Maximum Value")

        init_label = Label(f_frame, text="Injection Time:")
        inj_label1 = Label(f_frame, text="SRAM Address Range 1:")
        inj_label2 = Label(f_frame, text="SRAM Address Range 2:")
        # sampl_label = Label(f_frame, text="Register Number:")
        init_label.grid(column=0, row=1)
        inj_label1.grid(column=0)
        inj_label2.grid(column=0)
        # sampl_label.grid(column=0)

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

        # self.fault_ranges['reg'].min = IntVal()
        # entry4 = Entry(f_frame, textvariable=self.fault_ranges['reg'].min)
        # entry4.grid(row=4, column=1)

        self.fault_ranges['time'].max = IntVal()
        entry5 = Entry(f_frame, textvariable=self.fault_ranges['time'].max)
        entry5.grid(row=1, column=2)

        self.fault_ranges['mem1'].max = IntVal()
        entry6 = Entry(f_frame, textvariable=self.fault_ranges['mem1'].max)
        entry6.grid(row=2, column=2)

        self.fault_ranges['mem2'].max = IntVal()
        entry7 = Entry(f_frame, textvariable=self.fault_ranges['mem2'].max)
        entry7.grid(row=3, column=2)

        # self.fault_ranges['reg'].max = IntVal()
        # entry8 = Entry(f_frame, textvariable=self.fault_ranges['reg'].max)
        # entry8.grid(row=4, column=2)


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

        try:
            value = int(string_val, base=base)
        except ValueError:
            value = None

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
            val_list.append(random.randint(self.min.get(),
                                           self.max.get() + 1))

        return val_list
