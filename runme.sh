# Disable ASLR.
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space 

gcc -fno-stack-protector -g -z execstack -no-pie -o vuln vulnerable.c

