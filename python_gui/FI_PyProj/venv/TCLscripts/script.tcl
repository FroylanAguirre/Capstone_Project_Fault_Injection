# script.tcl
# Small script to call fault injection method or to measure benchmark
# 	runtime.

# might have to change these paths
source [find "hybrid_mod_fi.tcl"]
source [find "fault_utility.tcl"]

#set config_fn "tools/fault_injection/fi_config/new_mm4.txt"
#set sample_list_fn "tools/fault_injection/fi_config/new_mm_sampling.txt"

# comment/uncomment as needed
#fault_inject $config_fn $sample_list_fn

# first argument is last breakpoint address
#test_runtime 0x08000ff4 100


