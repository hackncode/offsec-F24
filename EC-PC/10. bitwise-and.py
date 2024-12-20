import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
and rdi, rsi    # Compute bitwise AND of rdi and rsi
push rdi        # Save result on stack
pop rax         # Load result from stack into rax
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())