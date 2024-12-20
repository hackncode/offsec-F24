import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
str_lower:
xor r10, 0x0               # Initialize counter to 0
cmp rdi, 0x0               # Check if src_addr is 0
jz end                     # Exit if src_addr is 0
loop:
mov rbx, rdi               # Store current src_addr in rbx
mov rax, 0x403000          # Load the address of foo into rax
xor rdi, rdi               # Clear rdi
mov dil, byte ptr [rbx]    # Load the byte at src_addr
cmp dil, 0x0               # Check for zero byte
jz end                     # Exit loop if zero byte is found
cmp dil, 0x5A              # Check if the byte is <= 0x5A
ja skip_foo                # Skip foo if not uppercase
add r10, 0x1               # Increment conversion counter
call rax                   # Call foo
mov byte ptr [rbx], al     # Write the result of foo back to memory
skip_foo:
mov rdi, rbx               # Update src_addr
add rdi, 0x1               # Move to next byte
jmp loop                   # Repeat loop
end:
mov rax, r10               # Return the conversion count
ret
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())