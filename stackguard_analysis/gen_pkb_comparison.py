#/usr/bin/python3

# Instructions:
# Update filenames.path to include the following:
#  - line1 is the path to vulnerable.c
#  - line2 is the path to dynamorio's ddrun
#  - line3 is the path to peekaboo's libpeekabo_dr.so 
#  - line4 is the path to read_trace
#  - line5 is the path to base target
#  - line6 is the path to 1st modified target (no overflow)
#  - line7 is the path to 2nd modified target (with overflow)

# /home/ubuntu/Desktop/peekaboo-master/read_trace /home/ubuntu/Desktop/cs5231_tp_repo/stackguard_analysis/modified-13328-1400As/13328/

import os

# ---------------------------------------------
# Compile vuln.c with specified memory defences
# ---------------------------------------------

gcc_md_flags = ["-z norelro", "-fno-stack-protector", "-z execstack", "-no-pie", 
	"| echo 0 | sudo tee /proc/sys/kernel/randomize_va_space", "| echo 2 | sudo tee /proc/sys/kernel/randomize_va_space"]

with open("filepaths.txt") as f:
    filepaths = [line.rstrip() for line in f]

def createBaseCase():

	gcc_base_cmd = "gcc -g"
	gcc_executable_base_name = "base"

	generateBase = input("[#] Do you want to generate peekaboo trace with no mem-def (i.e., base case)? [Y|n] ")

	if(generateBase == 'Y'):

		for i in range(4):
			gcc_base_cmd += " " + gcc_md_flags[i]

		print("creating executable: base")
		os.system(gcc_base_cmd + " " + filepaths[0] + " -o " + gcc_executable_base_name)

		print("checksec output: base")
		os.system("checksec --file=" + gcc_executable_base_name)

		print("creating peekaboo trace: base")
		peekaboo_cmd_base = filepaths[1] + " -c " + filepaths[2] + " -- " + gcc_executable_base_name
		os.system(peekaboo_cmd_base)


def createModifiedCase():

	# ---------------------------------------------
	# Create modified with specified memory defence
	# ---------------------------------------------

	gcc_cmd = "gcc -g"
	aslr_cmd = " "
	hasAslr = 0
	gcc_executable_modified_name = "modified"

	generateModified = input("[#] Do you want to generate peekaboo trace with your own mem-def specification? [Y|n] ")

	if(generateModified == 'Y'):

		print("\nChoose which memory defences to remove for the modified version...")
		print("[0] RELRO -- [1] CANARY -- [2] NX -- [3] PIE -- [4] disable ASLR -- [5] enable ASLR\n")

		selected_gcc_flags = input("[#] Enter defence to remove (e.g., 12 == canary + nx): ")

		selected_gcc_flags_tokens = [int(flag) for flag in str(selected_gcc_flags)]

		for flag in selected_gcc_flags_tokens:
			if flag == 4 or flag == 5:
				aslr_cmd += gcc_md_flags[flag]
				hasAslr = 1
				continue
			gcc_cmd += " " + gcc_md_flags[flag]

		print("creating executable: modified")

		if hasAslr == 1:
			print(gcc_cmd + filepaths[0] + " -o " + gcc_executable_modified_name + aslr_cmd)
			os.system(gcc_cmd + " " + filepaths[0] + " -o " + gcc_executable_modified_name + aslr_cmd)
		else:
			print(gcc_cmd + filepaths[0] + " -o " + gcc_executable_modified_name)
			os.system(gcc_cmd + " " + filepaths[0] + " -o " + gcc_executable_modified_name)

		# ---------------------------------------------
		# Double check memory defences with 'checksec'
		# ---------------------------------------------

		print("checksec output: modified")
		os.system("checksec --file=" + gcc_executable_modified_name)

		# ---------------------------------------------
		# Create peekaboo trace files (modified)
		# ---------------------------------------------

		peekaboo_cmd_modified = filepaths[1] + " -c " + filepaths[2] + " -- " + gcc_executable_modified_name
		os.system(peekaboo_cmd_modified)


def compareInstructions():

	# ---------------------------------------------
	# Create instruction dump of all trace files
	# ---------------------------------------------

	base_inst_filename = "allInst_compare/base_inst.txt"
	modified1_inst_filename = "allInst_compare/noOverflow_inst.txt"
	modified2_inst_filename = "allInst_compare/withOverflow_inst.txt"

	generateInstFiles = input("[#] Do you want to generate peekaboo all instructions files? [Y|n] ")

	if(generateInstFiles == 'Y'):

		# base
		print(filepaths[3] + " " + filepaths[4])
		os.system(filepaths[3] + " " + filepaths[4] + " > " + base_inst_filename)

		# modified1 (no overflow)
		print(filepaths[3] + " " + filepaths[5])
		os.system(filepaths[3] + " " + filepaths[5] + " > " + modified1_inst_filename)

		# modified2 (with overflow)
		print(filepaths[3] + " " + filepaths[6])
		os.system(filepaths[3] + " " + filepaths[6] + " > " + modified2_inst_filename)


	generateRangeInstFiles = input("[#] Do you want to generate peekaboo range of instructions files? [Y|n] ")

	if(generateRangeInstFiles == 'Y'):

		getRange = input("[#] Please specify your instruction range (e.g., 100-105): ")

		base_inst_filename = "rangeInst_compare/base_inst_" + getRange + ".txt"
		modified1_inst_filename = "rangeInst_compare/noOverflow_inst_" + getRange + ".txt"
		modified2_inst_filename = "rangeInst_compare/withOverflow_inst_" + getRange + ".txt"

		getRangeToken = getRange.split('-')

		print(getRangeToken)

		# base
		print(filepaths[3] + " -s " + getRangeToken[0] + " -e " + getRangeToken[1] + " " + filepaths[4])
		os.system(filepaths[3] + " -s " + getRangeToken[0] + " -e " + getRangeToken[1] + " " + filepaths[4] + " > " + base_inst_filename)

		# modified1 (no overflow)
		print(filepaths[3] + " -s " + getRangeToken[0] + " -e " + getRangeToken[1] + " " + filepaths[5])
		os.system(filepaths[3] + " -s " + getRangeToken[0] + " -e " + getRangeToken[1] + " " + filepaths[5] + " > " + modified1_inst_filename)

		# modified2 (with overflow)
		print(filepaths[3] + " -s " + getRangeToken[0] + " -e " + getRangeToken[1] + " " + filepaths[6])
		os.system(filepaths[3] + " -s " + getRangeToken[0] + " -e " + getRangeToken[1] + " " + filepaths[6] + " > " + modified2_inst_filename)


def compareSyscall():

	# ---------------------------------------------
	# Create syscall dump of all trace files
	# ---------------------------------------------

	base_syscall_filename = "syscall_compare/base_syscall.txt"
	modified1_syscall_filename = "syscall_compare/noOverflow_syscall.txt"
	modified2_syscall_filename = "syscall_compare/withOverflow_syscall.txt"

	generateSyscallFiles = input("[#] Do you want to generate peekaboo syscall files? [Y|n] ")

	if(generateSyscallFiles == 'Y'):

		# base
		print(filepaths[3] + " -y " + filepaths[4])
		os.system(filepaths[3] + " -y " + filepaths[4] + " > " + base_syscall_filename)

		# modified1 (no overflow)
		print(filepaths[3] + " -y " + filepaths[5])
		os.system(filepaths[3] + " -y " + filepaths[5] + " > " + modified1_syscall_filename)

		# modified2 (with overflow)
		print(filepaths[3] + " -y " + filepaths[6])
		os.system(filepaths[3] + " -y " + filepaths[6] + " > " + modified2_syscall_filename)

	#with open(base_syscall_filename) as f:
	#	base_syscalls = [line.rstrip() for line in f]

	#with open(modified1_syscall_filename) as f:
	#	modified1_syscalls = [line.rstrip() for line in f]

	#with open(modified2_syscall_filename) as f:
	#	modified2_syscalls = [line.rstrip() for line in f]

	# ---------------------------------------------
	# Generate syscall_diff_summary
	# ---------------------------------------------
	
	# clean up syscalls (remove inst id)
	#line_iterator = 0
	#del base_syscalls[0:3]
	#del base_syscalls[-1]

	#base_syscalls_num_lines = len(base_syscalls)
	#while line_iterator < base_syscalls_num_lines:
	#	index = base_syscalls[line_iterator].find(']') + 1
	#	base_syscalls[line_iterator] = base_syscalls[line_iterator][index:].lstrip()
	#	line_iterator += 1
		
	#line_iterator = 0
	#del modified1_syscalls[0:3]
	#del modified1_syscalls[-1]

	#modified1_syscalls_num_lines = len(modified1_syscalls)
	#while line_iterator < modified1_syscalls_num_lines:
	#	index = modified1_syscalls[line_iterator].find(']') + 1
	#	modified1_syscalls[line_iterator] = modified1_syscalls[line_iterator][index:].lstrip()
	#	line_iterator += 1

	#line_iterator = 0
	#del modified2_syscalls[0:3]
	#del modified2_syscalls[-1]

	#modified2_syscalls_num_lines = len(modified2_syscalls)
	#while line_iterator < modified2_syscalls_num_lines:
	#	index = modified2_syscalls[line_iterator].find(']') + 1
	#	modified2_syscalls[line_iterator] = modified2_syscalls[line_iterator][index:].lstrip()
	#	line_iterator += 1

	# base vs modified1		

	# base vs modified2

	# modified1 vs modified2




if __name__ == "__main__":

	# create peekaboo files
	createBaseCase()
	createModifiedCase()

	# run read_trace analysis
	compareInstructions()
	compareSyscall()