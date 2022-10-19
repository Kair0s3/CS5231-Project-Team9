## Name: poc.py
## Purpose: Run the program at its baseline, record down the syscall stack and then run the program with the user's input
## This will note down if it makes any dangerous syscalls.
## Author: Lee Ju-Ler Jonathan
## Sample Usages:
## $ python3 poc.py benign_program AAAAAAAAAAAA NAME_OF_FILE_WITH_PAYLOAD
## $ python3 poc.py vuln AAAAAAAAAAAA payload

# Imports are managed here
import os
from pickle import NEWFALSE
import sys
import argparse
from subprocess import Popen, PIPE, STDOUT

# List of constant values
NEW_LINE_DELIM = "\n"
LEFT_PARENTHESIS_DELIM = "("
INDEX_OF_SYSCALL_NAME = 0
INDEX_OF_POPEN_STDERR = 1
STRACE_PROGRAM_STRING = "strace"
DEFAULT_TESTING_VALUE = "l33th4ck3r"
DEFAULT_TERMINATION_MESSAGE = "[!] Program will be terminated"

# List of global variables
list_default_syscalls = []
list_user_syscalls = []


def compareSyscallStacks():
    """
    Compare the baseline syscall stacks with the user provided one 
    :param program_name: (str) name of the program 
    :param previous_args: (list) list of arguments provided by the user
    """
    ## This code somehow feels like shit
    system_index = 0
    # Iterate through each shadow stack and user stack syscalls
    for user_index in range(len(list_user_syscalls)):
        shadow_stack_syscall = list_default_syscalls[system_index]
        user_stack_syscall = list_user_syscalls[user_index]
        # If the syscalls don't match up, print it out and do not move on to the shadow stack syscall until there is a suitable match in user stack
        if shadow_stack_syscall != user_stack_syscall:
            print(f"The user's syscall {user_stack_syscall} at position {user_index} differs from the system's syscall {shadow_stack_syscall} at position {system_index}")
            continue
        system_index = system_index + 1


def createUserCase(program_name, previous_args):
    """
    Creation of program list with user provided arguments that will be eventually passed to run strace
    :param program_name: (str) name of the program 
    :param previous_args: (list) list of arguments provided by the user
    """
    return [STRACE_PROGRAM_STRING, program_name] + previous_args


def sanitizeSyscalls(syscall_output, list_to_record):
    """
    Takes the syscall outputs, sanitizes them and puts it into a list that is 
    stored globally.
    :param arguments: (str) raw string of raw syscall output 
    :param list_to_record: (list) list where the syscalls will be appended to 
    :returns: None
    """
    # Parse each line of syscall output based on new line
    # Given that each line is likely SYSCALL_NAME(BLAH BLAH)
    # We split by ( and take the first element
    for line in syscall_output.split(NEW_LINE_DELIM):
        list_to_record.append(line.split(LEFT_PARENTHESIS_DELIM)[INDEX_OF_SYSCALL_NAME])
    
    # We remove the last one from the list as we do not want the exit code
    list_to_record.pop()
    print(list_to_record)


def runStraceProgram(arguments, shellcode_location=None):
    """
    Runs the program (arguments[0]) and its given other arguments (arguments[1...])
    and continues to return output from the program.
    :param arguments: (list) list of the arguments
    :param arguments: (str) filename of shellcode 
    :returns: str output of the given program 
    """
    # Checks if shellcode_location is specified
    # If it is, redirect data from the file to stdin
    if shellcode_location is None:
        p = Popen(arguments, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        output = p.communicate(input=DEFAULT_TESTING_VALUE.encode())[INDEX_OF_POPEN_STDERR]
    else:
        shellcode_fd = open(shellcode_location, 'r')
        p = Popen(arguments, stdout=PIPE, stdin=shellcode_fd, stderr=PIPE)
        output = p.communicate()[INDEX_OF_POPEN_STDERR]

    # If subprocess doesnt run properly, quit program
    if output is None:
        print("[!] Subprocess call has failed")
        print(DEFAULT_TERMINATION_MESSAGE)
        sys.exit(1)
    return output.decode("utf-8").strip()


def createBaseCase(program_name):
    """
    Creation of program list with default arguments that will be eventually passed to run strace
    :param program_name: (str) name of the program 
    """
    return [STRACE_PROGRAM_STRING, program_name, DEFAULT_TESTING_VALUE]


def getAbsoluteFilepath(filepath):
    """
    Converts file path to the absolute file paths.
    :param filepath: (str) file path of the given file 
    :returns: str of the absolute file path 
    """
    return os.path.abspath(filepath)


def fileExists(filepath):
    """
    Checks if file path exists.
    :param filepath: (str) file path of the given file 
    :returns: True (if file exists), False (otherwise)
    """
    return os.path.isfile(filepath) 


def manageParser():
    """
    This initializes the parser object and adds in different variables
    :returns: parser object containing parsed information
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("program_name", help="the name of the program to test on")
    # I have added this to be variable number of arguments so that this can be scalable 
    parser.add_argument("arguments", help="""the arguments to be run with the program where the"
                                            last one is the file with the shellcode""", nargs="+")
    args = parser.parse_args()
    return args


def main():
    """
    Runs the main logic of the code. 
    """
    args = manageParser()
    filepath = args.program_name
    user_arguments = args.arguments
    previous_args = user_arguments[:-1]
    shellcode_location = user_arguments[-1]
    
    # Checks if file path of vulnerable program and shellcode exists before proceeding
    if not fileExists(filepath) and not fileExists(shellcode_location):
        print("[!] The file path location(s) does not exist!")
        print(DEFAULT_TERMINATION_MESSAGE)
        sys.exit(1)

    filepath = getAbsoluteFilepath(filepath)
    shellcode_location = getAbsoluteFilepath(shellcode_location)
    default_case = createBaseCase(filepath)
    default_output = runStraceProgram(default_case)
    sanitizeSyscalls(default_output, list_default_syscalls)

    user_case = createUserCase(filepath, previous_args)
    user_output = runStraceProgram(user_case, shellcode_location)
    sanitizeSyscalls(user_output, list_user_syscalls)
    compareSyscallStacks()

    
if __name__ == "__main__":
    main()
