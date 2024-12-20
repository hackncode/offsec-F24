from pwn import *
import ctypes

class Exploit:
    def __init__(self, server_host, server_port, student_id):
        self.server_host = server_host
        self.server_port = server_port
        self.student_id = student_id

    def get_prediction(self):
        libc = ctypes.CDLL("libc.so.6")
        current_time = ctypes.c_long()
        libc.time(ctypes.byref(current_time))
        libc.srand(current_time.value + 0x19)
        return libc.rand()

    def execute(self):
        print(f"\n\033[1;34m✹ Connecting to the server with NetID: \033[1;36m{self.student_id}\033[0m")
        with remote(self.server_host, self.server_port) as conn:
            conn.sendlineafter(b'abc123): ', self.student_id.encode())
            print("\033[1;32m✓ Waiting for server response...\033[0m")
            conn.recvuntil(b"Please wait a moment...")

            prediction = self.get_prediction()
            conn.sendline(f"{prediction}".encode())

            print("\033[1;32m✔ Prediction sent successfully!\033[0m")
            print(f"\033[1;33m🔮 Random Prediction: \033[1;36m{prediction}\033[0m")

            conn.interactive()

if __name__ == "__main__":
    exploit = Exploit(
        server_host='offsec-chalbroker.osiris.cyber.nyu.edu',
        server_port=1514,
        student_id='<NET ID>'
    )
    exploit.execute()
