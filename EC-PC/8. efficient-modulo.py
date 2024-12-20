import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov al, dil    # Compute rdi % 256 and store in rax
mov bx, si     # Compute rsi % 65536 and store in rbx
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())