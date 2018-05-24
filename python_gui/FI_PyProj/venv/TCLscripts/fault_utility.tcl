# Fault Injection Utility Functions 

proc get_sp {} {
	return [lindex [regexp -all -inline {\S+} [capture "reg sp"]] 2]
}

proc get_pc {} {
	return [lindex [regexp -all -inline {\S+} [capture "reg pc"]] 2]
}

proc get_reg_num { regNum } {
	return [lindex [regexp -all -inline {\S+} [capture "reg $regNum"]] 2]
}

proc checkHardfault {} {
	set psr_reg [capture "reg xPSR"]
	set psr_reg [lindex $psr_reg 2]
	set psr_reg [expr $psr_reg & 3]

	#true if hard fault occured, false otherwise
	return [expr $psr_reg == 3]
}

proc get_stack_size {} {
	set max_sp 0x20030000
	set current_sp [get_sp]
	return [expr $max_sp - $current_sp]
}

proc flip_bit {data bitPos} {
	set newValue [expr 1 << $bitPos]
	# set newValue $data
	set newValue [expr $data ^ $newValue]
	echo "new value: [format {0x%02x} $newValue]"
	return $newValue
}

proc test_runtime {initbp endbp runtime_guess} {

	halt
	bp $endbp 2
	bp $initbp 2
	set count 0	
	set count_sum 0
	#array set temp {}
	#set seed(0) $start_seed

	set tim_period_addr 0x4000002C
	set tim_period 100000000

	while {[expr $count < 20]} {
		reset run
		sleep 50
		mem2array period_data_arr 32 $tim_period_addr 1 
		echo "          Period was: $period_data_arr"
		mww $tim_period_addr $tim_period
		mem2array period_data_arr 32 $tim_period_addr 1 
		echo "          Period is now: $period_data_arr"
		resume
		sleep $runtime_guess
		
		#array2mem seed 32 $seed_addr 1
	
		#resume		
		#sleep 100
		#halt

		mem2array temp 32 0x40000024 1
		#echo "seed: $seed(0)"
		echo "CNT: $temp(0)"

		set count_sum [expr $count_sum + $temp(0)]
		#set seed(0) [expr $seed(0) + 1]
		set count [expr $count + 1]
	}

	rbp $initbp
	rbp $endbp

	set count_sum [expr $count_sum / 20]
	
	echo "Average clock cycles: $count_sum"
}



