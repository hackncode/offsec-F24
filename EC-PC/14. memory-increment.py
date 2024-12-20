import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, [0x404000]          # Load value at 0x404000 into rax
add qword ptr [0x404000], 0x1337 # Increment the value at 0x404000 by 0x1337
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())