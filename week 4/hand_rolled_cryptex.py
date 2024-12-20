from pwn import *

def main():
    p = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1273)
    p.recvuntil(b'Please input your NetID (something like abc123): ')
    p.sendline(b'<NET ID>')

    # Phase 1
    p.recvuntil(b'The first round requires two inputs...\n > ', timeout=5)
    p.sendline(b'flag.txt')
    p.recvuntil(b' > ', timeout=5)
    p.sendline(b'0')
    data = p.recvuntil(b'The second phase requires a single input...\n > ', timeout=5)
    print(data.decode('latin1'))

    # Extract the file descriptor
    try:
        fd_bytes = data.split(b'interior...\n')[1][:4]
        fd = int.from_bytes(fd_bytes, 'little', signed=True)
        print(f"Extracted file descriptor: {fd}")
        if fd < 0:
            print("Failed to open file. Exiting.")
            p.close()
            return
    except Exception as e:
        print(f"Error extracting file descriptor: {e}")
        p.close()
        return

    # Phase 2
    input_char = ((~fd) ^ 0xC9) & 0xFF
    p.send(bytes([input_char]))
    data = p.recvuntil(b'final level requires another single input...\n > ', timeout=5)
    print(data.decode('latin1'))

    # Phase 3
    p.send(bytes([2]))
    output = p.recvall(timeout=5)
    print(output.decode('latin1'))
    p.close()

if __name__ == '__main__':
    main()