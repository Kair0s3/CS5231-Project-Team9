from ast import arg
import sys


def parseAddress(val):
    return "\\x".join([val[i:i+2].upper() for i in range(0, len(val), 2)][::-1])


def main():
    user_input = sys.argv[1]
    print(f"The little endian address in bytes is \\x{parseAddress(user_input[2:])}")



if __name__ == '__main__':
    main()