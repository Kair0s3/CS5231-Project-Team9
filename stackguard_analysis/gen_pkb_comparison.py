#/usr/bin/python3

# Instructions:
# Update filenames.path to include the following:
#  - line1 is the path to vulnerable.c
#  - line2 is the path to dynamorio's ddrun
#  - line3 is the path to peekaboo's libpeekabo_dr.so 

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

	genereateBase = input("Do you want to generate peekaboo trace with no mem-def (i.e., base case) as well? [Y|n] ")

	if(genereateBase == 'Y'):
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

	print("Choose which memory defences to remove")
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


if __name__ == "__main__":
	createBaseCase()
	createModifiedCase()