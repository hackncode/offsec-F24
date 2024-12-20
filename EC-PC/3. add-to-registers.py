import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
add rdi, 0x331337   # Add 0x331337 directly to rdi
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())