import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import sample_parser as spl
from mpl_toolkits import mplot3d


print "Starting XML Parsing...."

regs = spl.CpuRegs()
p = spl.SampleParser()

# with open("mm_samplesG.txt") as xml_file:
#     goldenParse = ET.parse(xml_file)

# golden_samples = goldenParse.getroot()

with open("samples.txt") as xml_file:
    injectParse = ET.parse(xml_file)

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
            

    # for val in heap_err:
    #     print val
    #     errs.append(val[0][0])
    #     addrs.append(val[1])
    #     tims.append(val[2])

    print tims_a, tims_b
    err_plot = plt.figure(1)
    # ax.set(xlabel='SRAM address (0x20000000 offset)', ylabel='error count',
    #    title='Addresses Error Accumulation')
    plt.plot(addrErrs, 'r')
    plt.xlabel("SRAM address (0x20000000 offset)")
    plt.ylabel("Error Count")
    plt.title("Address Error Accumulation")
    plt.grid() 

    tim_plot = plt.figure(2)
    # tim_plot.set(xlabel='Injection Time (timer counts)', ylabel='error count',
    #     title='Errors vs. injection time')
    plt.plot(tims_a, errs_a, 'b.')
    plt.plot(tims_b, errs_b, 'bs')
    plt.xlabel("Injection Time (timer counts)")
    plt.ylabel("Error Count")
    plt.title("Errors v. injection time")
    plt.grid() 

    addr_plot = plt.figure(3)
    # ax.set(xlabel='SRAM address (0x20000000 offset)', ylabel='error count',
    # title='Injection Location vs. injection time')  
    plt.plot(addrs_a, errs_a,  'g.')
    plt.plot(addrs_b, errs_b, 'gs')
    plt.xlabel("SRAM address")
    plt.ylabel("Error Count")
    plt.title("Injection Location vs. injection time")
    plt.grid() 


    for i in range(len(addrs_a) ):
        if addrs_a[i] > 536875140: 
            addrs_a[i] = 536870912
            tims_a[i] = 20000
            errs_a[i] = 100


    cool = plt.figure(4)
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(addrs_a, tims_a, errs_a, cmap='viridis', edgecolor='none');
    # ax.scatter(addrs_a, tims_a, errs_a, c=errs_a, cmap='viridis', linewidth=0.5);


    # plt.plot(addrs, errs, 'r.')
    plt.show()


except IndexError:
    print("IndexError. End.")




