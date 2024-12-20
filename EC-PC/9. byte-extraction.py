import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, rdi    # Copy rdi to rax
shr rax, 32     # Shift right by 32 bits (4 bytes)
shl rax, 56     # Shift left by 56 bits to clear unwanted bits
shr rax, 56     # Shift right by 56 bits to isolate B4
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())