import time

def main():
    i = 0
    data = []
    with open("sample1.txt", mode="r") as f, open("asample1.txt", mode="w") as out_file:
        for line in f:
            if(i > 2 and "[" in line):
                print(line)
                line = line.strip("\n")
                pos_1 = line.find("0x")
                pos_2 = line.find(":")
                seq = line[0:pos_1].strip(" ")
                addr = line[pos_1:pos_2].strip(" ")
                instr = line[pos_2+1:].strip(" ").strip("\t").strip(" ")
                out_file.write(instr+"\n")
            i+=1

if __name__ == "__main__":
    main()