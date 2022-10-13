# Disable ASLR.
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space 
alias peek='dynamorio/build/bin64/drrun -c peekaboo/peekaboo_dr/build/libpeekaboo_dr.so -- ls'
gcc -fno-stack-protector -no-pie -o vuln vulnerable.c
