import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, rdi    # Move dividend into rax
xor rdx, rdx    # Clear rdx (upper 64-bits of dividend)
div rsi         # Perform division, remainder in rdx
mov rax, rdx    # Move remainder into rax
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())