from pwn import *
import ctypes
import re
import time

class CLibraryRandom:
    def __init__(self):
        self.libc = ctypes.CDLL("libc.so.6")
        self.libc.srand.argtypes = [ctypes.c_uint]
        self.libc.rand.restype = ctypes.c_int

    def set_seed(self, seed):
        self.libc.srand(seed)

    def get_random_byte(self):
        return self.libc.rand() & 0xFF

class XORDecrypt:
    def __init__(self):
        self.random_gen = CLibraryRandom()

    def decrypt(self, encrypted_data, seed):
        self.random_gen.set_seed(seed)
        return bytes(byte ^ self.random_gen.get_random_byte() for byte in encrypted_data)

class CiphertextExtractor:
    @staticmethod
    def extract(response):
        hex_pattern = r'[a-fA-F0-9]{64,}'
        match = re.search(hex_pattern, response)
        return bytes.fromhex(match.group(0)) if match else None

class FlagBruteForcer:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext
        self.decryptor = XORDecrypt()

    def brute_force(self, base_time, time_offset):
        for t in range(base_time - time_offset, base_time + time_offset):
            seed = t * t
            decrypted = self.decryptor.decrypt(self.ciphertext, seed)
            try:
                decoded_text = decrypted.decode('utf-8')
                if "flag{" in decoded_text:
                    return seed, decoded_text
            except UnicodeDecodeError:
                continue
        return None, None

class Exploit:
    def __init__(self, server_host, server_port, student_id):
        self.server_host = server_host
        self.server_port = server_port
        self.student_id = student_id

    def connect(self):
        print(f"\n\033[1;34m✹ Connecting to the server with NetID: \033[1;36m{self.student_id.decode()}\033[0m")
        with remote(self.server_host, self.server_port) as conn:
            conn.sendlineafter(b'abc123): ', self.student_id)
            print("\033[1;32m✓ Waiting for server response...\033[0m")
            return conn.recvall(timeout=2).decode()

    def execute(self):
        response = self.connect()
        ciphertext = CiphertextExtractor.extract(response)
        if not ciphertext:
            print("\033[1;31m❌ Failed to extract ciphertext.\033[0m")
            return

        print("\033[1;34m✨ Ciphertext extracted successfully.\033[0m")
        current_time = int(time.time())
        search_window = 3600
        print("\033[1;33m⏳ Brute-forcing seeds...\033[0m")
        brute_forcer = FlagBruteForcer(ciphertext)
        seed, flag = brute_forcer.brute_force(current_time, search_window)

        if flag:
            print("\n\033[1;32m⭐ Flag found:\033[0m")
            print(f"\033[1;36m{flag}\033[0m")
        else:
            print("\033[1;31m❌ Could not retrieve the flag.\033[0m")

if __name__ == "__main__":
    exploit = Exploit(
        server_host='offsec-chalbroker.osiris.cyber.nyu.edu',
        server_port=1517,
        student_id=b'<NET ID>'
    )
    exploit.execute()
