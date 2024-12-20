import gmpy2
from gmpy2 import gcdext, powmod
from pwn import *
import binascii

class RSACommonModulusExploit:
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
            print("\033[1;35m⏳ Retrieving RSA parameters...\033[0m")

            conn.recvuntil(b"e1 = "); e1 = int(conn.recvline().strip())
            conn.recvuntil(b"n1 = "); n1 = int(conn.recvline().strip())
            conn.recvuntil(b"c1 = "); c1 = int(conn.recvline().strip())
            conn.recvuntil(b"e2 = "); e2 = int(conn.recvline().strip())
            conn.recvuntil(b"n2 = "); n2 = int(conn.recvline().strip())
            conn.recvuntil(b"c2 = "); c2 = int(conn.recvline().strip())

            print("\n\033[1;34m✨ RSA Parameters Retrieved:\033[0m")
            print(f"  \033[1;33mExponent 1 (e1):\033[0m \033[1;36m{e1}\033[0m")
            print(f"  \033[1;33mModulus (n1):\033[0m \033[1;36m{n1}\033[0m")
            print(f"  \033[1;33mCiphertext 1 (c1):\033[0m \033[1;36m{c1}\033[0m")
            print(f"  \033[1;33mExponent 2 (e2):\033[0m \033[1;36m{e2}\033[0m")
            print(f"  \033[1;33mModulus (n2):\033[0m \033[1;36m{n2}\033[0m")
            print(f"  \033[1;33mCiphertext 2 (c2):\033[0m \033[1;36m{c2}\033[0m")

            print("\n\033[1;35m🔎 Calculating coefficients using Extended Euclidean Algorithm...\033[0m")
            _, a, b = gcdext(e1, e2)

            print("\033[1;32m✔ Coefficients Computed Successfully!\033[0m")
            print(f"  \033[1;33mCoefficient a:\033[0m \033[1;36m{a}\033[0m")
            print(f"  \033[1;33mCoefficient b:\033[0m \033[1;36m{b}\033[0m")

            print("\n\033[1;35m🔓 Decrypting Ciphertexts...\033[0m")
            m = (powmod(c1, a, n1) * powmod(c2, b, n1)) % n1
            plaintext = binascii.unhexlify(hex(m)[2:]).decode('utf-8')

            print("\033[1;32m🎉 Decrypted Plaintext:\033[0m")
            print(f"  \033[1;36m{plaintext}\033[0m\n")

            print("\033[1;32m🚀 Exploit Complete! Enjoy your flag.\033[0m")

if __name__ == "__main__":
    exploit = RSACommonModulusExploit(
        server_host='offsec-chalbroker.osiris.cyber.nyu.edu',
        server_port=1516,
        student_id='<NET ID>'
    )
    exploit.execute()
