import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, rdi   # Move distance into rax
xor rdx, rdx   # Clear rdx to ensure no upper 64-bits
div rsi        # Divide rax (distance) by rsi (time), result in rax
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())