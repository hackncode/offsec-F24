import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov al, [0x404000]    # Load the least significant byte at 0x404000 into al
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())