'''
HeapVariables.py
@author Froylan Aguirre
'''
import re

HEADER_LINE_WORD_COUNT = 4
HEADER_LINE_ADDR_IDX = 1
HEADER_LINE_TOTAL_SIZE_IDX = 2
LINE_ADDR_IDX = 0
LINE_NAME_IDX = 1
RAM_ADDR_SIZE_LEN = 4
RAM_ADDR_IDX = 1
RAM_SIZE_IDX = 2

class HeapVariables:
    '''
    Saves the name, address, and size of all global variables parsed from output.map file.
    '''

    def __init__(self):
        self.output_map_path = None
        self.heap_var_l = None
        self.ram_start_addr = 0
        self.ram_size = 0

    def set_output_map_path(self, file_path):
        self.output_map_path = file_path

    def update_heap_var_data(self):
        if self.output_map_path is None:
            return False

        relevant_lines = self.parse_heap_var_lines()

        var_group_list_l = []
        single_var_group_l = []

        # creates a list of "variable group" lists
        for line in reversed(relevant_lines):
            if len(line.split()) == HEADER_LINE_WORD_COUNT:
                single_var_group_l.insert(0, line)
                var_group_list_l.append(single_var_group_l)
                single_var_group_l = []
                continue

            single_var_group_l.append(line)

        self.heap_var_l = []

        for var_group in var_group_list_l:
            for line in var_group:
                current_line_l = line.split()
                if len(current_line_l) == HEADER_LINE_WORD_COUNT:
                    first_addr = int(current_line_l[HEADER_LINE_ADDR_IDX], 16)
                    total_size = int(current_line_l[HEADER_LINE_TOTAL_SIZE_IDX], 16)
                    last_addr = first_addr + total_size
                else:
                    current_var = HeapVarInfo(name=current_line_l[LINE_NAME_IDX],
                                              addr=int(current_line_l[LINE_ADDR_IDX], 16))
                    current_var.size = last_addr - current_var.addr
                    last_addr = current_var.addr
                    self.heap_var_l.append(current_var)

        self.heap_var_l.sort(key=lambda gv: gv.addr)

        return True

    # noinspection SpellCheckingInspection
    def parse_heap_var_lines(self):
        '''
        Returns lines that contain global variable information.
        Also updates RAM start address and size.
        '''

        print("Reading and Printing the output.map file")

        line_list = []
        mapfile = open(self.output_map_path, "r")

        if mapfile.mode != 'r':
            print("File not properly opened.")
            quit()

        prev_line = ""
        line = " "
        tokenlist = []
        mainStr = 'Src/main.o'
        flag = False

        while line != "":
            line = mapfile.readline()

            if len(line) == 0:
                break

            tokenlist = line.split()

            if len(tokenlist) == 0:
                continue
            elif (tokenlist[0] == "RAM") and (len(tokenlist) == RAM_ADDR_SIZE_LEN):
                self.ram_start_addr = int(tokenlist[RAM_ADDR_IDX], 16)
                self.ram_size = int(tokenlist[RAM_SIZE_IDX], 16)

            if re.search("Src/\w+[.]o", tokenlist[-1]):
                prev_line = line
                flag = True
                continue

            if flag:
                if tokenlist[0].startswith("0x2"):  # only SRAM locations for now
                    if not (prev_line is None):
                        line_list.append(prev_line)
                        prev_line = None

                    line_list.append(line)
                else:
                    flag = False

        mapfile.close()

        if len(line_list) == 0:
            line_list = None

        return line_list

    def __repr__(self):
        string_repr = ""

        for glbl in self.heap_var_l:
            string_repr += glbl.__repr__() + "\n"

        return string_repr


class HeapVarInfo:
    '''
    Represents a global variable saved in heap memory.
    '''

    def __init__(self, name=None, addr=None, size=None):
        self.name = name
        self.addr = addr
        self.size = size

    def __repr__(self):
        string_repr = self.name + " is " + str(self.size) + " bytes at "
        string_repr += format(self.addr, '#010x')
        return string_repr

    def __eq__(self, other):
        return self.name == other.name