# CS5231 Project Team 9

## Setup

Phase 1: No protections

To run with no protections in place, the code can be compiled with the following command 

```
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space 
gcc -fno-stack-protector -no-pie -o vuln vulnerable.c
```
