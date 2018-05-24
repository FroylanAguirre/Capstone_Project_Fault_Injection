# XML Print Formatting Procs

#source [find "z_fault_injection/fault_utility.tcl"]


proc takeGoldenSample {sampleList_fp outfile_fp} {
		
	puts  $outfile_fp "<SAMPLE desc=\"golden\">"
	#puts $outfile_fp "\"$desc\">"

	#save injection address
	puts $outfile_fp "    <addr>"
	puts $outfile_fp " "
	puts $outfile_fp "    </addr>"

	#save injection moment
	puts $outfile_fp "    <period>"
	puts $outfile_fp "	"
	puts $outfile_fp "    </period>"

	# save registers
	puts $outfile_fp "    <regs>"
	printRegs $outfile_fp
	puts $outfile_fp "    </regs>"

	# #save chosen heap data
	printHeapData $sampleList_fp $outfile_fp
	
	# save stack data
	puts $outfile_fp "    <stack>"
	printStackSnapshot $outfile_fp
	puts $outfile_fp "    </stack>"

	puts $outfile_fp "</SAMPLE>"

}

proc takeInjectionSample {sampleList_fp outfile_fp addr period desc is_LoS} {
		
	puts  -nonewline $outfile_fp "<SAMPLE desc="
	puts  $outfile_fp "\"$desc\">"

	#save injection address
	puts $outfile_fp "    <addr>"
	puts $outfile_fp "          $addr"
	puts $outfile_fp "    </addr>"

	#save injection moment
	puts $outfile_fp "    <period>"
	puts $outfile_fp "          $period"
	puts $outfile_fp "    </period>"

	# save registers
	puts $outfile_fp "    <regs>"
	printRegs $outfile_fp
	puts $outfile_fp "    </regs>"

	# #save chosen heap data
	printHeapData $sampleList_fp $outfile_fp
	
	# save stack data
	puts $outfile_fp "    <stack>"
	printStackSnapshot $outfile_fp
	puts $outfile_fp "    </stack>"

	puts $outfile_fp "    <loss_seq>"
	if {[expr $is_LoS != 0]} {
		puts $outfile_fp "1"
	} else {
		puts $outfile_fp "0"
	}
	puts $outfile_fp "    </loss_seq>"


	puts $outfile_fp "</SAMPLE>"

}

proc printRegs {file_fp} {
	set num_regs 40	

	for {set count 0} {[expr $count < $num_regs]} {incr count} {
		puts -nonewline $file_fp [capture "reg $count"]
	}
}

proc printHeapData {heapAddr_fp outfile_fp} {
	set line ""
	array set heap_data {}
	
	seek $heapAddr_fp 0

	puts $outfile_fp "    <heap>"

	while {[expr [gets $heapAddr_fp line] >= 0]} {
		
		mem2array heap_data [lindex $line 1] [lindex $line 0] [lindex $line 2]
		puts -nonewline $outfile_fp "        <gbl addr=\"[format {0x%02x} [lindex $line 0]]\" "
		puts -nonewline $outfile_fp "size=\"[lindex $line 1]\" "
		puts $outfile_fp "nElem=\"[lindex $line 2]\">"
		
		set max_count [lindex $line 2]

		puts -nonewline $outfile_fp "            "
		for {set count 0} {[expr $count < $max_count]} {incr count} {
			puts -nonewline $outfile_fp "[format {%02x} $heap_data($count)] "
		}

		puts $outfile_fp ""
		puts $outfile_fp "        </gbl>"
	}
	puts $outfile_fp "    </heap>"
} 

proc printStackSnapshot {file_fp} {
	set max_sp 0x20030000
	set current_sp [get_sp]
	set stack_size [expr $max_sp - $current_sp]
	array set stack_contents {}	

	if {[expr $stack_size > 0]} {
		mem2array stack_contents 8 $current_sp $stack_size
	}
	
	puts -nonewline $file_fp "        "	
	for {set count 0} {[expr $count < $stack_size]} {incr count} {
		puts -nonewline $file_fp "[format {%02x} $stack_contents($count)] "
	}

	puts $file_fp ""
}

proc initXML {output_fp} {
	puts $output_fp {<?xml version="1.0" encoding="UTF-8"?>}
	puts $output_fp "<sample_seq>"

}

proc completeXML {output_fp } {
	puts $output_fp "</sample_seq>"
}



