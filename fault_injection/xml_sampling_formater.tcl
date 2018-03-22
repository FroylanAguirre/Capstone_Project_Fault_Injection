# XML Print Formatting Procs
# Contains functions responsible for collecting data and outputing 
# 	it to the sample data file in XML syntax.
# Author: Froylan Aguirre and Matthew Gerken

source [find "tools/fault_injection/fault_utility.tcl"]

# Responsible from printing register values to output file.
# file_fp: pointer to output file
proc printRegs {file_fp} {
	set num_regs 40	

	for {set count 0} {[expr $count < $num_regs]} {incr count} {
		puts -nonewline $file_fp [capture "reg $count"]
	}
}

# Prints data stored at specified memory locations.
# heapAddr_fp: file pointer to sampling list (this is were addresses
#	to be sampled are listed
# outfile_fp: pointer to output file
proc printHeapData {heapAddr_fp outfile_fp} {
	set line ""
	array set heap_data {}
	
	seek $heapAddr_fp 0

	puts $outfile_fp "    <heap>"

	# interate through sampling list file
	while {[expr [gets $heapAddr_fp line] >= 0]} {
		
		mem2array heap_data 8 [lindex $line 0] [lindex $line 1]
		puts -nonewline $outfile_fp "        <gbl addr=\"[format {0x%02x} [lindex $line 0]]\" "
		puts $outfile_fp "nElem=\"[lindex $line 1]\">"
		
		set max_count [lindex $line 1]

		puts -nonewline $outfile_fp "            "
		for {set count 0} {[expr $count < $max_count]} {incr count} {
			puts -nonewline $outfile_fp "[format {%02x} $heap_data($count)] "
		}

		puts $outfile_fp ""
		puts $outfile_fp "        </gbl>"
	}

	puts $outfile_fp "    </heap>"
} 

# Prints the stack to output file.
# file_fp: pointer to output file
proc printStackSnapshot {file_fp} {
	# this is the bottom of the stack
	#	(the stack grows into lower addresses
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

#proc takeMemorySample {sampleList_fp outfile_fp desc} {
#		
#	puts -nonewline $outfile_fp "<SAMPLE desc="
#	puts $outfile_fp "\"$desc\">"
#
#	# save registers
#	puts $outfile_fp "    <regs>"
#	printRegs $outfile_fp
#	puts $outfile_fp "    </regs>"
#
#	#save chosen heap data
#	printHeapData $sampleList_fp $outfile_fp
#	
#	# save stack data
#	puts $outfile_fp "    <stack>"
#	printStackSnapshot $outfile_fp
#	puts $outfile_fp "    </stack>"
#
#	puts $outfile_fp "</SAMPLE>"
#
#}

proc initXML {output_fp} {
	puts $output_fp {<?xml version="1.0" encoding="UTF-8"?>}
	puts $output_fp "<sample_seq>"

}

proc completeXML {output_fp } {
	puts $output_fp "</sample_seq>"
}

#proc printSamplingData {heapAddr_fp outfile_fp} {
#	set line ""
#	array set heap_data {}
#	
#	seek $heapAddr_fp 0
#
#	set addr ""
#	set size ""
#	set nElem ""
#
#	#puts $outfile_fp "    <heap>"
#
#	while {[expr [gets $heapAddr_fp line] >= 0]} {
#		
#		#mem2array heap_data [lindex $line 1] [lindex $line 0] [lindex $line 2]
#		
#		set type [lindex $line 0]
#		if {[string equal $type regs]} { 
#			set addr all
#			set size 32
#			#there are 39 registers
#			set nElem 39
#		} elseif {[string equal $type reg]} { 
#			set addr [lindex $line 1]
#			set size 32
#			set nElem 1
#		} elseif {[string equal $type mem]} { 
#			set addr [lindex $line 1]
#			set size [lindex $line 2]
#			set nElem [lindex $line 3]
#		} else {
#			echo "Invalid sampling location. Ignored."
#			continue
#        }
#		
#		puts -nonewline $outfile_fp "    <area type=\"[lindex $line 0]\" addr=\"$addr\" "
#		puts -nonewline $outfile_fp "size=\"$size\" "
#		puts $outfile_fp "nElem=\"$nElem\">"
#
#		#puts -nonewline $outfile_fp "    <area addr=\"[format {0x%02x} [lindex $line 0]]\" "
#		#puts -nonewline $outfile_fp "size=\"[lindex $line 1]\" "
#		#puts $outfile_fp "nElem=\"[lindex $line 2]\">"
#		
#		if {[string equal $type regs]} { 
#			printRegs $outfile_fp
#		} elseif {[string equal $type reg]} { 
#			puts $outfile_fp [get_reg_num [lindex $line 1]]
#		} elseif {[string equal $type mem]} { 
#			set max_count [lindex $line 3]
#
#			mem2array heap_data [lindex $line 2] [lindex $line 1] [lindex $line 3]
#			
#			#puts -nonewline $outfile_fp "        "
#			for {set count 0} {[expr $count < $max_count]} {incr count} {
#				puts -nonewline $outfile_fp "[format {%02x} $heap_data($count)] "
#			}
#
#			puts $outfile_fp ""
#
#		}
#
#		#puts $outfile_fp ""
#		puts $outfile_fp "    </area>"
#	}
#
#	#puts $outfile_fp "    </heap>"
#} 
#
#proc takeSingleSample {sampleList_fp outfile_fp desc} {
#		
#	puts -nonewline $outfile_fp "<SAMPLE desc="
#	puts $outfile_fp "\"$desc\">"
#
#	printSamplingData $sampleList_fp $outfile_fp
#
#	puts $outfile_fp "</SAMPLE>"
#
#}

# Creates a single <SAMPLE> element.
# sampleList_fp: pointer to sampling list file
# outfile_fp: pointer to output file
# addr: memory address of fault injection
# period: time (in clock cycles) of fault injection
# desc: description of sample
# is_LoS: boolean value, 1 if loss of sequence occured, 0 otherwise 
proc takeInjectionSample {sampleList_fp outfile_fp addr period desc is_LoS} {
       
    puts  -nonewline $outfile_fp "<SAMPLE desc="
    puts  $outfile_fp "\"$desc\">"

    # save injection address
    puts $outfile_fp "    <addr>"
    puts $outfile_fp "          $addr"
    puts $outfile_fp "    </addr>"

    # save injection moment
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


