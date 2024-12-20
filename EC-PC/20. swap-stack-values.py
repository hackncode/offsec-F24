import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
push rdi       # Push the value in rdi onto the stack
push rsi       # Push the value in rsi onto the stack
pop rdi        # Pop the top value (original rsi) into rdi
pop rsi        # Pop the next value (original rdi) into rsi
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())