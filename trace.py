import os
import argparse
import re

def runPeekabooInstrumentation():
    print("Replace me")

def saveValidShadowStack(shadowStack):
    with open('validShadowStack', 'w') as f:
        for syscall in shadowStack:
            f.write(syscall + "\n")

def generateValidShadowStack():
    shadowStack = []
    with open('validStrace', 'r') as f:
        for line in f.read().split('\n'):
            match = re.findall(r".*\(.*\).*", line)
            if match:
                syscall = match[0].split('(')[0]
                shadowStack.append(syscall)
    saveValidShadowStack(shadowStack)

def runValidStrace():
    command = f"strace ./vuln < validInput 2> validStrace"
    os.system(command)

def traceValidRun():
    runValidStrace()
    generateValidShadowStack()
    runPeekabooInstrumentation()

def setupValidInput():
    command = "python3 -c 'print(\"A\" * 1336)' > validInput"
    os.system(command)

def checkForExploitation():
    # Will generate another shadow stack call it exploitShadowStack.
    # Then compare the syscalls and if any seg fault happens - immediately red flag.
    # Next, it will generate the instrumentation using peekaboo to compare as additional layer of tracing check.
    print("Replace me")

def runExploitStrace():
    command = f"strace ./vuln < exploitInput 2> exploitStrace"
    os.system(command)

def traceExploitRun():
    runExploitStrace()
    checkForExploitation()

# Temporary function to generate a exploit/seg fault input.
def setupExploitInput():
    command = "python3 -c 'print(\"A\" * 1350)' > exploitInput"
    os.system(command)

# Will always set up input files (for exploitInput, only temporary.)
setupValidInput()
setupExploitInput()

# Sets up the python arguments.
parser = argparse.ArgumentParser(
    description="""Detects exploitation using shadow stack and instrumentation with peekaboo.
    Example usage:
    python3 trace.py -g vuln"""
)
parser.add_argument("-g", "--generate", action="store_true", help="Generates and stores a shadow stack of the valid run. Also stores other tracing information.")
parser.add_argument("-e", "--exploit", action="store_true", help="Generates and stores a shadow stack of the malicious run. Also stores other tracing information.")
args = parser.parse_args()

if args.generate:
    traceValidRun()
elif args.exploit:
    traceExploitRun()
