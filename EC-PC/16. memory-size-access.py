import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov al, [0x404000]    # Load 1 byte into rax
mov bx, [0x404000]    # Load 2 bytes into rbx
mov ecx, [0x404000]   # Load 4 bytes into rcx
mov rdx, [0x404000]   # Load 8 bytes into rdx
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())