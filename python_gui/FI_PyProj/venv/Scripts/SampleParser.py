import xml.etree.ElementTree as ET
import re
import matplotlib.pyplot as plt

MAX_STACK_ADDR = 0x20030000

# within a sample
REG_SUBIDX = 2
HEAP_SUBIDX = 3
STACK_SUBIDX = 4
LOS_SUBIDX = 5

NUM_REGS = 17


class SampleParser:

    def __init__(self):
        self.sample_file = None
        self.num_samples = None
        self.num_global_var = None
        self.reg_err = None
        self.heap_err = None
        self.stack_err = None
        self.errCnt = None
        self.heapCnt = None
        self.seq_loss_errs = None

    # return a list of critical heap variables
    def parse_analysis_file(self, analysis_file):
        var_stats = []
        with open(analysis_file) as sa_f:
            content = sa_f.readlines()

        content = [x.strip("\n") for x in content]
        for line in content:
            var = line.split(" ")
            if var[-1] == "critical":
                var_stats.append(True)
            else:
                var_stats.append(False)

        return var_stats
        # critical_addrs = []
        # latent_addrs = []
        #
        # with open(analysis_file) as sa_f:
        #     content = sa_f.readlines()
        #
        # # you may also want to remove whitespace characters like `\n` at the end of each line
        # content = [x.strip("\n") for x in content]
        # for line in content:
        #     var = line.split(" ")
        #     addr = int(var[1], 16)
        #     size = int(var[2])
        #     for i in range(size):
        #         if var[-1] == "critical":
        #             critical_addrs.append(addr)
        #         else:
        #             latent_addrs.append(addr)
        #
        #         addr += 1
        #
        # return critical_addrs, latent_addrs

    def parse_sample_file(self, sample_file, analysis_file):
        print("hello")
        self.sample_file = sample_file
        self.num_samples = 0
        self.num_global_var = 0
        self.reg_err = []
        self.heap_err = []
        self.stack_err = []
        self.errCnt = 0
        self.heapCnt = []
        self.seq_loss_errs = []
        plot_list = []

        print("ANANLSLLSLS FILE: ", analysis_file)

        critical_vars = self.parse_analysis_file(analysis_file)

        # critical_list, latent_list = self.parse_analysis_file(analysis_file)
        # print("critical list : ", critical_list)
        # print("latent list: ", latent_list)
        # plt.plot(critical_list, "ro")
        # plt.plot(latent_list, "bo")
        # plt.show()

        print("opening sample file")

        try:
            with open(sample_file) as xml_file:
                injectParse = ET.parse(xml_file)

            print("parsing file for xml stuff..")
            samples = injectParse.getroot()
            self.num_samples = len(samples) - 1
            self.num_global_var = len(samples[0][3])

            val_listA = samples[0][3][0].text.split(' ')
            addrErrs = [0] * len(val_listA)
            for idx in range(1, self.num_samples):
                self.errCnt = self.diff_regs(samples[0], samples[idx])
                self.reg_err.append(self.errCnt)

                self.heapCnt = self.diff_heap(samples[0], samples[idx], self.num_global_var)
                self.heap_err.append(self.heapCnt)
                print("YOOOOOOOOOOOOO: ", self.heapCnt)

                addrErrs = self.addr_errs(samples[0], samples[idx], addrErrs)

                is_seq_loss = self.is_seq_loss(samples[idx])
                self.seq_loss_errs.append(is_seq_loss)


            addrs = []
            tims = []
            errs = []
            critical_errs = []
            latent_errs = []

            # iterate through all samples
            for i in range(len(self.heap_err)):
                addrs.append(self.heap_err[i][1])
                tims.append(self.heap_err[i][2])

                critical_err_cnt = 0
                latent_err_cnt = 0
                # iterate through each global variable in the sample
                for j in range(self.num_global_var):

                    # check if the variable is critical data
                    if critical_vars[j]:
                        critical_err_cnt += self.heap_err[i][0][j]
                    else:
                        latent_err_cnt += self.heap_err[i][0][j]

                critical_errs.append(critical_err_cnt)
                latent_errs.append(latent_err_cnt)
                errs.append(critical_err_cnt + latent_err_cnt)

            print("critical errs: ", critical_errs)
            print("latent errs: ", latent_errs)

            for i in range(len(addrs)):
                if addrs[i] > 536875140:
                    addrs[i] = 536870912
                    tims[i] = 20000
                    errs[i] = 100

            min_addr = min(addrs)
            addrs[:] = [x - min_addr for x in addrs]

            max_tim = float(max(tims))
            tims[:] = [x / max_tim * 100 for x in tims]

            plot_list.append(addrs)
            plot_list.append(tims)
            plot_list.append(errs)
            plot_list.append(critical_errs)
            plot_list.append(latent_errs)
            return plot_list

        except (IndexError, ET.ParseError) as e:
            print("IndexError. End.")
            return [], [], []

    def get_reg_list(self, sample):
        # note that first element of newline_split is ""
        newline_split = sample[REG_SUBIDX].text.split('\n')
        print(newline_split)
        reg_val = []

        for idx in range(1, NUM_REGS + 1):
            val = int(newline_split[idx].split(' ')[2], 16)
            reg_val.append(val)

        return reg_val

    def is_seq_loss(self, sample):
        return int(sample[LOS_SUBIDX].text)

    def get_stack_size(self, sample):
        regs = CpuRegs()
        registers = sample[REG_SUBIDX].text.split('\n')[regs.sp() + 1]
        print(registers)
        sp = int(registers.split(' ')[2], 16)
        size = MAX_STACK_ADDR - sp

        return size

    def diff_regs(self, sampleA, sampleB):
        regs = CpuRegs()
        regA = sampleA[REG_SUBIDX].text.split('\n')
        regB = sampleB[REG_SUBIDX].text.split('\n')
        errCount = 0

        for idx in range(1, NUM_REGS + 1):
            if regA[idx] != regB[idx]:
                errCount += 1

        return errCount

    def diff_string_list(self, val_listA, val_listB):
        errCount = 0

        for idx in range(0, len(val_listA)):  # assuming lists are of same length
            if val_listA[idx] != val_listB[idx]:
                errCount += 1

        return errCount

    def diff_heap(self, sampleA, sampleB, num_global_vars):

        errCount = []
        for idx in range(0, num_global_vars):
            val_listA = sampleA[HEAP_SUBIDX][idx].text.split(' ')
            val_listB = sampleB[HEAP_SUBIDX][idx].text.split(' ')
            errCount.append(self.diff_string_list(val_listA, val_listB))

        inj_addr = int(re.search(r'\d+', sampleB[0].text).group())
        inj_time = int(re.search(r'\d+', sampleB[1].text).group())

        return errCount, inj_addr, inj_time

    def addr_errs(self, sampleA, sampleB, addrCount):
        val_listA = sampleA[HEAP_SUBIDX][0].text.split(' ')
        val_listB = sampleB[HEAP_SUBIDX][0].text.split(' ')
        for idx in range(0, len(val_listA)):  # assuming lists are of same length
            if val_listA[idx] != val_listB[idx]:
                addrCount[idx] = addrCount[idx] + 1

        return addrCount


class CpuRegs:
    def r0(self):
        return 0

    def r1(self):
        return 1

    def r2(self):
        return 2

    def r3(self):
        return 3

    def r4(self):
        return 4

    def r5(self):
        return 5

    def r6(self):
        return 6

    def r7(self):
        return 7

    def r8(self):
        return 8

    def r9(self):
        return 9

    def r10(self):
        return 10

    def r11(self):
        return 11

    def r12(self):
        return 12

    def sp(self):
        return 13

    def lr(self):
        return 14

    def pc(self):
        return 15

    def xPSR(self):
        return 16

