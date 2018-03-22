# Capstone_Project_Fault_Injection
GUI for Capstone project that will output revelant memory stats.

More specifically, it parses info from the output.map (global variable location and size) and .su file (functions and their stack
usage). 
Generate the .su file for a .c file by including -fstack-usage as a compilation option in the submake file (Makefile in the same
directory as .c file).

IMPORTANT: From now on, widgets must be enclosed within a subclass of Frame
	or LabelFrame. Subclass should take care of updating or manipulating
	displayed data. Plus this makes rearranging the GUI easier in the future
	if its needed. 
	For example, a Frame subclass would contain a heat map and the methods
	necessary to configure it.   

