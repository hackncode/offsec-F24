import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov rax, [rdi]       # Load the first quad word from [rdi]
mov rbx, [rdi + 8]   # Load the second quad word from [rdi + 8]
add rax, rbx         # Add the two quad words
mov [rsi], rax       # Store the sum at the memory address in rsi
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())