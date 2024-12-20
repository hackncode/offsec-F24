import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, [rsp + 0x18]   # Load Quad Word A into rax
add rax, [rsp + 0x10]   # Add Quad Word B to rax
add rax, [rsp + 0x8]    # Add Quad Word C to rax
add rax, [rsp]          # Add Quad Word D to rax
shr rax, 2              # Divide the sum by 4
push rax                # Push the average back onto the stack
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())