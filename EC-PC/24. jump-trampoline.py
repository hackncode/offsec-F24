import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
jmp label                # Perform a relative jump to the 'label' position
"""
+
"nop\n" * 0x51 +         # Insert 0x51 (81) NOP instructions as padding
"""
label:                   # Label where the execution flow will jump
pop rdi                  # Pop the top value from the stack into the rdi register
mov rax, 0x403000        # Move the absolute address 0x403000 into the rax register
jmp rax                  # Jump to the address stored in rax (absolute jump)
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())