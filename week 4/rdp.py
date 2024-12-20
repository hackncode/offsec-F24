from pwn import *
p = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1272)
p.recvuntil('Please input your NetID (something like abc123): ')
p.sendline('<NET ID>')
p.recvuntil("Send me the right data and I'll give you the flag!\n")

# Packet 1 Connect
p.send(bytes([0x03, 0x00, 0x00]))
print(p.recvline().decode().strip())

# Packet 2 Send Value
p.send(bytes([0x04, 0x01, 0x00, 0x37]))
print(p.recvline().decode().strip())

# Packet 3 Disconnect
p.send(bytes([0x03, 0x02, 0x00]))
print(p.recvline().decode().strip())

while True:
    try:
        line = p.recvline()
        if not line:
            break
        print(line.decode().strip())
    except EOFError:
        break

p.close()