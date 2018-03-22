import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import sample_parser as spl
import sys
from tkinter.messagebox import *

'''
Standalone script that parses sample data file to create three plots from a chosen sample data file.
'''

print("Starting XML Parsing....")

regs = spl.CpuRegs()
p = spl.SampleParser()

if len(sys.argv) <= 1:
    print("No filename received.")
    quit()

sample_file = sys.argv[1]
print("we got file: " +  sample_file)

try:
    with open(sample_file) as xml_file:
        injectParse = ET.parse(xml_file)
except ET.ParseError:
    # how you prevent smaller window from opening?
    #showerror("XML Parsing Error", "Sample data file not formatted correctly.")
    print("sample data file not properly configured")
    quit()

samples = injectParse.getroot()

num_samples = len(samples) - 1
num_global_var = len(samples[0][3])
reg_err = []
heap_err = []
stack_err = []
errCnt = 0
heapCnt = []
seq_loss_errs = []

try:
    val_listA = samples[0][3][0].text.split(' ')
    addrErrs = [0] * len(val_listA)
    for idx in range(1, num_samples):
        
        errCnt = p.diff_regs(samples[0], samples[idx])
        reg_err.append(errCnt)

        heapCnt = p.diff_heap(samples[0], samples[idx], num_global_var)
        heap_err.append(heapCnt)

        addrErrs = p.addr_errs(samples[0], samples[idx], addrErrs)

        is_seq_loss = p.is_seq_loss(samples[idx])
        seq_loss_errs.append(is_seq_loss)

    print("Register Errors")
    print(reg_err)

    print("Heap Errors")
    print(heap_err)

    print("Sequence Loss Errors")
    print(seq_loss_errs)

    addrs_a = []
    addrs_b =[]

    tims_a = []
    tims_b = []

    errs_a = []
    errs_b = []

    for i in range(len(heap_err)):
        if seq_loss_errs[i] > 0:
            errs_b.append(heap_err[i][0][0])
            addrs_b.append(heap_err[i][1])
            tims_b.append(heap_err[i][2])
        else:
            errs_a.append(heap_err[i][0][0])
            addrs_a.append(heap_err[i][1])
            tims_a.append(heap_err[i][2])

    print(tims_a, tims_b)
    err_plot = plt.figure(1)
    plt.plot(addrErrs, 'r')
    plt.xlabel("SRAM address (0x20000000 offset)")
    plt.ylabel("Error Count")
    plt.title("Address Error Accumulation")
    plt.grid() 

    tim_plot = plt.figure(2)
    plt.plot(tims_a, errs_a, 'b.')
    plt.plot(tims_b, errs_b, 'bs')
    plt.xlabel("Injection Time (timer counts)")
    plt.ylabel("Error Count")
    plt.title("Errors v. injection time")
    plt.grid() 

    addr_plot = plt.figure(3)
    plt.plot(addrs_a, errs_a,  'g.')
    plt.plot(addrs_b, errs_b, 'gs')
    plt.xlabel("SRAM address")
    plt.ylabel("Error Count")
    plt.title("Injection Location vs. injection time")
    plt.grid() 

    plt.show()

except IndexError:
    print("IndexError. End.")
