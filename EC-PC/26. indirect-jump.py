import pwn
pwn.context.update(arch="amd64")

code = pwn.asm("""
mov rax, rdi                # Copy rdi (switch case value) into rax
and rax, 0xfffffffffffffffc # Mask the lower 2 bits of rax (check if >= 4)
je down                     # If masked result is 0 (rdi < 4), jump to 'down'
jmp [rsi + 32]              # If rdi >= 4, jump to the default case (jump_table[4])
down:                       # For rdi < 4
jmp [rsi + rdi * 8]         # Indirect jump to the address at jump_table[rdi]
""")

process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())