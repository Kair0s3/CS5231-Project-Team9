## Name: poc.py
## Purpose: Run the program at its baseline, record down the syscall stack and then run the program with the user's input
## This will note down if it makes any dangerous syscalls.
## Author: Lee Ju-Ler Jonathan
## Sample Usages:
## $ python3 poc.py benign_program AAAAAAAAAAAA

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


def createUserCase(program_name, user_arguments):
    """
    Creation of program list with user provided arguments that will be eventually passed to run strace
    :param program_name: (str) name of the program 
    :param user_arguments: (list) list of arguments provided by the user 
    """
    return [STRACE_PROGRAM_STRING, program_name] + user_arguments


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


def runStraceProgram(arguments):
    """
    Runs the program (arguments[0]) and its given other arguments (arguments[1...])
    and continues to return output from the program.
    :param arguments: (list) list of the arguments
    :returns: str output of the given program 
    """
    p = Popen(arguments, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    output = p.communicate(input=DEFAULT_TESTING_VALUE.encode())[INDEX_OF_POPEN_STDERR]
    
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
    parser.add_argument("arguments", help="the arguments to be run with the program", nargs="+")
    args = parser.parse_args()
    return args


def main():
    """
    Runs the main logic of the code. 
    """
    args = manageParser()
    filepath = args.program_name
    user_arguments = args.arguments
    
    # Checks if file path exists before proceeding
    if not fileExists(filepath):
        print("[!] The file path location does not exist!")
        print(DEFAULT_TERMINATION_MESSAGE)
        sys.exit(1)

    filepath = getAbsoluteFilepath(filepath)
    default_case = createBaseCase(filepath)
    default_output = runStraceProgram(default_case)
    sanitizeSyscalls(default_output, list_default_syscalls)

    user_case = createUserCase(filepath, user_arguments)
    user_output = runStraceProgram(user_case)
    sanitizeSyscalls(user_output, list_user_syscalls)

    // TODO: Comparison between the 2 syscall list_user_syscalls
    // Testing to make sure the above poc.py works with creating another stack 
    
    
    
    

    

    



if __name__ == "__main__":
    main()