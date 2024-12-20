import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, 0x403000  # Load the absolute address into rax
jmp rax            # Perform the jump to the address in rax
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())