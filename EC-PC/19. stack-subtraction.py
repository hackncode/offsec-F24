import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
pop rax           # Retrieve the top value from the stack into rax
sub rax, rdi      # Subtract rdi from the value in rax
push rax          # Push the updated value back onto the stack
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())