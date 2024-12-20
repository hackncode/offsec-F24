import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, rdi        # Move m into rax
imul rax, rsi       # Multiply rax (m) by rsi (x)
add rax, rdx        # Add b to rax
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())