#include <stdio.h>

int vulnerable(char *printf_str) {
    char buffer[1337];
    printf(printf_str);
    gets(buffer);
}

int main(int argc, char **argv) {
    vulnerable(argv[1]);
    puts("Return properly!");
    return 0;
}
