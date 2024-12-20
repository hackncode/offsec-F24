import gmpy2
from gmpy2 import iroot
from pwn import *

class Exploit:
    def __init__(self, server_host, server_port, student_id):
        self.server_host = server_host
        self.server_port = server_port
        self.student_id = student_id

    def execute(self):
        print(f"\n\033[1;34m✹ Connecting to the server...\033[0m")
        print(f"\033[1;33m⚙ NetID:\033[0m \033[1;36m{self.student_id}\033[0m")
        with remote(self.server_host, self.server_port) as conn:
            print("\033[1;32m✔ Connected successfully!\033[0m")
            conn.sendlineafter(b'abc123): ', self.student_id.encode())
            print("\033[1;35m⏳ Waiting for server response...\033[0m")

            # Retrieve RSA parameters
            conn.recvuntil(b"e = "); e = int(conn.recvline().strip())
            conn.recvuntil(b"n = "); n = int(conn.recvline().strip())
            conn.recvuntil(b"c = "); c = int(conn.recvline().strip())

            print("\n\033[1;34m✨ RSA Parameters Retrieved:\033[0m")
            print(f"  \033[1;33mExponent (e):\033[0m \033[1;36m{e}\033[0m")
            print(f"  \033[1;33mModulus (n):\033[0m \033[1;36m{n}\033[0m")
            print(f"  \033[1;33mCiphertext (c):\033[0m \033[1;36m{c}\033[0m")

            # Compute plaintext using e-th root of c
            print("\n\033[1;35m🔎 Decrypting the ciphertext...\033[0m")
            plaintext_int = iroot(c, e)[0]
            plaintext = bytes.fromhex(hex(plaintext_int)[2:]).decode('utf-8')

            # Display the decrypted flag
            print("\033[1;32m🎉 Decrypted Plaintext:\033[0m")
            print(f"  \033[1;36m{plaintext}\033[0m\n")

            print("\033[1;32m🚀 Exploit complete! Enjoy your flag.\033[0m")
            conn.interactive()

if __name__ == "__main__":
    exploit = Exploit(
        server_host='offsec-chalbroker.osiris.cyber.nyu.edu',
        server_port=1515,
        student_id='<NET ID>'
    )
    exploit.execute()
