import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, [0x404000]    # Load the value stored at 0x404000 into rax
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())