import pwn
pwn.context.update(arch="amd64")

code = pwn.asm("""
xor rax, rax             # Initialize rax to 0 (sum)
xor rcx, rcx             # Initialize rcx to 0 (temporary register)
mov rbx, rsi             # Copy n (rsi) into rbx (loop counter)

loop:                    # Loop label
sub rbx, 1               # Decrement rbx (loop counter)
mov ecx, [rdi + rbx*8]   # Load quad word at [rdi + rbx*8] into ecx
add rax, rcx             # Add the value in ecx to rax (accumulate sum)
cmp rbx, 0               # Check if rbx (loop counter) is 0
jne loop                 # If rbx != 0, jump back to 'loop'

div rsi                  # Divide sum in rax by n (rsi) to compute average
""")

process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())