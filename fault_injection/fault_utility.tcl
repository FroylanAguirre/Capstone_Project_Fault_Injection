# Fault Injection Utility Functions 
# Author: Froylan Aguirre
# Useful functions for use in fault injection.

# returns stack pointer value
proc get_sp {} {
	return [lindex [regexp -all -inline {\S+} [capture "reg sp"]] 2]
}

# returns program counter value
proc get_pc {} {
	return [lindex [regexp -all -inline {\S+} [capture "reg pc"]] 2]
}

# returns the value of register number "regNum"
proc get_reg_num { regNum } {
	return [lindex [regexp -all -inline {\S+} [capture "reg $regNum"]] 2]
}

#returns true if STM32 has experienced a HardFault
proc checkHardfault {} {
	set psr_reg [capture "reg xPSR"]
	set psr_reg [lindex $psr_reg 2]
	set psr_reg [expr $psr_reg & 3]

	#true if hard fault occured, false otherwise
	return [expr $psr_reg == 3]
}

# returns stack size
proc get_stack_size {} {
	set max_sp 0x20030000
	set current_sp [get_sp]
	return [expr $max_sp - $current_sp]
}

# data: a byte where one bit will be flipped
# bitPos: number between 0 and 7, specifies which bit to flip
# returns data with specified bit flipped
proc flip_bit {data bitPos} {
	set newValue [expr 1 << $bitPos]
	# set newValue $data
	set newValue [expr $data ^ $newValue]
	echo "new value: [format {0x%02x} $newValue]"
	return $newValue
}

# bp_addr: third breakpoint address
# runtime_guess: estimated runtime in ms, must be larger than actual runtime 
proc test_runtime {bp_addr runtime_guess} {

	halt

	# bp near end of program
	bp $bp_addr 2
	set count 0	
	set count_sum 0

	while {[expr $count < 20]} {
		reset run
		sleep $runtime_guess

		mem2array temp 32 0x40000024 1
		echo "CNT: $temp(0)"

		set count_sum [expr $count_sum + $temp(0)]
		set count [expr $count + 1]
	}

	rbp $bp_addr

	set count_sum [expr $count_sum / 20]
	
	echo "Average clock cycles: $count_sum"
}

