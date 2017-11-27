# Capstone_Project_Fault_Injection_GUI
GUI for Capstone project that will output revelant memory stats.

More specifically, it parses info from the output.map (global variable location and size) and .su file (functions and their stack
usage). 
Generate the .su file for a .c file by including -fstack-usage as a compilation option in the submake file (Makefile in the same
directory as .c file).
