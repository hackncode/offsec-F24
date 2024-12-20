import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, 0xdeadbeef00001337  # Load 0xdeadbeef00001337 into rax
mov [rdi], rax               # Write rax value to [rdi]

mov rax, 0xc0ffee0000        # Load 0xc0ffee0000 into rax
mov [rsi], rax               # Write rax value to [rsi]
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())