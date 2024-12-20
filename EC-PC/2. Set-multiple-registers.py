import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, 0x1337            # Set rax to 0x1337
mov r12, 0xCAFED00D1337BEEF # Set r12 to 0xCAFED00D1337BEEF
mov rsp, 0x31337           # Set rsp to 0x31337
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())