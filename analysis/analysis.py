import time

def extractInstructions():
    i = 0
    with open("with_pie_with_aslr_cached.txt", mode="r") as f, open("asm4_cached.txt", mode="w") as out_file:
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

def compareInstructions():
    data_a = []
    data_b = []
    data_c = []
    # with open("asample.txt", mode="r") as a:
    #     for line in a:
    #         data_a.append(line.strip("\n"))
    
    # with open("asample1.txt", mode="r") as b:
    #     for line in b:
    #         data_b.append(line.strip("\n"))

    with open("asample2.txt", mode="r") as c:
        for line in c:
            data_c.append(line.strip("\n"))

    i = 0
    for each in data_c:
        if(each == "90" and data_c[i+1] == "c9"):
            print("found", i)
        i += 1

    print(len(data_a), len(data_b), len(data_c))
    # a_cur = 0
    # b_cur = 0
    # while True:
    #     if(a_cur == len(data_a) or b_cur == len(data_b)):
    #         break
    #     if(data_a[a_cur] == data_b[b_cur]):
    #         b_cur += 1
    #         a_cur += 1
    #     else:
    #         b_cur += 1
    # print(a_cur,b_cur)
    # print(data_a[a_cur])
    # print(data_a[a_cur], data_b[])


def main():
    #extractInstructions()
    compareInstructions()

if __name__ == "__main__":
    main()