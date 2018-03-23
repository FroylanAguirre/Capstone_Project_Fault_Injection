# Hybird Method Script
# Author: Matt
# Modified by Froylan Aguirre
source [find "tools/fault_injection/fault_utility.tcl"]
source [find "tools/fault_injection/xml_sampling_formater.tcl"]

# config_file_name: specifies which configuration file to use
# sampling_file_name: where to output the collected data
# Runs the fault injection trials and outputs the collected data to a sample file
proc fault_inject {config_file_name sampling_file_name } {

	#===Reading config file
	set config_fp [open $config_file_name "r"]
	set sampling_fp [open $sampling_file_name "r"]
	
	set c1 ""
	gets $config_fp c1

	set wait_times ""
	gets $config_fp wait_times

	set bp_addr ""
	gets $config_fp bp_addr

	set filename [lindex $c1 0]
	set outfile_fp [open $filename "w"]

	initXML $outfile_fp

	set sample_list_fp  [open $sampling_file_name "r"]

	set TIME_start [clock clicks ]

	set count 0

	#define addresses of important mem locations
	#mem location of the period global variable
	set tim_period_addr 0x4000002C
	
	#descriptions for XML samples
	set golden_desc "golden"
	set inj_desc "injection"
	set seq_loss_desc "sequence_loss"

	#define wait times
	#how long to wait for first bp in main 
	set start_wait [lindex $wait_times 0]
	set inject_wait [lindex $wait_times 1]
	#how long to wait for the result to be calculated
	set results_wait [lindex $wait_times 2]
	
	#set breakpoints
	#where we will set the timer period,seed
	bp [lindex $bp_addr 0] 2		
	#set injection breakpoint
	bp [lindex $bp_addr 1] 2
	#where we capture the results matrix
	set results_bp [lindex $bp_addr 2]
	bp $results_bp 2
	echo "Breakpoints setup."
	
	set nInj [lindex $c1 0]
    halt

    #grab the golden sample
    reset run
	sleep $start_wait
	resume
	sleep $inject_wait
	resume
	sleep $results_wait
	halt

	#grab the golden sample
	takeInjectionSample $sample_list_fp $outfile_fp " " " " "golden" 0
	echo "Golden sample complete."	


	echo "STARTING LOOP"
    while {[expr [gets $config_fp case_params] >= 0]} {

		#parse out the next test params
		#gets $config_fp case_params
	
		set tim_period [lindex $case_params 0]
		set inj_addr [lindex $case_params 1]
		set bit_num [lindex $case_params 2]

		echo "time period: $tim_period"
		echo "inj_addr: $inj_addr"
		echo "bit_num: $bit_num"

		#SET THE TIMER PERIOD
		reset run
		sleep $start_wait

		#by this time, DUT must already hit first bp
		mem2array period_data_arr 32 $tim_period_addr 1 
		echo "          Period was: $period_data_arr"
		mww $tim_period_addr $tim_period
		mem2array period_data_arr 32 $tim_period_addr 1 
		echo "          Period is now: $period_data_arr"
		resume
		sleep $inject_wait
		
		#INJECT FAULT
		echo " "
		echo "*****Injecting fault at $inj_addr with period $tim_period"

		#we should now be stopped in inject_fault() function
		#get byte of data from the injection address
		mem2array inj_data_arr 8 $inj_addr 1        
		echo "OLD DATA: $inj_data_arr(0)"
		
		#flip bit 
		set inj_data [flip_bit $inj_data_arr(0) $bit_num]  
		mww $inj_addr $inj_data 8
		resume
		sleep $results_wait
		halt

		set stopAddr [get_pc]

		#check for loss of sequence error
		if {[expr $stopAddr != $results_bp]} {
			echo "Loss of Sequence: $stopAddr != $results_bp"
			takeInjectionSample $sample_list_fp $outfile_fp $inj_addr $tim_period "injection" 1
			set count [expr {$count + 1}]
			halt
			continue
		}
		
		takeInjectionSample $sample_list_fp $outfile_fp $inj_addr $tim_period "injection" 0

		set count [expr {$count + 1}]
		echo "Count: $count, $nInj"
    }

	close $config_fp
	close $sample_list_fp
	
	set TIME_taken [expr [clock clicks] - $TIME_start]
	
    echo "Injecting complete"
	echo "Completed $nInj injections"
	set TIME_taken_sec [expr {$TIME_taken / 1000}]
	echo "Took $TIME_taken_sec ms to complete"

	completeXML $outfile_fp
	
	close $outfile_fp 

	#remove breakpoints
	rbp [lindex $bp_addr 0] 		
	rbp [lindex $bp_addr 1] 
	set results_bp [lindex $bp_addr 2]
	rbp $results_bp 

}



