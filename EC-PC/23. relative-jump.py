import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
jmp target          # Perform a relative jump to the label `target`
.rept 0x51 - 2 + 2  # Adjust padding with nops to align correctly
nop
.endr
target:
mov rax, 0x1        # Set rax to 0x1 at the target location
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())