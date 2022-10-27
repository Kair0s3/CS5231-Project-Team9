gcc -fno-stack-protector -z execstack -no-pie -o nodef_vuln vulnerable.c
gcc -fno-stack-protector -no-pie -o vuln vulnerable.c

# Sanity Check
```
checksec nodef_vuln
[*] '/home/kair0s3/Desktop/CS5231-Project-Team9/nodef_vuln'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments

checksec vuln
[*] '/home/kair0s3/Desktop/CS5231-Project-Team9/vuln'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

With NX - vuln (196023)
```
/home/kair0s3/CS5231/Testing/dynamorio/build/bin64/drrun -c /home/kair0s3/CS5231/Testing/peekaboo/peekaboo_dr/build/libpeekaboo_dr.so -- '/home/kair0s3/Desktop/CS5231-Project-Team9/vuln' test < '/home/kair0s3/Desktop/CS5231-Project-Team9/input'
```

Without NX - nodef_vuln (196029)
```
/home/kair0s3/CS5231/Testing/dynamorio/build/bin64/drrun -c /home/kair0s3/CS5231/Testing/peekaboo/peekaboo_dr/build/libpeekaboo_dr.so -- '/home/kair0s3/Desktop/CS5231-Project-Team9/nodef_vuln' test < '/home/kair0s3/Desktop/CS5231-Project-Team9/input'
```

Generating Stripping only bytecodes
```
~/CS5231/Testing/peekaboo/read_trace vuln-196023/196023/ | awk -F '\t ' '{print $2}' | awk -F '  ' '{print $1}' | awk NF > vuln.txt
~/CS5231/Testing/peekaboo/read_trace nodef_vuln-196029/196029/ | awk -F '\t ' '{print $2}' | awk -F '  ' '{print $1}' | awk NF > nodef_vuln.txt
```


Interestingly, the nodef_vuln is the one with more instructions. hmmm
```
wc -l nodef_vuln.txt vuln.txt
 190425 nodef_vuln.txt
 190421 vuln.txt
 380846 total
```

How about comparing the instructions?
```
diff nodef_vuln.txt vuln.txt
110232,110235d110231
< 85 d2
< 0f 84 84 00 00 00
< 89 d0
< 48 89 f7
```

# Re run...

vuln - 196278

nodef_vuln - 196281

Same as before, `nodef_vuln.txt` has more instructions.
```
wc -l nodef_vuln.txt vuln.txt
 190425 nodef_vuln.txt
 190421 vuln.txt
 380846 total
```

```
diff nodef_vuln.txt vuln.txt
110232,110235d110231
< 85 d2
< 0f 84 84 00 00 00
< 89 d0
< 48 89 f7
```

How about I try the same binary name? Then compare with the run from process id `196278`.
`gcc -fno-stack-protector -z execstack -no-pie -o vuln vulnerable.c`

```
checksec vuln
[*] '/home/kair0s3/Desktop/CS5231-Project-Team9/vuln'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```

Running `/home/kair0s3/CS5231/Testing/dynamorio/build/bin64/drrun -c /home/kair0s3/CS5231/Testing/peekaboo/peekaboo_dr/build/libpeekaboo_dr.so -- '/home/kair0s3/Desktop/CS5231-Project-Team9/vuln' test < '/home/kair0s3/Desktop/CS5231-Project-Team9/input'` to generate the instructions, this time it has 190421 instructions...

Process id - 196478

```
~/CS5231/Testing/peekaboo/read_trace vuln-196478/196478/ | awk -F '\t ' '{print $2}' | awk -F '  ' '{print $1}' | awk NF > nodef_vuln.txt

# Comparison again...
wc -l nodef_vuln.txt vuln.txt
 190421 nodef_vuln.txt
 190421 vuln.txt
 380842 total

diff nodef_vuln.txt vuln.txt # Returns nothing?? No difference for NX vs non-NX.
```
