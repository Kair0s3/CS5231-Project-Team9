## Name: poc.py
## Purpose: Run the program at its baseline, record down the syscall stack and then run the program with the user's input
## This will note down if it makes any dangerous syscalls.
## Author: Lee Ju-Ler Jonathan
## Sample Usages:
## $ python3 poc.py benign_program AAAAAAAAAAAA NAME_OF_FILE_WITH_PAYLOAD

# Imports are managed here
import os
from pickle import NEWFALSE
import sys
import argparse
from subprocess import Popen, PIPE, STDOUT


def runStraceProgram(arguments, shellcode_location=None):
    shellcode_fd = open(shellcode_location, 'r')
    p = Popen(arguments, stdout=PIPE, stdin=shellcode_fd, stderr=PIPE)
    output, err = p.communicate()
    return output.decode("utf-8").strip()

print(runStraceProgram(["/home/student/Desktop/CS5231-Project-Team9/vuln", "AAAAA"], "/home/student/Desktop/CS5231-Project-Team9/payload"))
