import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov ah, 0x42    # Set the upper 8 bits of ax to 0x42
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())