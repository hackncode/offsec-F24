import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov [0x404000], rax    # Store the value in rax at the memory address 0x404000
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())