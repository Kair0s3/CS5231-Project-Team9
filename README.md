# CS5231 Project Team 9

## Setup

Phase 1: No protections

To run with no protections in place, the code can be compiled with the following command

```
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
gcc -fno-stack-protector -z execstack -no-pie -o vuln vulnerable.c
```

Phase 2: NX enabled

To run with NX in place, the code can be compiled with the following command

```
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
gcc -fno-stack-protector -no-pie -o vuln vulnerable.c
```

Phase 3: NX enabled and Canary

To run with NX and Canary in place, the code can be compiled with the following command

```
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
gcc -no-pie -D_FORTIFY_SOURCE=0 -o vuln vulnerable.c
```

## Tracing Script v0.0.1

> Currently, all the values - e.g. the commands, paths are hard-coded for now.

### How to use/run
```
# For the initial generation using valid vuln run.
python3 trace.py -g

# To run the exploited vuln run.
python3 trace.py -e
```
