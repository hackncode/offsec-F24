import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
and rdi, 1        # Extract LSB of rdi
xor rdi, 1        # Invert the result: 1 if even, 0 if odd
xor rax, rax      # Clear rax (set y = 0)
or rax, rdi       # Set rax to the result
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())