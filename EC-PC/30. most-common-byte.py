import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
most_common_byte:
mov rbp, rsp          # Save current stack pointer
sub rsp, 0x100        # Allocate 256 bytes on the stack for frequencies
xor r10, r10          # Initialize counter
loop1:
cmp r10, rsi          # Check if i < size
ja assignfreq         # Exit loop if all bytes are processed
mov dl, byte ptr [rdi+r10] # Load byte at src_addr + i
add byte ptr [rsp+rdx], 1  # Increment frequency in stack
inc r10               # Increment counter
jmp loop1             # Repeat loop
assignfreq:
xor rbx, rbx          # Byte iterator (b = 0)
xor rcx, rcx          # Maximum frequency (max_freq = 0)
xor rax, rax          # Byte with max frequency (max_freq_byte = 0)
jmp loop2
loop2:
cmp rbx, 0xff         # Check if b > 0xFF
ja return             # Exit loop
cmp [rsp+rbx], cl     # Compare frequency with max_freq
ja updatevalues       # Update max_freq and max_freq_byte
jmp increment
updatevalues:
mov cl, [rsp+rbx]     # Update max_freq
mov rax, rbx          # Update max_freq_byte
jmp increment
increment:
inc rbx               # Increment byte iterator
jmp loop2             # Repeat loop
return:
mov rsp, rbp          # Restore stack
ret                   # Return result in rax
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())