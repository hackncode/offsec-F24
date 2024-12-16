import pwn

# Update the architecture to x86-64
pwn.context.update(arch="amd64")

# Assemble the code to set rdi to 0x1337
code = pwn.asm("""
mov rdi, 0x1337
""")

# Start the process
process = pwn.process("/challenge/run")

# Write the assembled code into the process
process.write(code)

# Read and print the output
print(process.readall())
