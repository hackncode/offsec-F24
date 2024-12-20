import pwn
pwn.context.update(arch="amd64")

code = pwn.asm("""
mov rax, 0               # Initialize rax to 0 (default result)
cmp rdi, 0               # Check if the memory address rdi is 0
je done                  # If rdi == 0, jump to the 'done' label (set rax to 0 and exit)
mov rsi, -1              # Initialize rsi to -1 (acts as a counter, incremented in the loop)
loop:                    # Start of the loop
add rsi, 1               # Increment the counter (rsi)
mov rbx, [rdi + rsi]     # Load the byte at [rdi + rsi] into rbx
cmp rbx, 0               # Compare the loaded byte with 0
jne loop                 # If the byte is non-zero, repeat the loop
mov rax, rsi             # Store the final count of non-zero bytes into rax
done:                    # End of the function
""")

process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())